import os
import socket
import paramiko
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path

class SimpleSSHServer(paramiko.ServerInterface):
    def __init__(self, allowed_username: str, allowed_password: str):
        self.allowed_username = allowed_username
        self.allowed_password = allowed_password

    def check_auth_password(self, username: str, password: str):
        if (
            username == self.allowed_username
            and password == self.allowed_password
        ):
            return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username: str):
        return "password"

    def check_channel_request(self, kind: str, chanid: int):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def valid_port(value):
    try:
        port = int(value)
    except ValueError as exc:
        raise ArgumentTypeError("Port must be an integer") from exc

    if not 1 <= port <= 65535:
        raise ArgumentTypeError("Port must be between 1 and 65535")

    return port

def load_or_create_host_key(key_path: Path):
    if key_path.exists():
        print(f"[+] Loading existing host key from: {key_path}")
        return paramiko.RSAKey.from_private_key_file(str(key_path))

    print(f"[+] Host key not found. Generating new key at: {key_path}")
    host_key = paramiko.RSAKey.generate(bits=2048)
    host_key.write_private_key_file(str(key_path))
    key_path.chmod(0o600)
    return host_key

def ensure_port_permissions(port: int):
    if port < 1024 and os.name != "nt":
        if os.geteuid() != 0:
            raise PermissionError(
                f"Port {port} requires elevated privileges. "
                f"Run with sudo/root or use a higher port such as 2222."
            )


def create_listening_socket(port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    return server_socket


def parse_args():
    parser = ArgumentParser(
        description="Portable SFTP server serving the current directory"
    )
    parser.add_argument(
        "--username", 
        required=True,
        help="Username required for SFTP login")

    parser.add_argument(
        "--password",
        required=True,
        help="Password required for SFTP login"
    )

    parser.add_argument(
        "--port",
        type=valid_port,
        default=22,
        help="Port to listen on (default: 22)"
    )

    args = parser.parse_args()

    config = {
        "username": args.username,
        "password": args.password,
        "port": args.port,
        "base_dir": Path.cwd(),
    }

    return config

def handle_client_connection(
    client_socket,
    config: dict,
    host_key,
):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)

    server = SimpleSSHServer(
        allowed_username=config["username"],
        allowed_password=config["password"],
    )

    try:
        transport.start_server(server=server)
        print("[+] SSH negotiation started")

        channel = transport.accept(timeout=30)
        if channel is None:
            print("[-] No channel request received before timeout")
            return

        print("[+] SSH client authenticated and opened a session channel")
        channel.close()

    finally:
        transport.close()


if __name__ == "__main__":
    config = parse_args()

    key_path = Path("host_key.pem")
    host_key = load_or_create_host_key(key_path)

    ensure_port_permissions(config["port"])

    print("Startup configuration:")
    print(f"  Username : {config['username']}")
    print(f"  Password : {config['password']}")
    print(f"  Port     : {config['port']}")
    print(f"  Base dir : {config['base_dir']}")
    print(f"  Host key : {key_path.resolve()}")
    print(f"  Key type : {host_key.get_name()}")

    server_socket = create_listening_socket(config["port"])

    try:
        print(f"[+] Listening on 0.0.0.0:{config['port']}")
        client_socket, client_address = server_socket.accept()

        try:
            print(f"[+] Connection received from {client_address}")
            handle_client_connection(client_socket, config, host_key)
        finally:
            client_socket.close()
    finally:
        server_socket.close()