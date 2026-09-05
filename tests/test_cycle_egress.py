import importlib.util
import ipaddress
import json
import os
from pathlib import Path
import socket
import subprocess
import threading
import uuid

import pytest


RUNTIME = Path(__file__).parents[1] / "agent-runtime"
spec = importlib.util.spec_from_file_location("cycle_egress", RUNTIME / "egress_proxy.py")
proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proxy)


@pytest.mark.parametrize("address", ["127.0.0.1", "10.1.2.3", "169.254.169.254", "::1", "fc00::1", "::ffff:127.0.0.1"])
def test_proxy_denies_non_public_dns_answers(monkeypatch, address):
    family = socket.AF_INET6 if ipaddress.ip_address(address).version == 6 else socket.AF_INET
    monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **k: [(family, socket.SOCK_STREAM, 6, "", (address, 443))])
    with pytest.raises(ValueError, match="not public"):
        proxy.resolve_public("github.com")


@pytest.mark.parametrize("proxy_request", [
    b"CONNECT example.com:443 HTTP/1.1\r\n\r\n",
    b"CONNECT github.com:80 HTTP/1.1\r\n\r\n",
    b"CONNECT 127.0.0.1:443 HTTP/1.1\r\n\r\n",
    b"GET http://github.com/ HTTP/1.1\r\n\r\n",
    b"CONNECT github.com.evil.invalid:443 HTTP/1.1\r\n\r\n",
])
def test_proxy_rejects_disallowed_requests_over_a_real_socket(proxy_request):
    with proxy.Server(("127.0.0.1", 0), proxy.Handler) as server:
        server.allowed_hosts = {"github.com"}
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with socket.create_connection(server.server_address, timeout=2) as connection:
                connection.sendall(proxy_request)
                assert connection.recv(1024).startswith(b"HTTP/1.1 403")
        finally:
            server.shutdown()
            thread.join()


@pytest.mark.skipif(os.environ.get("SCORE2GP_DOCKER_TESTS") != "1", reason="explicit Docker smoke test")
def test_real_docker_owner_and_enforced_egress(tmp_path):
    """No agent login or GitHub token: real mounts, Git, proxy and negative network controls."""
    spec = importlib.util.spec_from_file_location("docker_cycle", RUNTIME / "cycle.py")
    cycle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cycle)
    name = "score2gp-smoke-" + uuid.uuid4().hex
    network, proxy_name = name + "-net", name + "-proxy"
    image = os.environ.get("SCORE2GP_TEST_IMAGE", "score2gp-codex:local")
    uid, gid = os.getuid(), os.getgid()
    config = tmp_path / "assignment.json"
    config.write_text(json.dumps({"egress_hosts": ["api.github.com"]}))
    repo = tmp_path / "repo"
    repo.mkdir()
    def docker(*args):
        return subprocess.run(["docker", *map(str, args)], check=True, capture_output=True, text=True).stdout
    try:
        docker("network", "create", "--internal", network)
        argv = cycle.common_container(proxy_name, image, uid, gid)
        argv += ["--detach", "--network", "bridge", "--entrypoint", "python"]
        argv += cycle.bind(RUNTIME / "egress_proxy.py", "/proxy.py") + cycle.bind(config, "/assignment.json")
        subprocess.run(argv + [image, "/proxy.py", "/assignment.json"], check=True, capture_output=True)
        docker("network", "connect", "--alias", "egress", network, proxy_name)
        docker("exec", proxy_name, "python", "-c",
               "import socket,time\nfor i in range(50):\n try:\n  socket.create_connection(('127.0.0.1',3128),1).close(); break\n except OSError: time.sleep(.1)\nelse: raise SystemExit(1)")
        code = '''
import os, pathlib, socket, subprocess, urllib.request, urllib.error
p = pathlib.Path('/repo')
(p / 'created.py').write_text('value = 1\\n')
assert (p / 'created.py').stat().st_uid == os.getuid()
subprocess.run(['git', 'init', '/repo'], check=True, capture_output=True)
subprocess.run(['git', '-C', '/repo', 'add', '.'], check=True)
subprocess.run(['git', '-C', '/repo', '-c', 'user.name=Smoke', '-c', 'user.email=smoke@example.invalid', 'commit', '-m', 'Smoke'], check=True, capture_output=True)
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'https': 'http://egress:3128'}))
assert opener.open('https://api.github.com/zen', timeout=15).status == 200
try:
    opener.open('https://example.com/', timeout=5)
except urllib.error.URLError as exc:
    assert '403' in str(exc), str(exc)
else:
    raise AssertionError('non-allowlisted endpoint reachable')
try:
    socket.create_connection(('1.1.1.1',443), timeout=2)
except OSError:
    pass
else:
    raise AssertionError('direct outbound bypass reachable')
print('PASS: host ownership, allowed HTTPS, denied HTTPS, blocked direct egress')
'''
        argv = cycle.common_container(name, image, uid, gid)
        argv += ["--network", network, "--entrypoint", "python"] + cycle.bind(repo, "/repo", False)
        result = subprocess.run(argv + [image, "-c", code], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert "PASS:" in result.stdout
        assert all(p.stat().st_uid == uid for p in repo.rglob("*"))
        subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], check=True, capture_output=True)
        # A second cycle must be able to edit files written by the first.
        argv = cycle.common_container(name, image, uid, gid)
        argv += ["--network", "none", "--entrypoint", "python"] + cycle.bind(repo, "/repo", False)
        subprocess.run(argv + [image, "-c", "from pathlib import Path; Path('/repo/created.py').write_text('value = 2\\n')"], check=True, capture_output=True)
        assert (repo / "created.py").read_text() == "value = 2\n"
    finally:
        for target in (name, proxy_name):
            subprocess.run(["docker", "rm", "--force", target], capture_output=True)
        subprocess.run(["docker", "network", "rm", network], capture_output=True)


@pytest.mark.skipif(os.environ.get("SCORE2GP_DOCKER_TESTS") != "1", reason="explicit Docker smoke test")
def test_offline_utility_does_not_create_foreign_owned_files(tmp_path):
    repo = tmp_path / "offline-repo"
    repo.mkdir()
    subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
    (repo / "pyproject.toml").write_text('[project]\nname = "score2gp"\nversion = "0.0.0"\n')
    package = repo / "src/score2gp"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("value = 1\n")
    task = "offline-smoke-" + uuid.uuid4().hex
    env = os.environ.copy()
    env.update(SCORE2GP_PRODUCT_DIR=str(repo), SCORE2GP_TASK=task,
               SCORE2GP_AGENT_IMAGE=os.environ.get("SCORE2GP_TEST_IMAGE", "score2gp-codex:local"))
    code = "import os,score2gp; from pathlib import Path; assert score2gp.value == 1; Path('created.txt').write_text(str(os.getuid()))"
    try:
        result = subprocess.run([str(RUNTIME / "start-agent.sh"), "python", "-c", code],
                                env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert (repo / "created.txt").read_text() == str(os.getuid())
        assert all(p.stat().st_uid == os.getuid() for p in repo.rglob("*"))
        assert not list(repo.rglob("*.egg-info"))
    finally:
        env.update(SCORE2GP_HOST_UID=str(os.getuid()), SCORE2GP_HOST_GID=str(os.getgid()),
                   COMPOSE_PROJECT_NAME=f"score2gp-agent-{task}")
        subprocess.run(["docker", "compose", "--file", str(RUNTIME / "compose.yaml"), "down"], env=env, capture_output=True)
