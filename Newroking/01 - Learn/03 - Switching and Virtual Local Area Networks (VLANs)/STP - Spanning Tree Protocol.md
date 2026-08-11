---
title: "STP - Spanning Tree Protocol"
aliases:
  - STP Overview
  - Spanning Tree Protocol
  - STP
type: protocol
status: active
area: Networking
protocol: STP
keywords:
  - spanning tree protocol
  - STP
  - RSTP
  - PVST+
  - root bridge
  - bridge ID
  - BPDU
  - Layer 2 loop prevention
tags:
  - networking/protocols
  - networking/stp
  - switching
created: 2026-08-11
updated: 2026-08-11
related:
  - "[[Network Monitoring]]"
  - "[[HSRP - Hot Standby Router Protocol]]"
  - "[[Lab 20 - STP]]"
category: "Switching"
difficulty: "Mixed"
packet_tracer_supported: "Yes"
related_protocols: []
---

# STP - Spanning Tree Protocol

> [!abstract]
> STP (**Spanning Tree Protocol**) prevents Layer 2 switching loops while preserving redundant physical links that can be activated after a failure.

## 1. Why STP is necessary

Ethernet frames do not contain a hop-count field. A switching loop can therefore circulate broadcasts, multicasts, and unknown unicasts indefinitely.

```text
               Redundant Layer 2 links
        +---------- Switch1 ----------+
        |              |              |
     Switch2 ----------+---------- Switch3
        |                             |
        +------ physical loop --------+
```

Without STP, a loop can cause:

- Broadcast storms.
- Duplicate frames.
- Unstable MAC address tables.
- High link and CPU utilization.
- Loss of network connectivity.

STP creates one loop-free logical tree by placing selected redundant ports into a non-forwarding state.

## 2. STP process

```text
1. Elect one root bridge
          |
          v
2. Select one root port on each non-root switch
          |
          v
3. Select one designated port per network segment
          |
          v
4. Place remaining redundant ports in a blocking/discarding role
```

## 3. Bridge Protocol Data Units

Switches exchange **BPDUs** to describe the spanning-tree topology.

A BPDU includes information used to compare paths, such as:

- Root bridge ID.
- Root path cost.
- Sender bridge ID.
- Sender port ID.
- STP timers.

The best information wins each comparison.

## 4. Root bridge election

The switch with the lowest **Bridge ID (BID)** becomes the root bridge.

```text
Bridge ID = bridge priority + extended system ID + switch MAC address
```

Election order:

1. Lowest bridge priority.
2. If tied, lowest MAC address.

The common default bridge priority is `32768`. Cisco per-VLAN spanning tree incorporates the VLAN number into the displayed priority value.

> [!important]
> Do not leave the root bridge selection to chance. Configure the intended central switch with a lower priority.

## 5. Port roles

| Role | Where it appears | Behavior |
|---|---|---|
| Root | One per non-root switch | Best path toward the root bridge |
| Designated | One per network segment | Best forwarding port for that segment |
| Alternate | Redundant path | Discarding until needed |
| Backup | Redundant path on the same shared segment | Discarding until needed |

Every active port on the root bridge is normally a designated port.

## 6. Path selection

A non-root switch selects the path with the lowest total STP cost to the root bridge.

Common short path-cost values include:

| Link speed | STP cost |
|---:|---:|
| 10 Mbps | `100` |
| 100 Mbps | `19` |
| 1 Gbps | `4` |
| 10 Gbps | `2` |

When costs tie, STP continues comparing bridge IDs and port IDs until one path wins.

## 7. Port states

### Classic STP states

```text
Blocking --> Listening --> Learning --> Forwarding
```

| State | Learns MAC addresses | Forwards user frames |
|---|---:|---:|
| Blocking | No | No |
| Listening | No | No |
| Learning | Yes | No |
| Forwarding | Yes | Yes |
| Disabled | No | No |

### Rapid STP states

Rapid STP combines the classic non-forwarding states:

```text
Discarding --> Learning --> Forwarding
```

## 8. Common Cisco modes

| Mode | Description |
|---|---|
| PVST+ | Separate classic spanning-tree instance for each VLAN |
| Rapid PVST+ | Separate rapid spanning-tree instance for each VLAN |
| MST | Maps multiple VLANs into a smaller number of spanning-tree instances |

Packet Tracer switch models commonly support PVST+ and Rapid PVST+.

## 9. PortFast and BPDU Guard

**PortFast** lets an endpoint-facing access port move directly to forwarding instead of waiting through normal STP convergence.

**BPDU Guard** disables a protected edge port if it receives a BPDU, helping prevent an unauthorized switch from affecting the topology.

```text
PC ---- access port [PortFast + BPDU Guard] ---- Switch
```

> [!warning]
> Enable PortFast only on ports connected to endpoints. Do not enable it on normal links between switches.

Recommended endpoint-port configuration:

```cisco
interface fastEthernet 0/10
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
```

## 10. Basic Cisco IOS commands

| Command | Purpose |
|---|---|
| `show spanning-tree` | Display all active spanning-tree instances |
| `show spanning-tree vlan 10` | Display the tree for VLAN 10 |
| `show spanning-tree summary` | Display mode and general status |
| `spanning-tree vlan 10 priority 24576` | Set an explicit root-bridge priority |
| `spanning-tree vlan 10 root primary` | Let IOS choose a priority intended to become root |
| `spanning-tree vlan 10 root secondary` | Configure a backup root preference |
| `spanning-tree mode rapid-pvst` | Enable Rapid PVST+ where supported |

## 11. Design rules

- Select the root bridge intentionally for each VLAN.
- Place the root near the logical center of the Layer 2 topology.
- Use a second planned switch as the backup root.
- Configure PortFast only on endpoint-facing access ports.
- Pair PortFast with BPDU Guard on untrusted edge ports.
- Verify the active and alternate paths after every topology change.
- Avoid disabling STP simply to force a link to forward.

## 12. Key terms

- **BPDU** - Control frame switches use to build and maintain the tree.
- **Bridge ID** - Priority and MAC-based value used in elections.
- **Designated port** - Forwarding port selected for one segment.
- **Root bridge** - Reference switch at the center of the STP topology.
- **Root port** - Best port toward the root on a non-root switch.
- **Topology change** - Event that causes STP to update forwarding information.

## 13. Relationship with HSRP

STP and [[HSRP - Hot Standby Router Protocol|HSRP]] provide redundancy at different layers:

| Protocol | Layer | Protects against |
|---|---|---|
| STP | Layer 2 | Loops and failed switch paths |
| HSRP | Layer 3 | Failure of the endpoint's default gateway |

A campus LAN can use both: STP chooses safe switching paths while HSRP maintains a virtual routed gateway.

## 14. References

- [Cisco STP configuration guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/stp/stp-configuration-guide/m-stp.html)
- [Cisco PortFast and BPDU Guard guidance](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10586-65.html)

---

**Parent:** [[Networking Dashboard]]  
**Practice:** [[Lab 20 - STP|Configure STP in Cisco Packet Tracer]]
