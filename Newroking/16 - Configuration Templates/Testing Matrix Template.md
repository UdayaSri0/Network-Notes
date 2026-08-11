---
title: "Testing Matrix Template"
category: "Configuration Templates"
difficulty: "Mixed"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[Lab 29 - Complete Enterprise Network]]"
  - "[[Network Troubleshooting Methodology]]"
tags:
  - networking
  - testing
  - configuration-template
type: "template"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# Testing Matrix Template

> [!abstract]
> Record the source, destination, expected result, actual result, and evidence for every important service and failure path.

| Test | Source | Destination | Expected | Actual | Evidence |
|---|---|---|---|---|---|
| Local gateway | PC1 | VLAN gateway | Success | | |
| Inter-VLAN | VLAN10 PC | VLAN20 PC | Success or policy deny | | |
| DHCP | Client | DHCP server | Correct lease | | |
| DNS | Client | Server name | Resolves | | |
| NTP | Router | NTP server | Synchronized | | |
| Syslog | Device | Syslog server | Message received | | |
| SNMP | Manager | Agent | OID returned | | |
| Routing | Branch LAN | Data-center LAN | Success | | |
| Internet | Inside PC | ISP test server | Success through PAT | | |
| HSRP failover | Client | Virtual gateway | Recovers | | |
| STP failover | PC1 | PC2 | Recovers | | |

## Acceptance Rule

Do not mark a service complete from configuration alone. Record protocol state and an end-to-end result.
