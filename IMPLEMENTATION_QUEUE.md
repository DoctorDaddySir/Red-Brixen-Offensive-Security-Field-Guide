# Implementation queue

Each ticket has its own branch and PR. The owner approves and merges. Status is tracked in GitHub; this table records the initial queue, not completion.

| Ticket | Scope | Branch |
| --- | --- | --- |
| [RB-000](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/1) | Track the completion roadmap and contribution workflow | `ticket/rb-000` |
| [RB-001](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/2) | Correct Windows and pivoting workflows | `ticket/rb-001` |
| [RB-002](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/3) | Replace mislabeled ProxyChains and token privilege guides | `ticket/rb-002` |
| [RB-003](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/4) | Complete or explicitly defer AD placeholders | `ticket/rb-003` |
| [RB-004](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/5) | Prevent sensitive data in default report exports | `ticket/rb-004` |
| [RB-005](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/6) | Add complete finding and evidence data model | `ticket/rb-005` |
| [RB-006](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/7) | Protect credential entry storage and recovery | `ticket/rb-006` |
| [RB-007](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/8) | Make testing and cleanup scope-aware | `ticket/rb-007` |
| [RB-008](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/9) | Repair navigation and canonical indexes | `ticket/rb-008` |
| [RB-009](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/10) | Separate professional and exam reporting templates | `ticket/rb-009` |
| [RB-010](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/11) | Document defensible versioned severity scoring | `ticket/rb-010` |
| [RB-011](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/12) | Refactor RB-OPS and add engagement lifecycle support | `ticket/rb-011` |
| [RB-012](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/13) | Add continuous validation and release acceptance gates | `ticket/rb-012` |

Start with RB-001 and RB-002 content corrections. Prioritize RB-004 report confidentiality before using exports for clients. Define data contracts before RB-005/006/011 and test migrations before merging those changes. RB-012 provides the integration and release gate. The roadmap also includes broader domain expansion that must be decomposed into additional tickets before implementation.
