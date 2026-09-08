---
title: "HSRP - Hot Standby Router Protocol"
aliases:
  - Hot Standby Router Protocol
  - HSRP
type: protocol
status: active
area: Networking
vendor: Cisco
protocol: HSRP
keywords:
  - HSRP
  - first-hop redundancy
  - virtual gateway
  - active router
  - standby router
  - gateway availability
tags:
  - networking/protocols
  - networking/hsrp
  - cisco
created: 2026-08-11
updated: 2026-08-11
related:
  - "[[Network Monitoring]]"
  - "[[Lab 23 - HSRP]]"
category: "Redundancy and High Availability"
difficulty: "Mixed"
packet_tracer_supported: "Yes"
related_protocols: []
---

# HSRP - Hot Standby Router Protocol

> [!abstract]
> HSRP (**Hot Standby Router Protocol**) is a Cisco first-hop redundancy protocol that lets multiple routers provide one highly available virtual default gateway.

## 1. The problem HSRP solves

An endpoint normally has only one configured default-gateway address. If that physical gateway fails, the endpoint can lose access to remote networks even when another router is available.

```text
Without HSRP

PC ----> Router1 ----> Remote network
            X
       Gateway failure
```

HSRP places a virtual IP address and virtual MAC address in front of the physical routers:

```text
With HSRP

                       +--> Router1: Active
PC --> Virtual Gateway |
                       +--> Router2: Standby
```

The endpoint always uses the virtual IP as its default gateway.

## 2. HSRP roles

| Role | Purpose |
|---|---|
| Active | Forwards traffic sent to the virtual gateway |
| Standby | Takes over if the active router fails |
| Listen | Participates in the group but is neither active nor standby |

## 3. Core values

| Item | Meaning |
|---|---|
| Group number | Identifies one HSRP group on an interface |
| Virtual IP | Default-gateway address used by endpoints |
| Priority | Controls the active-router election; higher is preferred |
| Preemption | Allows a higher-priority router to take back the active role |
| Tracking | Reduces priority when a monitored interface or object fails |

The default priority is `100`. If priorities tie, the router with the higher HSRP interface IP address wins the election.

## 4. Election and recovery

```text
Highest priority
      |
      v
Active router ---- failure ----> Standby becomes Active
                                      |
                     higher-priority router recovers
                                      |
                           preempt configured?
                              |             |
                             yes            no
                              |             |
                       role returns     roles remain
```

> [!important]
> A recovered router does not take back the active role merely because it has a higher priority. Configure `standby <group> preempt` when that behavior is required.

## 5. HSRP states

```text
Initial --> Learn --> Listen --> Speak --> Standby or Active
```

| State | Description |
|---|---|
| Initial | HSRP is starting or the interface is unavailable |
| Learn | Router has not learned the virtual IP |
| Listen | Router knows the group but is not active or standby |
| Speak | Router sends hello messages and participates in the election |
| Standby | Router is the next candidate to become active |
| Active | Router forwards traffic for the virtual gateway |

## 6. HSRP versions

| Feature | HSRPv1 | HSRPv2 |
|---|---|---|
| Common multicast address | `224.0.0.2` | `224.0.0.102` |
| UDP port | `1985` | `1985` |
| Group range | `0-255` | `0-4095` |

The Packet Tracer lab uses the default HSRP version available on the selected router model.

## 7. Basic Cisco IOS commands

```cisco
interface gigabitEthernet 0/0
 standby 1 ip 192.168.10.1
 standby 1 priority 110
 standby 1 preempt
```

| Command | Purpose |
|---|---|
| `standby 1 ip 192.168.10.1` | Create group 1 and assign its virtual IP |
| `standby 1 priority 110` | Prefer this router over the default priority of 100 |
| `standby 1 preempt` | Permit this router to take the active role when preferred |
| `standby 1 track g0/1 20` | Reduce priority by 20 if the tracked interface fails |
| `show standby brief` | Display a compact HSRP status table |
| `show standby` | Display detailed HSRP state and timers |

## 8. Design rules

- Place both physical router addresses and the virtual IP in the same subnet.
- Configure the same group number and virtual IP on both routers.
- Give every physical router a unique interface IP address.
- Configure endpoints with the virtual IP, not a physical router address.
- Use priority and preemption deliberately.
- Track the upstream path when LAN-interface status alone cannot detect a failure.

## 9. Key terms

- **Active router** - Router currently forwarding traffic for the virtual gateway.
- **First hop** - First router an endpoint uses to reach other networks.
- **Preemption** - Ability of a preferred router to take over the active role.
- **Standby router** - Router ready to assume the active role.
- **Virtual IP** - Shared gateway address configured on all members of the HSRP group.

## 10. References

- [Cisco: HSRP configuration guide](https://www.cisco.com/c/en/us/td/docs/routers/ios-xe/network-services/network-services/m_fhp-hsrp-0.html)
- [Cisco: Using HSRP preempt and interface tracking](https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/13780-6.html)

---

**Parent:** [[Networking Dashboard]]  
**Practice:** [[Lab 23 - HSRP|Configure HSRP in Cisco Packet Tracer]]
