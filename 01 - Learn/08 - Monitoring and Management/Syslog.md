---
title: Syslog Overview
aliases:
  - System Logging Protocol
  - Syslog
type: protocol
status: active
area: Networking
protocol: Syslog
keywords:
  - Syslog
  - logging
  - event messages
  - severity levels
  - UDP 514
  - log server
tags:
  - networking/protocols
  - networking/syslog
  - monitoring
created: 2026-08-11
updated: 2026-08-11
related:
  - "[[Network Monitoring]]"
  - "[[NTP - Network Time Protocol]]"
  - "[[Lab 15 - Syslog Server]]"
category: "Network Management and Monitoring"
difficulty: "Mixed"
packet_tracer_supported: "Yes"
related_protocols: []
---

# Syslog Overview

> [!abstract]
> Syslog provides a standard way for network devices and systems to generate event messages and send them to a central logging server.

## 1. Why centralize logs

- Preserve events when a device restarts or loses local history.
- Search messages from many devices in one place.
- Correlate failures and security events.
- Alert administrators about important conditions.
- Support troubleshooting, auditing, and incident response.

## 2. Basic message flow

```text
+----------------+    Syslog messages    +----------------+
| Router/Switch  | --------------------> | Syslog Server  |
| Log Source     |       UDP 514         | Collector      |
+----------------+                       +----------------+

The source generates events; the server receives and stores them.
```

## 3. Common ports

| Port | Transport | Typical use |
|---|---|---|
| `514` | UDP | Traditional Syslog; used by Packet Tracer labs |
| `514` | TCP | Reliable transport on supported systems |
| `6514` | TCP with TLS | Encrypted Syslog on supported systems |

> [!note]
> Packet Tracer provides a simplified Syslog service and commonly simulates UDP port `514`.

## 4. Severity levels

| Number | Name | Meaning |
|---:|---|---|
| `0` | Emergencies | System is unusable |
| `1` | Alerts | Immediate action is required |
| `2` | Critical | Critical condition |
| `3` | Errors | Error condition |
| `4` | Warnings | Warning condition |
| `5` | Notifications | Normal but significant condition |
| `6` | Informational | Informational message |
| `7` | Debugging | Detailed troubleshooting message |

> [!important] Severity filtering
> A configured level includes that level and every more severe level. For example, `logging trap informational` sends levels `0` through `6`, but not level `7`.

## 5. Reading a Cisco Syslog message

```text
*Aug 11 10:15:20.123: %LINK-5-CHANGED: Interface Loopback0, changed state to up
|____________________|  |____| |_______|  |____________________________________|
       timestamp        facility severity               message
```

| Part | Example | Meaning |
|---|---|---|
| Timestamp | `Aug 11 10:15:20.123` | When the event occurred |
| Facility | `LINK` | Cisco subsystem that produced the event |
| Severity | `5` | Notification-level event |
| Mnemonic | `CHANGED` | Short event identifier |
| Description | Interface state text | Human-readable event details |

## 6. Cisco logging destinations

| Destination | Purpose |
|---|---|
| Console | Display messages on the console session |
| Monitor | Display messages on terminal sessions |
| Buffer | Store a limited local history in memory |
| Remote host | Send messages to a central Syslog server |

## 7. Relationship with NTP

[[NTP - Network Time Protocol|NTP]] is essential to useful logging. If devices have different clocks, events can appear in the wrong order and troubleshooting becomes unreliable.

```text
NTP Server ---> synchronized time ---> Router
                                          |
                                          v
Syslog Server <--- timestamped events ----+
```

## 8. Security and reliability

- Synchronize every device to trusted NTP sources.
- Restrict who can send logs to the server.
- Protect the server from unauthorized access and deletion.
- Use reliable or encrypted transport where supported and required.
- Choose a severity threshold that provides useful detail without excessive noise.

## 9. Key terms

- **Facility** - Subsystem or category that generated a message.
- **Log source** - Device or application that generates messages.
- **Severity** - Numeric importance level from `0` through `7`.
- **Syslog server** - Central system that receives and stores messages.
- **Timestamp** - Date and time attached to an event.

---

**Parent:** [[Network Monitoring]]  
**Practice:** [[Lab 15 - Syslog Server|Configure Syslog in Cisco Packet Tracer]]  
**Related:** [[NTP - Network Time Protocol|NTP Overview]]
