# Pivoting with ProxyChains-NG

Purpose: send supported TCP application connections through an existing SOCKS proxy. ProxyChains does not create the proxy or a routed interface.

Status: reference-reviewed 2026-09-25 against the upstream README/configuration; isolated network lab execution pending. Record installed versions and the exact application tested.

## Prerequisites and limits

Identify an authorized pivot, destination, and destination port. Confirm the pivot can reach the service and that the operator is allowed to use that path.

ProxyChains intercepts networking calls in compatible dynamically linked applications. It supports TCP, not arbitrary UDP or ICMP. Static binaries and programs with incompatible networking behavior may bypass interception or fail. It is not a universal traffic isolation boundary. Consult the [upstream README](https://github.com/rofl0r/proxychains-ng).

Prefer an application's native SOCKS support when available. Validate actual traffic paths rather than relying solely on a ProxyChains startup message.

## 1. Start a loopback-bound SOCKS listener

Run on the operator host, replacing the account and pivot hostname:

```bash
ssh -N -o ExitOnForwardFailure=yes -D 127.0.0.1:1080 USER@PIVOT_HOST
```

Keep this foreground session running. Verify the SSH host key using the engagement's trusted record. This example uses [OpenSSH dynamic forwarding](https://man.openbsd.org/ssh); Chisel or another approved proxy can serve the same role.

## 2. Use an engagement-local configuration

Create `proxychains.conf` in the engagement workspace:

```text
strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks5 127.0.0.1 1080
```

Use one chain mode and the explicit `-f` option, avoiding accidental use of a system configuration. `proxy_dns` affects supported resolver calls; confirm its behavior with the actual application and resolver environment. See the [upstream configuration comments](https://github.com/rofl0r/proxychains-ng/blob/master/src/proxychains.conf).

## 3. Verify one approved service

For an HTTPS application, replace `INTERNAL_HOST` with its real hostname and preserve normal certificate validation:

```bash
proxychains4 -f ./proxychains.conf curl --connect-timeout 5 --max-time 15 -I https://INTERNAL_HOST/
```

Record the response, time, destination identity, and proxy diagnostics. An HTTP error response can still establish connectivity; it does not establish authorization bypass. A TLS error may indicate a hostname or trust-store issue rather than failed routing.

For an approved numeric target and a bounded port check, a compatible Nmap installation can use:

```bash
proxychains4 -f ./proxychains.conf nmap -sT -Pn -n -p 443 --max-retries 1 TARGET_IP
```

Replace `TARGET_IP` before use. `-sT` selects TCP connect, `-Pn` omits host discovery, and `-n` omits name lookup. Do not substitute SYN/UDP scans or add broad discovery options. Verify this combination in the lab using endpoint logs or packet capture; Nmap compatibility is not guaranteed merely by these flags. See [Nmap scan techniques](https://nmap.org/book/man-port-scanning-techniques.html).

## 4. Diagnose failures

| Result | Next check |
| --- | --- |
| Connection to proxy refused | SSH session and loopback listener/port |
| Proxy works but target times out | Pivot reachability, target service and firewall |
| Numeric IP works but name fails | Resolver path and application compatibility |
| Application works even with proxy stopped | Direct route, cached result, or interception bypass |
| Ping/UDP fails | Unsupported transport; use a suitable approved method |

In an isolated lab without a direct route, stop the proxy and repeat an uncached request. The request should fail. Verify the positive path in target logs as well; failure alone does not prove every prior connection used the proxy.

## 5. Evidence, cleanup, and remediation

Record sanitized commands/configuration, tool versions, operator/pivot/destination diagram, request/result, source observed by the destination, DNS behavior, and negative-control results. Store secrets outside shared command examples.

Stop the specific SSH session and confirm its listener is closed. Remove any temporary test configuration after preserving needed evidence. Do not remove unrelated routes or terminate other operators' sessions.

If the path demonstrates a segmentation issue, report the unintended source-to-destination access and expected policy. Recommend appropriate service authorization and network restrictions, then retest from the same source after remediation. Merely running ProxyChains is not a finding.

## Validation still required

Use an isolated operator/pivot/destination topology to record successful TCP forwarding, hostname behavior, a refused port, a stopped proxy, and cleanup. Record a known incompatible application case if encountered. This page is not yet lab-validated.
