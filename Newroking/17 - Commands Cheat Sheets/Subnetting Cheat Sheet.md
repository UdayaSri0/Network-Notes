---
title: "Subnetting Cheat Sheet"
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

# Subnetting Cheat Sheet

> [!abstract]
> Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

| Command or value | Purpose |
|---|---|
| `/8 255.0.0.0` | 16,777,216 addresses |
| `/16 255.255.0.0` | 65,536 addresses |
| `/23 255.255.254.0` | 512 addresses, 510 traditional usable hosts |
| `/24 255.255.255.0` | 256 addresses, 254 usable |
| `/25 255.255.255.128` | 128 addresses, 126 usable |
| `/26 255.255.255.192` | 64 addresses, 62 usable |
| `/27 255.255.255.224` | 32 addresses, 30 usable |
| `/28 255.255.255.240` | 16 addresses, 14 usable |
| `/29 255.255.255.248` | 8 addresses, 6 usable |
| `/30 255.255.255.252` | 4 addresses, 2 usable |

## Use Safely

- Start with read-only `show`, ping, or lookup commands.
- Record the expected result before changing configuration.
- Do not copy placeholders or example credentials into production.

## Related Notes

- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
