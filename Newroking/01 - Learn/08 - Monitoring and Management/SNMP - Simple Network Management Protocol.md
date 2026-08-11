---
title: "SNMP - Simple Network Management Protocol"
aliases:
  - Simple Network Management Protocol
  - SNMP
type: protocol
status: active
area: Networking
protocol: SNMP
keywords:
  - SNMP
  - network management system
  - manager
  - agent
  - MIB
  - OID
  - trap
tags:
  - networking/protocols
  - networking/snmp
created: 2026-08-11
updated: 2026-08-11
related:
  - "[[Network Monitoring]]"
  - "[[Lab 14 - SNMP Monitoring]]"
category: "Network Management and Monitoring"
difficulty: "Mixed"
packet_tracer_supported: "Yes"
related_protocols: []
---

# SNMP - Simple Network Management Protocol

> [!abstract]
> SNMP (**Simple Network Management Protocol**) is an application-layer protocol used to monitor and manage network devices.

## 1. Architecture

```text
                    UDP 161: queries/responses
+----------------+  -------------------------->  +----------------+
| SNMP Manager   |                               | SNMP Agent     |
| (NMS)          |  <--------------------------  | Router/Switch  |
+----------------+                               +----------------+
        ^                                                 |
        |             UDP 162: trap/inform                |
        +-------------------------------------------------+

Manager: requests and records information
Agent:   runs on the managed device
MIB:     describes the available managed objects
OID:     identifies one specific managed object
```

## 2. Default ports

| Port | Transport | Purpose |
|---|---|---|
| `161` | UDP | Manager queries and agent responses |
| `162` | UDP | Traps and informs sent to the manager |

## 3. SNMP versions

| Version | Authentication and privacy | Recommendation |
|---|---|---|
| SNMPv1 | Community string; no encryption | Legacy only |
| SNMPv2c | Community string; no encryption | Suitable for isolated labs |
| SNMPv3 | User-based authentication and optional encryption | Preferred for production |

> [!warning]
> SNMPv1 and SNMPv2c community strings are not encrypted. Do not reuse lab community strings on production devices.

## 4. Common operations

| Operation | Direction | Purpose |
|---|---|---|
| `Get` | Manager to agent | Read one object |
| `GetNext` | Manager to agent | Read the next object in the MIB tree |
| `Set` | Manager to agent | Change a writable object |
| `Response` | Agent to manager | Return requested data or an error |
| `Trap` | Agent to manager | Send an unsolicited event notification |
| `Inform` | Agent to manager | Send an acknowledged notification |

## 5. Common system OIDs

| Object | OID | Information returned |
|---|---|---|
| `sysDescr.0` | `1.3.6.1.2.1.1.1.0` | Device and software description |
| `sysObjectID.0` | `1.3.6.1.2.1.1.2.0` | Device type identifier |
| `sysUpTime.0` | `1.3.6.1.2.1.1.3.0` | Time since the agent started |
| `sysContact.0` | `1.3.6.1.2.1.1.4.0` | Administrative contact |
| `sysName.0` | `1.3.6.1.2.1.1.5.0` | Device hostname |
| `sysLocation.0` | `1.3.6.1.2.1.1.6.0` | Device location |

## 6. Core terms

- **Agent** - Software on the monitored device that maintains management data.
- **Community string** - Shared credential used by SNMPv1 and SNMPv2c.
- **Manager/NMS** - System that queries agents and receives notifications.
- **MIB** - Hierarchical definition of managed objects.
- **OID** - Numeric path that uniquely identifies a managed object.
- **Trap** - Event notification sent without a preceding manager request.

---

**Parent:** [[Network Monitoring]]  
**Practice:** [[Lab 14 - SNMP Monitoring|Configure SNMP in Cisco Packet Tracer]]
