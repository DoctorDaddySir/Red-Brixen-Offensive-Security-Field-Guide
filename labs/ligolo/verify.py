#!/usr/bin/env python3
"""Isolated Docker Ligolo 0.9.2 routed TCP lab; no host routes changed."""
import argparse
import hashlib
import json
import re
import subprocess
import time
import uuid
from pathlib import Path
import pexpect


def docker(*args, check=True):
    r = subprocess.run(['docker', *args], text=True, capture_output=True, timeout=40)
    if check and r.returncode:
        raise RuntimeError(r.stderr or r.stdout)
    return r


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--binaries', type=Path, required=True)
    p.add_argument('--image', default='red-brixen-ligolo-lab:local')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    expected = {'agent': '714534917a4a58812669619667cc57dfad03d34d0de5b0d7c468d76819f84111',
                'proxy': '6c683c403502d366276595197749e620c975908dae7314c21079ec8ebee4e5d0'}
    # Verify the release archives and extracted binaries; do not trust unrelated executables.
    import tarfile
    for role, digest in expected.items():
        archive = args.binaries / f'ligolo-ng_{role}_0.9.2_linux_amd64.tar.gz'
        if hashlib.sha256(archive.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'{role}: archive checksum mismatch')
        with tarfile.open(archive) as stream:
            member = next(m for m in stream.getmembers() if Path(m.name).name == role)
            if stream.extractfile(member).read() != (args.binaries / role).read_bytes():
                raise RuntimeError(f'{role}: binary differs from verified archive')
    ident = 'rb-ligolo-' + uuid.uuid4().hex[:8]
    front, back = ident + '-front', ident + '-back'
    proxy, agent, target = [ident + '-' + name for name in ('proxy', 'agent', 'target')]
    networks, containers = [], []
    cli = None
    checks = []
    console = []
    try:
        image_id = docker('image', 'inspect', '--format', '{{.Id}}', args.image).stdout.strip()
        for net in (front, back):
            docker('network', 'create', '--internal', net); networks.append(net)
        for name, net in ((proxy, front), (agent, front), (target, back)):
            options = ['run', '-d', '--name', name, '--network', net, '--entrypoint', '/bin/sh']
            if name == proxy:
                options += ['--cap-add', 'NET_ADMIN', '--device-cgroup-rule', 'c 10:200 rwm']
            docker(*options, args.image, '-c', 'sleep 600'); containers.append(name)
        docker('network', 'connect', back, agent)
        def address(name, net):
            return docker('inspect', '--format', '{{(index .NetworkSettings.Networks "' + net + '").IPAddress}}', name).stdout.strip()
        proxy_ip, target_ip = address(proxy, front), address(target, back)
        for name, role in ((proxy, 'proxy'), (agent, 'agent')):
            docker('cp', str(args.binaries / role), f'{name}:/tmp/{role}')
        docker('exec', target, 'sh', '-c', 'mkdir -p /tmp/proof && printf "red-brixen-ligolo-proof\\n" > /tmp/proof/proof.txt')
        docker('exec', '-d', target, 'python3', '-m', 'http.server', '8000', '--directory', '/tmp/proof')
        url = f'http://{target_ip}:8000/proof.txt'
        curl = ['curl', '--noproxy', '*', '--silent', '--show-error', '--fail', '--connect-timeout', '2', '--max-time', '4', url]
        # Agent must reach the target before any tunneling claim.
        for _ in range(20):
            response = docker('exec', agent, *curl, check=False)
            if response.returncode == 0: break
            time.sleep(.1)
        if response.stdout != 'red-brixen-ligolo-proof\n': raise RuntimeError('Agent cannot reach synthetic target')
        checks.append('Agent reaches target on the isolated back network')
        if docker('exec', proxy, *curl, check=False).returncode == 0:
            raise RuntimeError('Isolation precondition failed: proxy can reach target directly')
        checks.append('Proxy direct access fails before tunnel creation')
        docker('exec', proxy, 'sh', '-c', 'mkdir -p /dev/net && mknod /dev/net/tun c 10 200 && ip tuntap add dev rbligolo mode tun && ip link set rbligolo up')
        docker('exec', proxy, 'openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', '/tmp/key.pem', '-out', '/tmp/cert.pem', '-days', '1', '-subj', '/CN=rb-ligolo-lab')
        fingerprint = docker('exec', proxy, 'openssl', 'x509', '-in', '/tmp/cert.pem', '-noout', '-fingerprint', '-sha256').stdout.strip().split('=')[1].replace(':', '')
        docker('exec', proxy, 'sh', '-c', "printf 'web:\n  enabled: false\n' > /tmp/ligolo.yaml")
        cli = pexpect.spawn('docker', ['exec', '-it', proxy, '/tmp/proxy', '-config', '/tmp/ligolo.yaml', '-nobanner', '-certfile', '/tmp/cert.pem', '-keyfile', '/tmp/key.pem', '-laddr', '0.0.0.0:11601'], encoding='utf-8', timeout=20)
        cli.expect('»')
        console.append(cli.before)
        docker('exec', '-d', agent, '/tmp/agent', '-connect', proxy_ip + ':11601', '-accept-fingerprint', fingerprint)
        cli.expect('Agent joined')
        checks.append('Agent joins proxy using the pinned certificate fingerprint')
        cli.sendline('session')
        cli.expect('Specify a session')
        time.sleep(.2)
        cli.send('\r')
        cli.expect('»')
        cli.sendline('tunnel_start --tun rbligolo')
        cli.expect('Starting tunnel')
        console.append(cli.before)
        docker('exec', proxy, 'ip', 'route', 'add', target_ip + '/32', 'dev', 'rbligolo')
        for _ in range(10):
            response = docker('exec', proxy, *curl, check=False)
            if response.stdout == 'red-brixen-ligolo-proof\n': break
            time.sleep(.2)
        if response.stdout != 'red-brixen-ligolo-proof\n': raise RuntimeError('Routed proof failed: ' + response.stderr)
        checks.append('Proxy receives exact HTTP proof through Ligolo and a /32 route')
        cli.sendline('tunnel_stop')
        time.sleep(1)
        if docker('exec', proxy, *curl, check=False).returncode == 0: raise RuntimeError('Stopped tunnel still reaches target')
        checks.append('Stopped tunnel prevents proxy access')
        if docker('exec', agent, *curl).stdout != 'red-brixen-ligolo-proof\n': raise RuntimeError('Target control unavailable')
        checks.append('Agent direct control remains reachable after tunnel stop')
        docker('exec', proxy, 'ip', 'route', 'del', target_ip + '/32', 'dev', 'rbligolo')
        docker('exec', proxy, 'ip', 'link', 'delete', 'rbligolo')
        if docker('exec', proxy, 'ip', 'link', 'show', 'rbligolo', check=False).returncode == 0: raise RuntimeError('Interface cleanup failed')
        checks.append('Created route and TUN interface removed')
    except Exception:
        if cli:
            print('Console tail:', cli.before)
        raise
    finally:
        if cli: cli.close(force=True)
        for name in reversed(containers): docker('rm', '-f', name)
        for name in reversed(networks): docker('network', 'rm', name)
    checks.append('All three temporary containers and both internal networks removed')
    report = {'date_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'release': '0.9.2',
              'archive_sha256': expected, 'image_id': image_id, 'docker_version': docker('version','--format','{{.Server.Version}}').stdout.strip(),
              'checks': checks, 'limits': 'Linux amd64 routed TCP only; Windows, DNS, UDP, double pivots and listeners not validated'}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__': main()
