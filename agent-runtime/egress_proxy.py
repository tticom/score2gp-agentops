#!/usr/bin/env python3
"""HTTPS CONNECT proxy: exact DNS allowlist, public addresses only, port 443 only."""
import ipaddress
import json
import select
import socket
import socketserver
import sys

MAX_REQUEST_LINE_BYTES = 4096
MAX_HEADERS_BYTES = 16384
REQUEST_TIMEOUT_SECONDS = 15
CONNECT_TIMEOUT_SECONDS = 15
PROXY_IDLE_TIMEOUT_SECONDS = 120
PROXY_BUFFER_BYTES = 65536


def resolve_public(host):
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        raise ValueError("destination is not public")
    return addresses


class Handler(socketserver.StreamRequestHandler):
    timeout = REQUEST_TIMEOUT_SECONDS

    def handle(self):
        try:
            line = self.rfile.readline(MAX_REQUEST_LINE_BYTES + 1)
            if len(line) > MAX_REQUEST_LINE_BYTES:
                raise ValueError("request too large")
            method, authority, version = line.decode("ascii").strip().split()
            host, port = authority.rsplit(":", 1)
            if method != "CONNECT" or port != "443" or host not in self.server.allowed_hosts:
                raise ValueError("destination denied")
            size = 0
            while True:
                header = self.rfile.readline(MAX_REQUEST_LINE_BYTES + 1)
                size += len(header)
                if size > MAX_HEADERS_BYTES or not header:
                    raise ValueError("invalid headers")
                if header in (b"\r\n", b"\n"):
                    break
            # Connect to the validated numeric address, avoiding a second DNS lookup.
            upstream = None
            for family, kind, proto, _, address in resolve_public(host):
                candidate = socket.socket(family, kind, proto)
                candidate.settimeout(CONNECT_TIMEOUT_SECONDS)
                try:
                    candidate.connect(address)
                    upstream = candidate
                    break
                except OSError:
                    candidate.close()
            if upstream is None:
                raise OSError("destination unavailable")
        except (ValueError, OSError, UnicodeError):
            self.wfile.write(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Length: 0\r\n\r\n")
            return
        with upstream:
            self.wfile.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            self.wfile.flush()
            peers = (self.connection, upstream)
            while True:
                readable, _, _ = select.select(peers, [], [], PROXY_IDLE_TIMEOUT_SECONDS)
                if not readable:
                    return
                for source in readable:
                    chunk = source.recv(PROXY_BUFFER_BYTES)
                    if not chunk:
                        return
                    (upstream if source is self.connection else self.connection).sendall(chunk)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("0.0.0.0", 3128), Handler) as server:
        server.allowed_hosts = set(json.load(open(sys.argv[1]))["egress_hosts"])
        server.serve_forever()
