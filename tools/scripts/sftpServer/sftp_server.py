"""
Red Brixen Security — Portable SFTP Server

A lightweight, operator-focused SFTP server designed for rapid deployment
in field environments.

Core Capabilities:
- Serves the current working directory as an isolated SFTP root
- Username/password authentication (runtime supplied)
- Minimal dependencies (Paramiko only)
- Safe path resolution to prevent directory traversal
- Supports file upload and download
- Designed for short-lived, controlled transfer sessions

Intended Use:
- Rapid file transfer during security assessments
- Controlled data staging between systems
- Temporary secure file dropbox

Security Model:
- Not hardened for long-term exposure
- Assumes trusted operator control
- Plaintext password authentication (by design)
"""

from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
import errno
import os
import socket
import time

import paramiko


def log(msg: str):
    print(f"[Red Brixen] {msg}")


def valid_port(value):
    try:
        port = int(value)
    except ValueError as exc:
        raise ArgumentTypeError("Port must be an integer") from exc

    if not 1 <= port <= 65535:
        raise ArgumentTypeError("Port must be between 1 and 65535")

    return port


def parse_args():
    parser = ArgumentParser(
        description="Portable SFTP server serving the current directory"
    )

    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--port", type=valid_port, default=22)

    args = parser.parse_args()

    return {
        "username": args.username,
        "password": args.password,
        "port": args.port,
        "base_dir": Path.cwd(),
    }


def load_or_create_host_key(key_path: Path):
    if key_path.exists():
        log(f"Loading existing host key from: {key_path}")
        return paramiko.RSAKey.from_private_key_file(str(key_path))

    log(f"Generating new host key at: {key_path}")
    host_key = paramiko.RSAKey.generate(bits=2048)
    host_key.write_private_key_file(str(key_path))
    key_path.chmod(0o600)
    return host_key


def ensure_port_permissions(port: int):
    if port < 1024 and os.name != "nt":
        if os.geteuid() != 0:
            raise PermissionError(
                f"Port {port} requires elevated privileges. "
                f"Use sudo or a higher port like 2222."
            )


def create_listening_socket(port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    return server_socket


class SimpleSSHServer(paramiko.ServerInterface):
    def __init__(self, allowed_username: str, allowed_password: str):
        self.allowed_username = allowed_username
        self.allowed_password = allowed_password

    def check_auth_password(self, username: str, password: str):
        if username == self.allowed_username and password == self.allowed_password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username: str):
        return "password"

    def check_channel_request(self, kind: str, chanid: int):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


class SimpleSFTPHandle(paramiko.SFTPHandle):
    def __init__(self, flags, file_obj):
        super().__init__(flags)
        self.file_obj = file_obj

    def read(self, offset, length):
        try:
            self.file_obj.seek(offset)
            return self.file_obj.read(length)
        except OSError as exc:
            return paramiko.SFTPServer.convert_errno(exc.errno)

    def write(self, offset, data):
        try:
            self.file_obj.seek(offset)
            self.file_obj.write(data)
            self.file_obj.flush()
            return paramiko.SFTP_OK
        except OSError as exc:
            return paramiko.SFTPServer.convert_errno(exc.errno)

    def close(self):
        try:
            self.file_obj.close()
        except OSError as exc:
            return paramiko.SFTPServer.convert_errno(exc.errno)
        return paramiko.SFTP_OK


class SimpleSFTPServer(paramiko.SFTPServerInterface):
    def __init__(self, server, *args, base_dir: Path, **kwargs):
        super().__init__(server, *args, **kwargs)
        self.base_dir = base_dir.resolve()
        log(f"SFTP initialized (base: {self.base_dir})")

    def _resolve_path(self, path: str) -> Path:
        if not path or path == "/":
            return self.base_dir

        relative_path = path.lstrip("/")
        candidate_path = (self.base_dir / relative_path).resolve()

        try:
            candidate_path.relative_to(self.base_dir)
        except ValueError as exc:
            raise PermissionError(
                errno.EACCES,
                "Access denied: path escapes base directory",
                str(candidate_path),
            ) from exc

        return candidate_path

    def stat(self, path: str):
        try:
            local_path = self._resolve_path(path)
            return paramiko.SFTPAttributes.from_stat(local_path.stat())
        except OSError as exc:
            return paramiko.SFTPServer.convert_errno(exc.errno)

    def lstat(self, path: str):
        try:
            local_path = self._resolve_path(path)
            return paramiko.SFTPAttributes.from_stat(local_path.lstat())
        except OSError as exc:
            return paramiko.SFTPServer.convert_errno(exc.errno)

    def list_folder(self, path: str):
        try:
            local_path = self._resolve_path(path)

            if not local_path.is_dir():
                raise NotADirectoryError(errno.ENOTDIR, "Not a directory")

            entries = []
            for entry in local_path.iterdir():
                attrs = paramiko.SFTPAttributes.from_stat(entry.lstat())
                attrs.filename = entry.name
                entries.append(attrs)

            return entries

        except OSError as exc:
            return paramiko.SFTPServer.convert_errno(exc.errno)

    def open(self, path: str, flags, attr):
        try:
            local_path = self._resolve_path(path)

            if flags & os.O_CREAT:
                local_path.parent.mkdir(parents=True, exist_ok=True)

            fd = os.open(str(local_path), flags, 0o644)

            access_mode = flags & os.O_ACCMODE
            if access_mode == os.O_WRONLY:
                mode = "wb"
            elif access_mode == os.O_RDWR:
                mode = "r+b"
            else:
                mode = "rb"

            if flags & os.O_APPEND:
                mode = "a+b"

            file_obj = os.fdopen(fd, mode)
            return SimpleSFTPHandle(flags, file_obj)

        except OSError as exc:
            return paramiko.SFTPServer.convert_errno(exc.errno)


def handle_client_connection(client_socket, config, host_key):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)

    transport.set_subsystem_handler(
        "sftp",
        paramiko.SFTPServer,
        SimpleSFTPServer,
        base_dir=config["base_dir"],
    )

    server = SimpleSSHServer(config["username"], config["password"])

    try:
        transport.start_server(server=server)
        log("SSH negotiation started")

        channel = transport.accept(timeout=30)
        if channel is None:
            log("No channel received")
            return

        log("Client authenticated")

        while transport.is_active():
            time.sleep(1)

    finally:
        transport.close()


if __name__ == "__main__":
    config = parse_args()

    key_dir = Path.home() / ".portable_sftp_server"
    key_dir.mkdir(parents=True, exist_ok=True)
    key_path = key_dir / "host_key.pem"

    host_key = load_or_create_host_key(key_path)

    ensure_port_permissions(config["port"])

    print("\nRed Brixen Security — Portable SFTP Server")
    print("--------------------------------------------------")

    log(f"Username : {config['username']}")
    log(f"Port     : {config['port']}")
    log(f"Base dir : {config['base_dir']}")
    log(f"Host key : {key_path}")
    log("WARNING: Plaintext password authentication in use")

    server_socket = create_listening_socket(config["port"])

    try:
        log(f"Listening on 0.0.0.0:{config['port']}")
        client_socket, addr = server_socket.accept()

        try:
            log(f"Connection from {addr}")
            handle_client_connection(client_socket, config, host_key)
        finally:
            client_socket.close()
    finally:
        server_socket.close()