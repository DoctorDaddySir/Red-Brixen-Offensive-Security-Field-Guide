# Verified SSH, SOCKS and ProxyChains commands

The [recorded run](ssh-socks-result.json) passed on Linux using OpenSSH 10.4p1, curl 8.21.0, and ProxyChains 4.17. The [executable lab](verify_ssh_socks.py) is the exact source of the test commands and assertions.

## Copy and run the complete local lab

From the repository root, as an ordinary user on Debian/Kali Linux:

```bash
python3 labs/pivoting/verify_ssh_socks.py --output /tmp/red-brixen-ssh-socks-result.json
```

Prerequisites: Python 3, OpenSSH client/server, curl, ProxyChains 4, dpkg-query, and permission to create loopback listeners. The host's `/run/sshd` prerequisite must already exist. No external destination is contacted. The script creates private temporary keys, a local-only SSH daemon, and a local HTTP proof file; it does not modify the host SSH service.

The temporary server disables StrictModes only for its private temporary authorized-key path under `/tmp`. Password authentication is disabled, the server binds loopback, and forwarding is restricted to the lab HTTP endpoint. Do not copy this temporary daemon configuration into a production service.

A successful run prints JSON with seven checks: local forward, SOCKS5, ProxyChains proof response, stopped-proxy failure, live direct control, closed tunnel listeners, and cleanup. A failed assertion exits unsuccessfully and includes diagnostics. Temporary resources are removed even on ordinary exceptions; forced process termination can require manual cleanup.

## Copyable operator commands

These use the same forwarding/request options exercised by the lab. Set the variables to your approved environment first. The local daemon setup and ephemeral credentials are handled automatically in the complete lab above.

```bash
read -r -p 'Approved pivot SSH destination (user@host): ' PIVOT
read -r -p 'Approved internal destination IP: ' DESTINATION
read -r -p 'Destination TCP port: ' DESTINATION_PORT
LOCAL_PORT=18443
SOCKS_PORT=11080
ssh -N -o ExitOnForwardFailure=yes \
  -L "127.0.0.1:${LOCAL_PORT}:${DESTINATION}:${DESTINATION_PORT}" \
  -D "127.0.0.1:${SOCKS_PORT}" "$PIVOT"
```

Run from the operator's Bash terminal; keep it open, use your approved SSH authentication, and validate the host key. Remote environments are not covered by the loopback result. In a second terminal, define the same variables before issuing requests. For an HTTP endpoint (the local lab protocol):

```bash
LOCAL_PORT=18443
curl --noproxy '*' --silent --show-error --fail \
  --connect-timeout 2 --max-time 5 "http://127.0.0.1:${LOCAL_PORT}/proof.txt"
```

Expect the agreed test content, not merely a zero exit code. HTTPS requires the correct application hostname/SNI and trusted certificate, and needs separate verification.

To use ProxyChains, create an engagement-local configuration:

```bash
cat > proxychains-lab.conf <<'CONFIG'
strict_chain
proxy_dns
tcp_read_time_out 5000
tcp_connect_time_out 2000
[ProxyList]
socks5 127.0.0.1 11080
CONFIG
read -r -p 'Approved HTTP proof URL: ' PROOF_URL
env -u http_proxy -u https_proxy -u all_proxy -u no_proxy \
  -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u NO_PROXY \
  proxychains4 -f ./proxychains-lab.conf curl --silent --show-error --fail \
  --connect-timeout 2 --max-time 5 "$PROOF_URL"
```

The lab exercises this configuration with its selected port and a numeric loopback destination. Confirm proxy diagnostics name the intended proxy and the response matches the expected proof. In the disposable lab, repeat after closing the SSH process: the proxy request must fail while the direct control remains live. Stop only the SSH process you created; preserve any evidence needed before deleting the temporary configuration.

## Limits

This is a smoke test of compatible TCP application forwarding. It does not establish network isolation, remote reachability, hostname resolution, UDP/ICMP, Nmap compatibility, or Ligolo correctness. A normal configured environment can differ from the clean local fixture.
