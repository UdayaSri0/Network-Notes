---
title: "Cisco Troubleshooting Cheat Sheet"
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

# Cisco Troubleshooting Cheat Sheet

> [!abstract]
> Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

| Command or value | Purpose |
|---|---|
| `show running-config` | Compare active configuration with design |
| `show ip interface brief` | Start with interface state |
| `show interfaces` | Inspect counters, duplex, and errors |
| `show arp` | Check IPv4-to-MAC resolution |
| `show mac address-table` | Follow Layer 2 learning |
| `show ip route` | Follow Layer 3 forwarding |
| `ping <IP>` | Test reachability |
| `traceroute <IP>` | Find the first failing routed hop |
| `show logging` | Correlate device events |

## Use Safely

- Start with read-only `show`, ping, or lookup commands.
- Record the expected result before changing configuration.
- Do not copy placeholders or example credentials into production.

## Related Notes

- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
