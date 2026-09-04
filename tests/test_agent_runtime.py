import os
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "agent-runtime/scripts/run-agy.sh"


def test_run_agy_uses_valid_long_form_bind_mount(tmp_path):
    product_dir = tmp_path / "product"
    product_dir.mkdir()
    (product_dir / "pyproject.toml").write_text("[project]\nname = 'test-product'\n")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    args_file = tmp_path / "docker-args"
    (bin_dir / "docker").write_text(
        "#!/usr/bin/env bash\n"
        "if [[ $1 == volume ]]; then exit 0; fi\n"
        f"printf '%s\\n' \"$@\" > {args_file}\n"
    )
    (bin_dir / "docker").chmod(0o755)

    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}:{env['PATH']}",
        SCORE2GP_PRODUCT_DIR=str(product_dir),
        AGY_CONFIG_VOLUME="test-config",
    )
    result = subprocess.run(
        [str(SCRIPT), "--help"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    args = args_file.read_text().splitlines()
    mount_values = [value for index, value in enumerate(args) if args[index - 1] == "--mount"]
    assert "type=bind,src=" + str(product_dir) + ",dst=/workspace/score2gp,readonly=false" in mount_values
