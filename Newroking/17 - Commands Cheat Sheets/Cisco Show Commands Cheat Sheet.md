---
title: "Cisco Show Commands Cheat Sheet"
category: "Commands Cheat Sheets"
difficulty: "Beginner"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[Cisco Troubleshooting Commands]]"
  - "[[Networking Dashboard]]"
tags:
  - networking
  - cheat-sheet
  - teaching
type: "cheat-sheet"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# Cisco Show Commands Cheat Sheet

> [!abstract]
> Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

| Command or value | Purpose |
|---|---|
| `show ip interface brief` | Compact Layer 3 interface state and addresses |
| `show interfaces status` | Switch port status, VLAN, duplex, and speed |
| `show vlan brief` | VLAN database and access-port membership |
| `show interfaces trunk` | Operational trunks and carried VLANs |
| `show spanning-tree vlan <ID>` | Root, roles, state, cost, and priority |
| `show etherchannel summary` | Bundle protocol and member flags |
| `show ip route` | IPv4 routing table |
| `show ip protocols` | Dynamic routing process settings |
| `show cdp neighbors detail` | Direct Cisco neighbor details |
| `show logging` | Logging destinations and buffered events |

## Use Safely

- Start with read-only `show`, ping, or lookup commands.
- Record the expected result before changing configuration.
- Do not copy placeholders or example credentials into production.

## Related Notes

- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
