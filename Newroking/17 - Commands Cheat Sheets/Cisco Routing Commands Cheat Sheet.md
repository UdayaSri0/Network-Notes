---
title: "Cisco Routing Commands Cheat Sheet"
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

# Cisco Routing Commands Cheat Sheet

> [!abstract]
> Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

| Command or value | Purpose |
|---|---|
| `ip route <NET> <MASK> <NEXT-HOP>` | Create an IPv4 static route |
| `router rip` | Enter RIP configuration |
| `router ospf <PID>` | Start an OSPF process |
| `router eigrp <AS>` | Start classic EIGRP |
| `show ip route` | Verify installed routes |
| `show ip ospf neighbor` | Verify OSPF adjacencies |
| `show ip eigrp neighbors` | Verify EIGRP neighbors |
| `traceroute <IP>` | Display routed hop path |

## Use Safely

- Start with read-only `show`, ping, or lookup commands.
- Record the expected result before changing configuration.
- Do not copy placeholders or example credentials into production.

## Related Notes

- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
