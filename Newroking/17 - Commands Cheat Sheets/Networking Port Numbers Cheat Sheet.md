---
title: "Networking Port Numbers Cheat Sheet"
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

# Networking Port Numbers Cheat Sheet

> [!abstract]
> Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

| Command or value | Purpose |
|---|---|
| `FTP TCP 20/21` | File data/control |
| `SSH TCP 22` | Encrypted administration |
| `Telnet TCP 23` | Legacy clear-text administration |
| `SMTP TCP 25` | Mail transfer |
| `DNS UDP/TCP 53` | Name resolution |
| `DHCP UDP 67/68` | Address leasing |
| `TFTP UDP 69` | Simple file transfer |
| `HTTP TCP 80` | Web |
| `POP3 TCP 110` | Mail retrieval |
| `NTP UDP 123` | Time synchronization |
| `IMAP TCP 143` | Mailbox synchronization |
| `SNMP UDP 161/162` | Management/traps |
| `HTTPS TCP 443` | Encrypted web |
| `Syslog UDP 514` | Traditional logging |
| `RADIUS UDP 1812/1813` | Authentication/accounting |

## Use Safely

- Start with read-only `show`, ping, or lookup commands.
- Record the expected result before changing configuration.
- Do not copy placeholders or example credentials into production.

## Related Notes

- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
