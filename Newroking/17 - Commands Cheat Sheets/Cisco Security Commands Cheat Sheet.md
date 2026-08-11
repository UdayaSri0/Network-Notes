---
title: "Cisco Security Commands Cheat Sheet"
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

# Cisco Security Commands Cheat Sheet

> [!abstract]
> Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

| Command or value | Purpose |
|---|---|
| `username <USER> privilege 15 secret <SECRET>` | Create protected local administrator |
| `transport input ssh` | Allow SSH on VTY lines |
| `show access-lists` | Inspect ACL entries and counters |
| `show port-security` | Inspect switch port security |
| `show ip dhcp snooping` | Inspect snooping state |
| `show ip arp inspection` | Inspect DAI state |
| `show ip nat translations` | Inspect NAT/PAT state |

## Use Safely

- Start with read-only `show`, ping, or lookup commands.
- Record the expected result before changing configuration.
- Do not copy placeholders or example credentials into production.

## Related Notes

- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
