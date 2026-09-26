# 07 — Pivoting and tunneling workflow

Purpose: establish and verify an approved path to an in-scope internal service through an authorized pivot host.

Status: reference-reviewed 2026-09-25; multi-host lab validation pending. Record client/server versions and the network layout used for each engagement.

## 1. Map the intended path

Record operator → pivot → destination, including IPs, destination ports, identity, route direction, DNS resolution location, and scope. Access to a pivot does not establish authorization for every reachable network.

Capture current routes and listeners before changing them. Identify overlapping VPN/internal ranges and existing forwards. Select one known in-scope service for the connectivity check; do not begin with a subnet-wide scan.

## 2. Select a transport

| Need | Method | Important limit |
| --- | --- | --- |
| One TCP service | [SSH local forwarding](../pivoting/ssh_tunnel.md) | Forward is specific to the selected destination/port |
| Several TCP destinations with proxy-aware tools | SSH dynamic forwarding or [Chisel](../pivoting/chisel.md), optionally [ProxyChains](../pivoting/proxychains.md) | Application and DNS behavior must be verified |
| Routed access for supported protocols | [Ligolo](../pivoting/ligolo.md) | Route scope, interface state, privileges, and protocol support depend on the setup |

Use the tool's documented authentication and certificate verification. Bind operator-side listeners to loopback unless other access is explicitly needed. Record why the chosen method fits the test.

## 3. Establish a narrow forward

For an SSH-capable pivot, run from the operator's shell, replacing all uppercase example values:

```bash
ssh -N -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:8443:INTERNAL_HOST:443 USER@PIVOT_HOST
```

Keep this foreground session open. The destination is reached from the SSH server. A successful listener startup does not prove the destination service is reachable; validate the application next. Confirm the SSH host key against the engagement's trusted record. See the [OpenSSH client manual](https://man.openbsd.org/ssh).

For HTTPS, preserve the application's hostname and TLS identity when using the local listener. Do not treat a certificate or virtual-host mismatch as proof the tunnel failed. A browser or proxy may need explicit routing configuration.

## 4. Verify routing before testing

1. Confirm the local listener or tunnel interface exists.
2. Make one connection to the approved service and record the response.
3. Check pivot/server logs or lab packet capture to establish where traffic actually traveled.
4. Check DNS separately if using hostnames.
5. In a disposable lab, stop the tunnel and repeat the same request. It should fail when no direct path exists; an unexpected success suggests bypass or an alternate route.

ProxyChains supports TCP connections from compatible dynamically linked applications; it is not an IP VPN. ICMP ping and UDP scans do not establish its functionality. For a compatible Nmap setup, use a bounded TCP connect scan and disable discovery and name lookup; verify routing in the lab before relying on it. See [ProxyChains limitations](https://github.com/rofl0r/proxychains-ng) and [Nmap scan techniques](https://nmap.org/book/man-port-scanning-techniques.html).

## 5. Diagnose one layer at a time

| Symptom | Check |
| --- | --- |
| Local connection refused | Listener binding, port collision, tunnel process |
| Listener works but destination times out | Pivot-to-target reachability, firewall, approved destination/port |
| IP works but hostname fails | Resolver location, split DNS, proxy DNS support |
| Wrong page or TLS error | Host header/SNI, expected certificate identity |
| Only some applications work | Proxy support, preload compatibility, direct socket behavior |
| Route disrupts existing access | Overlapping networks and route specificity; restore the recorded original route |

Do not increase scan scope or disable verification merely to work around an unexplained failure.

## 6. Capture evidence and close the path

Record the diagram, scope decision, tool/version, sanitized setup command, connection result, time, and limitations. Associate findings with the destination asset and relevant trust boundary, not just the pivot host.

Stop only the tunnel process created for this test. Remove its temporary agents, listeners, interfaces, and routes; preserve original routes and logs. Verify the test listener is closed and the original network configuration is restored. Use the [finding template](../exploited-vulns/_TEMPLATE/finding_template.md) for demonstrated segmentation issues, including a retest from the same source position.

## Validation still required

Exercise SSH single-port forwarding, a SOCKS path, and a routed path in an isolated multi-host lab. Record positive connectivity, stopped-tunnel behavior, DNS behavior, excluded destinations, and cleanup. Keep protocol limitations explicit in the verification record.
