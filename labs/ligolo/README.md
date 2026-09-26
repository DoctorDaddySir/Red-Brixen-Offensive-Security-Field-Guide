# Ligolo 0.9.2 isolated routing lab

Topology: operator/proxy on an internal front network; agent attached to front and back networks; HTTP target attached only to the internal back network. Only the proxy container receives NET_ADMIN and TUN device access. No host routes or interfaces are changed, and no container ports are published.

The fixture checks the official Linux amd64 archives and extracted binaries before execution. Use an ordinary Docker-capable account with Python 3 and pexpect 4.9 installed. Build the optional lab image using the included Dockerfile, or supply a local Linux image containing Python 3, curl, OpenSSL and iproute2. Its actual image ID is recorded in the result.

## Copy and run

From the repository root:

```bash
LIGOLO_DIR="$(mktemp -d /tmp/rb-ligolo-download.XXXXXX)"
gh release download v0.9.2 --repo nicocha30/ligolo-ng \
  --pattern ligolo-ng_0.9.2_checksums.txt \
  --pattern ligolo-ng_agent_0.9.2_linux_amd64.tar.gz \
  --pattern ligolo-ng_proxy_0.9.2_linux_amd64.tar.gz \
  --dir "$LIGOLO_DIR"
(
  cd "$LIGOLO_DIR" || exit 1
  sha256sum --check --ignore-missing ligolo-ng_0.9.2_checksums.txt || exit 1
  tar -xzf ligolo-ng_agent_0.9.2_linux_amd64.tar.gz agent
  tar -xzf ligolo-ng_proxy_0.9.2_linux_amd64.tar.gz proxy
)
docker build -t red-brixen-ligolo-lab:local labs/ligolo
python3 labs/ligolo/verify.py --binaries "$LIGOLO_DIR" \
  --image red-brixen-ligolo-lab:local --output /tmp/red-brixen-ligolo-result.json
```

The download and Docker build require network access. Test networks themselves are internal. Image construction is an alternative preparation path; use the recorded image ID and versions to understand the verified environment, rather than assuming that a future package build is identical.

Review [result.json](result.json) for the actual run and [the executable fixture](verify.py) for exact invocations. The fixture creates uniquely named resources, runs positive and negative checks, removes the test route/interface, and destroys its containers/networks in a finally block. Interrupted execution or a Docker failure can require removal of the specific `rb-ligolo-<run-id>` resources; do not prune unrelated Docker resources.

## Assertions

1. The agent can reach the synthetic HTTP target.
2. The proxy cannot reach it before the tunnel.
3. The agent joins using the certificate's SHA-256 fingerprint.
4. The proxy retrieves the exact proof through a /32 route and the running tunnel.
5. Stopping the tunnel prevents that request while the agent's direct request still succeeds.
6. The created route/interface and every fixture container/network are removed.

A failure raises an error and does not produce a success record. The script never follows the guide against a real network.

## Limits

Linux amd64, single-hop routed TCP only. DNS resolution, UDP, Windows agents/proxies, listeners and multi-hop paths require separate verification. The guide marks these pending. The certificate is a one-day test certificate created in the proxy container, not a production certificate. The HTTP proof is synthetic.
