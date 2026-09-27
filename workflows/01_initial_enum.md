# 01 — Initial enumeration

Purpose: identify services on approved targets and decide which reference to use next. Follow the [scope checklist](../methodology/scope-and-cleanup.md) and record the tested tool version. No RB workspace is required.

## 1. Choose the initial scan

Run in the operator's Bash shell. Set one approved IPv4 address, an explicit port list, an agreed maximum packet rate and an output prefix in your own evidence folder:

```bash
read -r -p 'Approved IPv4 address: ' TARGET
read -r -p 'Approved TCP ports, such as 22,80,443: ' PORTS
read -r -p 'Agreed maximum packets/second: ' MAX_RATE
read -r -p 'Output prefix in an existing evidence directory: ' SCAN_OUTPUT
nmap --version
nmap -sT -Pn -n -p "$PORTS" --max-rate "$MAX_RATE" -oA "$SCAN_OUTPUT" "$TARGET"
```

`-sT` uses TCP connections, `-Pn` skips discovery for this known target, and `-n` avoids name lookups. The rate is a ceiling, not a guarantee of harmlessness. Stop if the target shows unexpected degradation. Do not apply a fast minimum rate to every environment.

Expected: a port-state table plus three output files. `open` establishes a connection result; `closed` and `filtered` require different interpretation. A port number alone does not establish the actual service or a vulnerability. See [Nmap timing guidance](https://nmap.org/book/man-performance.html).

## 2. Identify observed services

Set the ports actually observed open and choose a new output prefix:

```bash
read -r -p 'Observed open ports approved for version probing: ' OPEN_PORTS
read -r -p 'New service-scan output prefix: ' SERVICE_OUTPUT
nmap -sT -Pn -n -sV --version-light -p "$OPEN_PORTS" \
  --max-rate "$MAX_RATE" -oA "$SERVICE_OUTPUT" "$TARGET"
```

The scan-rate setting is not a global application-request limit for version detection. Version probing sends application data; confirm that it fits the approved method. Record uncertain service matches as hypotheses. Add script checks individually after reviewing their behavior; default script sets are not a mandatory first step.

## 3. Expand only when needed

A full TCP range, UDP checks, IPv6, or host discovery can reveal additional coverage, but each has its own scope, privileges and traffic characteristics. Record untested protocols rather than silently treating them as absent. Do not treat the limited initial scan as complete coverage.

## 4. Choose the next reference

| Observation | Next reference |
| --- | --- |
| HTTP/HTTPS service | [Web](02_web.md) |
| SMB service | [SMB](03_smb.md) |
| Directory/domain services | [AD planning](../active-directory/00_ad_start_here.md) |
| Other service | [Enumeration index](../enumeration/README.md) |

Preserve target, time, identity/vantage point, command, tool version and output. Scan results are observations; validate any proposed finding. A connect scan creates connections/log entries but does not authorize configuration changes or file collection.

Verification: command syntax and a bounded loopback TCP scan are checked in [the RB-007 record](../methodology/rb-007-verification.md). Real target behavior, UDP and IPv6 are outside that record.
