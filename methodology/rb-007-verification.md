# RB-007 command verification record

Executed 2026-09-27 UTC on Linux. These checks validate specific command behavior; the guides remain manual references and require no fixture or RB binary.

| Command | Installed version | Fixture and observed result |
| --- | --- | --- |
| Nmap TCP connect scan | 7.99 | One temporary loopback HTTP port, maximum scan rate 10: reported open while listening and closed after shutdown; XML output parsed successfully |
| Nmap light service detection | 7.99 | Same port identified as HTTP with `-sV --version-light` |
| curl response capture | 8.21.0 | GET of `known.txt` saved HTTP 200 headers and exact synthetic proof body |
| ffuf content discovery | 2.1.0-dev | Two-word list (`known.txt`, `absent.txt`), rate 2, one worker: JSON contained respective 200 and 404 results |
| GNU grep filename search | 3.12 | Synthetic config file matched; unrelated file excluded; output contained filename and no synthetic secret value |
| Linux context | Local hostname/id utilities | `hostname` and `id` completed and displayed local host and identity |

## Method and cleanup

A Python standard-library HTTP server bound only to `127.0.0.1` on an ephemeral port served a temporary directory. Subprocess checks used the argument lists shown in the corresponding guides, substituting fixture values for prompted inputs. Assertions checked Nmap XML, exact curl body, HTTP status results in ffuf JSON, and filename-only grep output. The listener was stopped before the negative Nmap check. Temporary fixture files were removed on exit. HTTP connection-reset diagnostics during Nmap service probing did not fail the assertions.

These checks exercise the commands, not an engagement process. They do not prove real-network rate compliance, production availability, DNS/IPv6/UDP behavior, TLS security, authentication, exploitation, or Windows behavior. Interactive prompts were not exercised by the subprocess harness; Bash syntax is checked separately. The ffuf result applies to the installed development build, not every release.

## Reference-only and pending checks

SMB commands are reviewed against the Samba manual; authenticated share listing, sample retrieval and restoration need a separate server lab record. Windows `cmdkey /list` and `whoami /all` were not executed. AD restoration instructions are a decision checklist: successful restoration depends on the actual original state and target platform. Do not label these as lab-verified based on this record.
