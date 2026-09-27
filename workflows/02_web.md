# 02 — Web enumeration

Purpose: map an approved application's behavior and select a specific test based on observations. Use the [scope checklist](../methodology/scope-and-cleanup.md), including origins, paths, roles, request limits and actions that change data. No RB tool is required.

## 1. Capture one response

Operator Bash with curl; choose a GET endpoint that is approved for inspection and paths in your own protected evidence folder:

```bash
read -r -p 'Approved application URL: ' APP_URL
read -r -p 'Response-header output file: ' HEADER_FILE
read -r -p 'Response-body output file: ' BODY_FILE
curl --version
curl --proto '=http,https' --max-time 10 --dump-header "$HEADER_FILE" \
  --output "$BODY_FILE" -- "$APP_URL"
```

The files contain the response headers/body. Review status, content, links, redirects, cookies and technology clues. The command does not follow redirects automatically; verify a destination remains in scope before requesting it. Protect cookies and tokens in captured responses. HTTPS validation stays enabled.

A 200 status can be a login page or soft error. A 401/403 is an access-control response, not proof the application is unavailable. A banner is a technology clue, not a confirmed vulnerable version.

## 2. Browse the authorized functionality

Using the appropriate test account, identify endpoints, inputs, uploads, role boundaries and state-changing operations. Record normal request/response behavior first. Compare only the roles/accounts within scope. Avoid actions such as payment, deletion or password reset unless they are part of the approved test.

## 3. Discover content when permitted

Choose a short, relevant wordlist and an approved maximum request rate. Run from operator Bash with ffuf:

```bash
read -r -p 'Approved base URL: ' BASE_URL
read -r -p 'Path to approved small wordlist: ' WORDLIST
read -r -p 'Agreed requests/second: ' REQUEST_RATE
read -r -p 'Discovery JSON output file: ' DISCOVERY_OUTPUT
ffuf -u "${BASE_URL%/}/FUZZ" -w "$WORDLIST" -rate "$REQUEST_RATE" \
  -t 1 -mc all -noninteractive -of json -o "$DISCOVERY_OUTPUT"
```

The result is a list of responses, not findings. Compare a known valid path with a nonexistent path before filtering. Inspect lengths, status and content; do not discard all 403 responses or accept every 200 as a discovery. ffuf does not follow redirects by default; keep cross-origin follow-up manual and scoped. Virtual-host discovery needs a separately approved hostname set; a discovered name does not automatically extend scope. See the [ffuf documentation](https://github.com/ffuf/ffuf).

## 4. Choose a specific validation

| Observation | Next decision |
| --- | --- |
| Login or session handling | Baseline authentication behavior, role and attempt limits |
| Object IDs or role-specific actions | Compare authorized versus unauthorized access with agreed accounts |
| Upload functionality | Establish allowed content/storage first; agree any execution test separately |
| Unexpected input behavior | Reproduce minimally and distinguish application logic from infrastructure errors |
| Sensitive file or data | Capture minimum evidence; stop collecting when the impact is established |

A web shell, brute-force attempt, or broad injection pass is not a mandatory next step. The tester selects a test that answers an identified question within scope.

## 5. Evidence, remediation and cleanup

Record URL, account/role, request, UTC time, response, actual result and limitations. Redact session/authentication values from client copies. Explain the failed control and specific corrective action; do not use a scanner label as the whole finding.

Remove test uploads/accounts or data changes you introduced and verify legitimate behavior. Preserve logs. Retest the same boundary after the agreed fix.

Verification: curl response capture and a two-path ffuf check are exercised against a local HTTP fixture in [the RB-007 record](../methodology/rb-007-verification.md). This does not validate authentication, business logic, TLS configuration or upload exploitation against a real application.
