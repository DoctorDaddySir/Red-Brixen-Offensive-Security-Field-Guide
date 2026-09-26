# Ligolo-ng pivoting — verified Linux TCP workflow

**Lab-validated:** Ligolo-ng 0.9.2, Linux amd64, 2026-09-26. The [verification record](../labs/ligolo/result.json) and [reproducible lab](../labs/ligolo/README.md) show successful routed HTTP, a stopped-tunnel negative control, and cleanup. Commands below use the flags and operations exercised by that fixture; substitute only the documented engagement inputs.

This is a manual field procedure. Run each block in its named terminal, inspect the result, and choose the next step yourself. The automated lab is supporting verification evidence; it is not required to perform this procedure.

Topology: operator/proxy → agent/pivot → approved internal destination. The agent initiates the TLS connection to the proxy. A TUN interface on the operator carries the selected destination traffic; this does not imply authorization for every agent-reachable network.

## 1. Prepare the binaries and scope

Use the official [0.9.2 release](https://github.com/nicocha30/ligolo-ng/releases/tag/v0.9.2), matching each platform/architecture, and verify its checksum file. The tested Linux amd64 archives have these SHA-256 digests:

| Archive | SHA-256 |
| --- | --- |
| `ligolo-ng_agent_0.9.2_linux_amd64.tar.gz` | `714534917a4a58812669619667cc57dfad03d34d0de5b0d7c468d76819f84111` |
| `ligolo-ng_proxy_0.9.2_linux_amd64.tar.gz` | `6c683c403502d366276595197749e620c975908dae7314c21079ec8ebee4e5d0` |

[Download and local-lab commands](../labs/ligolo/README.md) are provided separately. Transfer only the matching agent binary through an approved channel. Verify its provenance on the receiving host.

Record the operator listener address, agent, destination IP and port, existing routes, approved test objective and cleanup owner. Use a single destination /32 for the initial TCP validation. Review overlapping VPN/internal ranges before adding routes.

## 2. Operator Bash: prepare the interface

Use a fresh interface name. These commands require administrative network privileges; the automated lab confines them to its proxy container.

```bash
ip route show
sudo ip tuntap add user "$(id -un)" mode tun rbligolo
sudo ip link set rbligolo up
ip link show rbligolo
```

The `user` option permits the named operator to open the interface; the lab runs as container root and uses the same TUN operation without that ownership option. If the interface already exists, inspect it instead of overwriting or deleting another session's interface.

## 3. Operator Bash: create a test certificate and start the proxy

For the disposable lab or an approved temporary test setup, create a private working directory. The fixture uses this certificate/key method, not disabled TLS verification:

```bash
umask 077
mkdir -p ligolo-session
cd ligolo-session || exit 1
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout key.pem -out cert.pem -days 1 -subj '/CN=rb-ligolo-lab'
printf 'web:\n  enabled: false\n' > ligolo.yaml
openssl x509 -in cert.pem -noout -fingerprint -sha256
read -r -p 'Absolute path to verified proxy binary: ' PROXY_BIN
read -r -p 'Approved operator listen IP: ' LISTEN_IP
"$PROXY_BIN" -config ./ligolo.yaml -certfile ./cert.pem -keyfile ./key.pem \
  -laddr "${LISTEN_IP}:11601"
```

Keep this terminal open. Supply an IP reachable from the agent and restrict access appropriately. The explicit configuration disables the optional WebUI and avoids a first-start prompt. For a longer engagement use its approved certificate/key lifecycle; the one-day key above is a lab example.

Read the SHA-256 fingerprint from the trusted operator terminal and remove the colon separators for the agent input. Do not obtain the expected fingerprint from an untrusted connection to the server.

## 4. Agent Bash: connect with certificate pinning

Run where the agent binary has been transferred:

```bash
read -r -p 'Approved proxy IP: ' PROXY_IP
read -r -p 'Trusted proxy SHA-256 fingerprint (hex, no colons): ' FINGERPRINT
./agent -connect "${PROXY_IP}:11601" -accept-fingerprint "$FINGERPRINT"
```

Expected: the proxy reports `Agent joined`. A rejected fingerprint is a trust/configuration problem; do not bypass it with `-ignore-cert`. Keep the agent foreground process available for controlled shutdown.

## 5. Proxy console: choose the agent and start the tunnel

These are Ligolo console commands, not Bash commands:

```text
session
```

Select the intended agent using the menu and Enter, then:

```text
tunnel_start --tun rbligolo
```

Expected: `Starting tunnel` for that agent. Match its identity to the scope record. The fixture uses exactly this selection and start sequence.

## 6. Second operator Bash terminal: add the narrow route and verify

Use a numeric IPv4 destination reachable from the agent and an HTTP endpoint approved for this assessment. Choose the actual application path; `/proof.txt` is only a fixture used by the accompanying lab. For other protocols, validate with that service’s client instead of inventing an HTTP endpoint:

```bash
read -r -p 'Approved internal IPv4 destination: ' DESTINATION_IP
read -r -p 'Approved HTTP TCP port: ' DESTINATION_PORT
read -r -p 'Approved HTTP path, beginning with /: ' TEST_PATH
sudo ip route add "${DESTINATION_IP}/32" dev rbligolo
ip route get "$DESTINATION_IP"
curl --noproxy '*' --silent --show-error --fail \
  --connect-timeout 2 --max-time 4 \
  "http://${DESTINATION_IP}:${DESTINATION_PORT}${TEST_PATH}"
```

Expected during an assessment: the response from the intended application. Confirm it is the correct service; an HTTP 401/403 is evidence of an authentication boundary, not automatically a failed tunnel (`curl --fail` returns nonzero for these responses). A timeout requires route and reachability checks before further testing. In the supplied lab, `/proof.txt` returns `red-brixen-ligolo-proof`. Before tunneling the same operator request must fail, while the agent's request succeeds. If direct operator access already succeeds, that environment cannot establish the tunnel as the exclusive path. A connection alone does not establish a security finding.

The route deliberately uses /32. Broader prefixes need a separate scope and route review. A ping is not a substitute for testing the application protocol. HTTPS requires correct hostname/SNI and certificate validation.

## 7. Stop, verify the negative control, and clean up

In the proxy console:

```text
tunnel_stop
```

Repeat the operator curl command: it should now fail in the isolated lab, while the agent's direct request remains successful. Then, in the same operator Bash terminal where `DESTINATION_IP` was set:

```bash
sudo ip route del "${DESTINATION_IP}/32" dev rbligolo
sudo ip link delete rbligolo
```

Stop the foreground agent and proxy processes with Ctrl-C. Remove only the transferred agent and temporary certificate/configuration files created for this test, after preserving required evidence. Confirm the original route state, listener closure and artifact removal. The automated fixture also destroys its dedicated containers and networks.

## Troubleshooting and coverage boundaries

| Symptom or feature | Action/status |
| --- | --- |
| Agent cannot connect | Check approved listener address, port and firewall; confirm agent-to-proxy direction |
| Fingerprint rejected | Compare the trusted certificate fingerprint and endpoint; retain TLS verification |
| Tunnel starts but request times out | Check selected agent, /32 route, agent-to-target reachability and target service |
| Interface busy or route already exists | Inspect existing sessions/routes; do not overwrite unrelated state |
| Hostname fails but numeric IP works | DNS path needs separate validation; this record only tests numeric IPv4 |
| UDP/ICMP | Not validated by this lab; do not infer support from the TCP result |
| Windows agent/proxy | Requires architecture-specific binaries and a separate lab record |
| Reverse listeners and double pivots | Planned; use primary references for research, not a verified command claim |

For evidence, retain the selected agent identity, before/after route output, sanitized setup commands, requested destination/path, timestamped application result, and cleanup confirmation. Record unexpected errors and untested protocols as limitations. Do not include the TLS private key or authentication secrets in a client report.

Record versions, topology, sanitized commands, timestamps, destination result, negative control and cleanup with the finding. If the path proves an unintended segmentation boundary crossing, describe the intended policy and observed access, recommend scoped network/service controls, and retest from the same source.

Primary references: [Ligolo quickstart](https://docs.ligolo.ng/Quickstart/), [advanced pivoting](https://docs.ligolo.ng/sample/double/), and the [pinned CLI implementation](https://github.com/nicocha30/ligolo-ng/blob/v0.9.2/cmd/proxy/app/app.go). Actual verification is limited to the linked lab record.
