---
title: Network Notes Home
aliases:
  - Networking Home
  - Network Notes Index
type: map-of-content
status: active
area: Networking
keywords:
  - networking
  - index
  - knowledge base
tags:
  - moc
  - networking
created: 2026-08-11
updated: 2026-08-11
---

# Network Notes Home

> [!abstract]
> Central navigation page for networking concepts, protocols, vendors, and hands-on labs.

## 1. Start here

```text
Network Notes
|
+-- Fundamentals
|   `-- Network Monitoring
|
+-- Protocols
|   +-- NTP
|   +-- SNMP
|   `-- Syslog
|
+-- Cisco
|   +-- NTP Packet Tracer Lab
|   +-- SNMP Packet Tracer Lab
|   `-- Syslog Packet Tracer Lab
|
`-- Templates
    `-- Networking Note Template
```

## 2. Knowledge map

### Fundamentals

- [[Network Monitoring]] - Why and how network devices are observed.

### Protocols

- [[NTP - Overview|NTP Overview]] - Time synchronization, strata, and UDP port 123.
- [[SNMP - Overview|SNMP Overview]] - Architecture, versions, ports, OIDs, and security.
- [[Syslog - Overview|Syslog Overview]] - Message flow, facilities, and severity levels.

### Cisco labs

- [[NTP - Cisco Packet Tracer Lab|Configure NTP in Cisco Packet Tracer]] - Synchronize a router with an NTP server.
- [[SNMP - Cisco Packet Tracer Lab|Configure SNMP in Cisco Packet Tracer]] - Complete beginner lab.
- [[Syslog - Cisco Packet Tracer Lab|Configure Syslog in Cisco Packet Tracer]] - Send router events to a central server.

## 3. Suggested learning order

1. Read [[Network Monitoring]].
2. Learn [[NTP - Overview|NTP]] and complete the [[NTP - Cisco Packet Tracer Lab|NTP Packet Tracer lab]].
3. Learn [[Syslog - Overview|Syslog]] and complete the [[Syslog - Cisco Packet Tracer Lab|Syslog Packet Tracer lab]].
4. Learn [[SNMP - Overview|SNMP]] and complete the [[SNMP - Cisco Packet Tracer Lab|SNMP Packet Tracer lab]].

## 4. Vault conventions

> [!info] Folder order
> Numbered folders keep broad subject areas in a stable order. Note titles do not include the folder number.

Every permanent note should contain:

- YAML properties with `title`, `type`, `status`, `area`, `keywords`, and `tags`.
- One clear `#` title matching the `title` property.
- Numbered `##` sections for predictable reading order.
- Links to prerequisite, parent, or related notes.
- A short summary callout near the top.
- ASCII diagrams when a topology or process needs a visual.

Use [[Networking Note Template]] when adding a note.

## 5. Status legend

| Status | Meaning |
|---|---|
| `draft` | Incomplete or awaiting review |
| `active` | Maintained navigation or reference note |
| `complete` | Finished and verified note or lab |

---

**Next:** [[Network Monitoring]]
