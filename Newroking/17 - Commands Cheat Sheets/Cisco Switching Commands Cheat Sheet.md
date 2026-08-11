---
title: "Cisco Switching Commands Cheat Sheet"
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

# Cisco Switching Commands Cheat Sheet

> [!abstract]
> Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

| Command or value | Purpose |
|---|---|
| `switchport mode access` | Force an access port |
| `switchport access vlan <ID>` | Assign the access VLAN |
| `switchport mode trunk` | Force a static trunk |
| `switchport trunk allowed vlan <LIST>` | Restrict trunk VLANs |
| `spanning-tree vlan <ID> root primary` | Prefer this switch as root |
| `channel-group <ID> mode active` | Create an LACP bundle |
| `show mac address-table` | Inspect learned MAC addresses |
| `show interfaces trunk` | Verify trunk state |

## Use Safely

- Start with read-only `show`, ping, or lookup commands.
- Record the expected result before changing configuration.
- Do not copy placeholders or example credentials into production.

## Related Notes

- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
