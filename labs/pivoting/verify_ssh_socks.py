#!/usr/bin/env python3
"""Exercise SSH local/dynamic forwarding and ProxyChains against loopback only."""
from __future__ import annotations
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import pwd
import shutil
import socket
import subprocess
import tempfile
import threading
import time


def run(args, **kwargs):
    result = subprocess.run(args, capture_output=True, text=True, timeout=15, **kwargs)
    if result.returncode:
        raise RuntimeError(f'{Path(args[0]).name} failed: {result.stderr.strip()}')
    return result.stdout


def port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def wait_port(number, process):
    for _ in range(100):
        if process.poll() is not None:
            raise RuntimeError('SSH process exited before listener became ready')
        try:
            with socket.create_connection(('127.0.0.1', number), timeout=.1):
                return
        except OSError:
            time.sleep(.05)
    raise RuntimeError('Listener startup timed out')


def stop(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write sanitized JSON result')
    args = parser.parse_args()
    binaries = {name: shutil.which(name) for name in ('ssh', 'sshd', 'ssh-keygen', 'curl', 'proxychains4')}
    missing = [name for name, binary in binaries.items() if not binary]
    if missing:
        raise SystemExit('Missing prerequisites: ' + ', '.join(missing))
    if os.geteuid() == 0:
        raise SystemExit('Run as an ordinary local user, not root.')
    if not Path('/run/sshd').is_dir():
        raise SystemExit('/run/sshd is missing; ask the host administrator to configure OpenSSH prerequisites.')
    processes = []
    checks = []
    with tempfile.TemporaryDirectory(prefix='rb-pivot-') as tmp:
        base = Path(tmp)
        server = None
        logs = []
        try:
            web = base / 'web'
            web.mkdir()
            (web / 'proof.txt').write_text('red-brixen-loopback-proof\n')
            server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(web)))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            web_port = server.server_port
            for name in ('host', 'client'):
                run([binaries['ssh-keygen'], '-q', '-t', 'ed25519', '-N', '', '-f', str(base / name)])
            ssh_port = port()
            config = base / 'sshd_config'
            config.write_text(f'''Port {ssh_port}
ListenAddress 127.0.0.1
HostKey {base}/host
PidFile {base}/sshd.pid
AuthorizedKeysFile {base}/client.pub
StrictModes no
# Lab-only: temporary directory is private but its /tmp ancestor is shared.
PasswordAuthentication no
KbdInteractiveAuthentication no
UsePAM no
AllowUsers {pwd.getpwuid(os.getuid()).pw_name}
AllowTcpForwarding yes
PermitOpen 127.0.0.1:{web_port}
PermitTTY no
X11Forwarding no
LogLevel VERBOSE
''')
            pub = (base / 'host.pub').read_text().split()
            known = base / 'known_hosts'
            known.write_text(f'[127.0.0.1]:{ssh_port} {pub[0]} {pub[1]}\n')
            log = open(base / 'sshd.log', 'w+'); logs.append(log)
            daemon = subprocess.Popen([binaries['sshd'], '-D', '-e', '-f', str(config)], stdout=log, stderr=log)
            processes.append(daemon)
            wait_port(ssh_port, daemon)
            local_port, socks_port = port(), port()
            common = [binaries['ssh'], '-F', '/dev/null', '-i', str(base / 'client'), '-p', str(ssh_port),
                      '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
                      '-o', f'UserKnownHostsFile={known}', '-o', 'ExitOnForwardFailure=yes']
            target = f'{pwd.getpwuid(os.getuid()).pw_name}@127.0.0.1'
            log2 = open(base / 'ssh.log', 'w+'); logs.append(log2)
            tunnel = subprocess.Popen(common + ['-N', '-L', f'127.0.0.1:{local_port}:127.0.0.1:{web_port}',
                                                  '-D', f'127.0.0.1:{socks_port}', target], stdout=log2, stderr=log2)
            processes.append(tunnel)
            wait_port(local_port, tunnel)
            wait_port(socks_port, tunnel)
            curl = [binaries['curl'], '--silent', '--show-error', '--fail', '--connect-timeout', '2', '--max-time', '5']
            env = {key: value for key, value in os.environ.items() if key.lower() not in ('http_proxy','https_proxy','all_proxy','no_proxy')}
            expected = 'red-brixen-loopback-proof\n'
            assert run(curl + ['--noproxy', '*', f'http://127.0.0.1:{local_port}/proof.txt'], env=env) == expected
            checks.append('SSH local forward returns exact proof')
            assert run(curl + ['--socks5-hostname', f'127.0.0.1:{socks_port}', f'http://127.0.0.1:{web_port}/proof.txt'], env=env) == expected
            checks.append('SSH SOCKS5 forward returns exact proof')
            proxy = base / 'proxychains.conf'
            proxy.write_text(f'strict_chain\nproxy_dns\ntcp_read_time_out 5000\ntcp_connect_time_out 2000\n[ProxyList]\nsocks5 127.0.0.1 {socks_port}\n')
            proxied = [binaries['proxychains4'], '-f', str(proxy)] + curl + [f'http://127.0.0.1:{web_port}/proof.txt']
            result = subprocess.run(proxied, env=env, capture_output=True, text=True, timeout=15)
            assert result.returncode == 0 and result.stdout == expected, result.stderr
            assert f'127.0.0.1:{socks_port}' in result.stderr and 'OK' in result.stderr, result.stderr
            checks.append('ProxyChains TCP request returns proof with proxy diagnostics')
            stop(tunnel)
            result = subprocess.run(proxied, env=env, capture_output=True, text=True, timeout=15)
            assert result.returncode != 0 and expected.strip() not in result.stdout
            checks.append('Stopped SOCKS tunnel causes ProxyChains request to fail')
            # Direct target remains live, proving the failure was not an HTTP server shutdown.
            assert run(curl + ['--noproxy', '*', f'http://127.0.0.1:{web_port}/proof.txt'], env=env) == expected
            checks.append('Direct loopback control remains live after tunnel stop')
            for number in (local_port, socks_port):
                with socket.socket() as sock:
                    assert sock.connect_ex(('127.0.0.1', number)) != 0
            checks.append('Both tunnel listeners closed')
        except Exception:
            for log in logs:
                log.flush(); log.seek(0)
                print(log.read())
            raise
        finally:
            for process in reversed(processes):
                stop(process)
            if server:
                server.shutdown(); server.server_close()
            for log in logs:
                log.close()
    checks.append('Temporary keys, configs, HTTP server and SSH daemon cleaned up')
    versions = {}
    for name, command in [('ssh', [binaries['ssh'], '-V']), ('curl', [binaries['curl'], '--version']),
                          ('proxychains', ['dpkg-query', '-W', '-f=${Version}', 'proxychains4'])]:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        versions[name] = (result.stdout or result.stderr).strip().splitlines()[0]
    report = {'date_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'platform': os.uname().sysname,
              'versions': versions, 'checks': checks, 'scope': 'loopback TCP only; no remote routing, DNS, Windows or Ligolo claim'}
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
