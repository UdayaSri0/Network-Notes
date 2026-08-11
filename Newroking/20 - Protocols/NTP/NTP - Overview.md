---
title: NTP Overview
aliases:
  - Network Time Protocol
  - NTP
type: protocol
status: active
area: Networking
protocol: NTP
keywords:
  - NTP
  - time synchronization
  - stratum
  - UDP 123
  - clock synchronization
tags:
  - networking/protocols
  - networking/ntp
created: 2026-08-11
updated: 2026-08-11
related:
  - "[[Network Monitoring]]"
  - "[[Syslog - Overview]]"
  - "[[NTP - Cisco Packet Tracer Lab]]"
---

# NTP Overview

> [!abstract]
> NTP (**Network Time Protocol**) synchronizes clocks across network devices so logs, certificates, scheduled tasks, and security events use consistent time.

## 1. Why accurate time matters

- Events from different devices can be placed in the correct order.
- [[Syslog - Overview|Syslog]] messages receive useful timestamps.
- Authentication and certificates can be validated correctly.
- Scheduled jobs and configuration changes occur at the intended time.
- Troubleshooting evidence can be correlated across the network.

## 2. Basic operation

```text
                     UDP port 123
+----------------+  time request/response  +----------------+
| NTP Client     | <----------------------> | NTP Server     |
| Router/Switch  |                          | Time Source    |
+----------------+                          +----------------+
```

An NTP client exchanges timing information with a server and adjusts its local clock. It normally makes gradual corrections instead of repeatedly forcing large clock changes.

## 3. NTP hierarchy

```text
Stratum 0  Reference clock: GPS or atomic clock
    |
Stratum 1  Server directly connected to stratum 0
    |
Stratum 2  Server synchronized to stratum 1
    |
Stratum 3  Server synchronized to stratum 2
    |
  Clients  Routers, switches, servers, and endpoints
```

| Stratum | Meaning |
|---|---|
| `0` | High-precision reference clock; not normally queried directly by clients |
| `1` | Server directly connected to a stratum 0 source |
| `2-15` | Successive synchronization levels |
| `16` | Unsynchronized or unreachable time source |

> [!important]
> A lower stratum represents a source closer to a reference clock. It does not automatically guarantee a better network path or a healthier server.

## 4. Port and transport

| Protocol | Port | Transport | Purpose |
|---|---|---|---|
| NTP | `123` | UDP | Time requests and responses |

## 5. Cisco IOS concepts

| Command | Purpose |
|---|---|
| `ntp server <address>` | Configure a remote NTP server |
| `show clock` | Display the device clock |
| `show ntp associations` | Display configured NTP peers and their state |
| `show ntp status` | Display synchronization status |
| `clock timezone <name> <hours> [minutes]` | Set the local timezone offset |

## 6. Verification indicators

On Cisco IOS, an asterisk beside an association normally marks the current synchronization source:

```text
address         ref clock       st   when   poll reach  delay  offset   disp
*~192.168.1.10  ...              2     20     64   377  ...    ...      ...
```

Packet Tracer may display fewer fields than physical Cisco IOS.

## 7. Security considerations

- Permit NTP only from approved sources.
- Use authentication where the device and server support it.
- Use multiple reliable time sources in production.
- Monitor for large time changes and unreachable sources.
- Do not treat a manually configured clock as ongoing synchronization.

## 8. Key terms

- **Client** - Device that synchronizes its clock from an NTP source.
- **Reference clock** - Precise physical time source.
- **Server** - Device that supplies time to NTP clients.
- **Stratum** - Distance in the NTP hierarchy from a reference clock.
- **Synchronized** - Successfully using an acceptable time source.

---

**Parent:** [[Network Notes Home]]  
**Practice:** [[NTP - Cisco Packet Tracer Lab|Configure NTP in Cisco Packet Tracer]]  
**Related:** [[Syslog - Overview|Syslog Overview]]
