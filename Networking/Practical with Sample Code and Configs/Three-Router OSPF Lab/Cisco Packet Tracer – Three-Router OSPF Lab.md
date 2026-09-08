---
title: Cisco Packet Tracer – Three-Router OSPF Lab
aliases:
  - Three-Router OSPF Lab
  - Three-Router OSPF Lab - Configuration Guide
  - Cisco Packet Tracer OSPF Practical
  - OSPF Triangle Network Configuration Guide
tags:
  - networking
  - cisco
  - packet-tracer
  - ospf
  - single-area
  - practical
created: 2026-09-08
---

# Cisco Packet Tracer – Three-Router OSPF Lab

Configure the supplied Packet Tracer triangle using **OSPFv2 in area 0**, connect the three LANs, and demonstrate automatic routing around a failed router-to-router link.

> [!info] Addressing assumptions
> All device addresses and port assignments below follow the supplied diagram. The image does **not** specify subnet masks: this guide assumes `/24` for each LAN and `/30` for each router link. OSPF process `1`, area `0`, and the router IDs are configuration choices for this lab.

> [!note] Scope and validation
> These are sample Cisco IOS configurations reviewed against the diagram and Cisco documentation. The companion `.pkt` file has been renamed for this lab; its saved device configurations and simulation behavior have not been verified. Expected outputs are illustrative; use the checks below to verify your own Packet Tracer simulation. The `200.100.x.x` addresses are retained from the diagram for this isolated lab; they are not private RFC 1918 addresses.

## Lab files

- Packet Tracer project: [[Three-Router OSPF Lab.pkt]]
- Topology image: [[Three-Router OSPF Topology.png]]

Keep these files alongside this note. The project was previously named `HSRP Gateway Redundancy Lab.pkt`; renaming it does not apply the OSPF commands or change its contents.

## Contents

- [[#1. Topology and cabling]]
- [[#2. Addressing plan]]
- [[#3. Prepare the devices]]
- [[#4. Configure the switches]]
- [[#5. Configure PC addressing]]
- [[#6. Configure router interfaces]]
- [[#7. Verify directly connected networks]]
- [[#8. Enable single-area OSPF]]
- [[#9. Verify OSPF and routing]]
- [[#10. Test end-to-end connectivity]]
- [[#11. Test automatic failover]]
- [[#12. Troubleshooting]]
- [[#13. Save and completion checklist]]
- [[#14. Related notes and references]]

---

## 1. Topology and cabling

![[Three-Router OSPF Topology.png]]

*Supplied topology screenshot. Some interface status indicators are red; use the configuration and verification steps below to bring the links up. Cable color alone does not indicate link status.*

```text
                       PC1: 200.100.20.5
                               |
                        Switch1 / VLAN 20
                               |
                       R1: 200.100.20.1
                         /           \
         10.10.10.0/30 /             \ 10.10.10.4/30
                       /               \
                     R2-----------------R3
                       10.10.10.8/30
                      |                 |
              200.100.10.1       200.100.30.1
                      |                 |
             Switch0 / VLAN 10  Switch2 / VLAN 30
                      |                 |
             PC0: 200.100.10.5  PC2: 200.100.30.5
```

The Packet Tracer labels `Router1`, `Router2`, and `Router3` correspond to CLI hostnames **R1**, **R2**, and **R3**. Switch0 becomes **SW10**, Switch1 becomes **SW20**, and Switch2 becomes **SW30**.

| Connection | First device and port | Second device and port |
|---|---|---|
| R2 ↔ R1 | R2 `Gi0/0` | R1 `Gi0/0` |
| R1 ↔ R3 | R1 `Gi1/0` | R3 `Gi1/0` |
| R2 ↔ R3 | R2 `Gi1/0` | R3 `Gi0/0` |
| VLAN 10 uplink | R2 `Gi2/0` | Switch0 `Gi0/1` |
| VLAN 20 uplink | R1 `Gi2/0` | Switch1 `Gi0/1` |
| VLAN 30 uplink | R3 `Gi2/0` | Switch2 `Gi0/1` |
| PC0 | PC0 `Fa0` | Switch0 `Fa0/1` |
| PC1 | PC1 `Fa0` | Switch1 `Fa0/1` |
| PC2 | PC2 `Fa0` | Switch2 `Fa0/1` |

Use copper straight-through for PC-to-switch and switch-to-router connections. Use copper crossover for direct Ethernet router links, or Packet Tracer's automatic cable selection.

> [!important] One VLAN per switch uplink
> Both used ports on each switch are **access ports in the same VLAN**. Each router has a dedicated physical LAN interface. No trunk, `encapsulation dot1Q`, or router subinterface is needed. The 2960 switches provide Layer 2 switching; OSPF runs on the routers.

## 2. Addressing plan

### LANs and PCs

| VLAN | LAN subnet | Mask | Router gateway | PC address |
|---|---|---|---|---|
| 10 | `200.100.10.0/24` | `255.255.255.0` | R2: `200.100.10.1` | PC0: `200.100.10.5` |
| 20 | `200.100.20.0/24` | `255.255.255.0` | R1: `200.100.20.1` | PC1: `200.100.20.5` |
| 30 | `200.100.30.0/24` | `255.255.255.0` | R3: `200.100.30.1` | PC2: `200.100.30.5` |

### Router-to-router subnets

| Link | Subnet | Usable addresses | Broadcast | Mask |
|---|---|---|---|---|
| R2 ↔ R1 | `10.10.10.0/30` | `.1` and `.2` | `10.10.10.3` | `255.255.255.252` |
| R1 ↔ R3 | `10.10.10.4/30` | `.5` and `.6` | `10.10.10.7` | `255.255.255.252` |
| R2 ↔ R3 | `10.10.10.8/30` | `.9` and `.10` | `10.10.10.11` | `255.255.255.252` |

### Complete router interface map

| Router | Interface | Address | Mask | Connected device |
|---|---|---|---|---|
| R1 | `Gi0/0` | `10.10.10.2` | `255.255.255.252` | R2 `Gi0/0` |
| R1 | `Gi1/0` | `10.10.10.5` | `255.255.255.252` | R3 `Gi1/0` |
| R1 | `Gi2/0` | `200.100.20.1` | `255.255.255.0` | SW20 `Gi0/1` |
| R2 | `Gi0/0` | `10.10.10.1` | `255.255.255.252` | R1 `Gi0/0` |
| R2 | `Gi1/0` | `10.10.10.9` | `255.255.255.252` | R3 `Gi0/0` |
| R2 | `Gi2/0` | `200.100.10.1` | `255.255.255.0` | SW10 `Gi0/1` |
| R3 | `Gi0/0` | `10.10.10.10` | `255.255.255.252` | R2 `Gi1/0` |
| R3 | `Gi1/0` | `10.10.10.6` | `255.255.255.252` | R1 `Gi1/0` |
| R3 | `Gi2/0` | `200.100.30.1` | `255.255.255.0` | SW30 `Gi0/1` |

### OSPF choices

| Setting | Value |
|---|---|
| Protocol | OSPFv2 for IPv4 |
| Process ID | `1` on all routers, for consistency |
| Area | `0` on all participating interfaces |
| Router IDs | R1: `1.1.1.1`; R2: `2.2.2.2`; R3: `3.3.3.3` |
| Passive interface | Each router's LAN interface, `Gi2/0` |
| Link network type | Default Ethernet broadcast |

The router IDs are identifiers, not extra interface addresses or PC gateways. Process IDs are local to each router and need not match between neighbors. Area IDs must match on a shared link. See [Cisco's OSPF interface guide](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13689-17.html).

## 3. Prepare the devices

1. Save a working copy of the Packet Tracer project.
2. Check the cables against section 1. If rebuilding with `Router-PT-Empty`, power off the router before fitting compatible copper Gigabit Ethernet modules, then power it on.
3. Open each router's **CLI**. If asked to enter the initial configuration dialog, answer `no`, then press Enter.
4. Check actual port names:

```ios
enable
show ip interface brief
show running-config
show ip route
```

The configuration below uses the diagram's `GigabitEthernet0/0`, `1/0`, and `2/0`. If your hardware uses different names, map them to the same physical links before pasting commands.

> [!warning] Reusing an earlier lab
> These blocks assume a clean lab routing configuration. Inspect old addresses, static routes, OSPF settings, ACLs, and any HSRP configuration first. Remove obsolete settings individually. A normal static route to the same prefix can take precedence over OSPF and hide the result. To remove a specific old static route, enter `no ` followed by its exact `ip route ...` line in global configuration mode. Do not erase the entire configuration as a troubleshooting shortcut.

## 4. Configure the switches

Open the correct switch's CLI and enter its block. Commands are shown without prompts so they can be pasted. `exit` changes configuration level; `end` returns to privileged EXEC mode.

### Switch0 → SW10

```ios
enable
configure terminal
hostname SW10
vlan 10
 name LAN10
 exit
interface fastEthernet0/1
 description PC0
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
 exit
interface gigabitEthernet0/1
 description R2_Gi2/0
 switchport mode access
 switchport access vlan 10
 no shutdown
 exit
end
```

### Switch1 → SW20

```ios
enable
configure terminal
hostname SW20
vlan 20
 name LAN20
 exit
interface fastEthernet0/1
 description PC1
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 no shutdown
 exit
interface gigabitEthernet0/1
 description R1_Gi2/0
 switchport mode access
 switchport access vlan 20
 no shutdown
 exit
end
```

### Switch2 → SW30

```ios
enable
configure terminal
hostname SW30
vlan 30
 name LAN30
 exit
interface fastEthernet0/1
 description PC2
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 no shutdown
 exit
interface gigabitEthernet0/1
 description R3_Gi2/0
 switchport mode access
 switchport access vlan 30
 no shutdown
 exit
end
```

PortFast is enabled only on the PC-facing ports. Allow the uplinks time to reach forwarding state.

On each switch, run:

```ios
show vlan brief
show interfaces fastEthernet0/1 switchport
show interfaces gigabitEthernet0/1 switchport
```

**Expected:** VLAN 10, 20, or 30 is active on its switch, with both `Fa0/1` and `Gi0/1` assigned to it. Switch management IP addresses are not required for this lab.

## 5. Configure PC addressing

On each PC, open **Desktop → IP Configuration → Static** and enter:

| PC | IPv4 address | Subnet mask | Default gateway |
|---|---|---|---|
| PC0 | `200.100.10.5` | `255.255.255.0` | `200.100.10.1` |
| PC1 | `200.100.20.5` | `255.255.255.0` | `200.100.20.1` |
| PC2 | `200.100.30.5` | `255.255.255.0` | `200.100.30.1` |

Leave DNS blank; all tests use IP addresses. The default gateway must be the router interface in the PC's own LAN.

## 6. Configure router interfaces

### Router1 → R1

```ios
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 description TO_R2_Gi0/0
 ip address 10.10.10.2 255.255.255.252
 no shutdown
 exit
interface gigabitEthernet1/0
 description TO_R3_Gi1/0
 ip address 10.10.10.5 255.255.255.252
 no shutdown
 exit
interface gigabitEthernet2/0
 description VLAN20_GATEWAY
 ip address 200.100.20.1 255.255.255.0
 no shutdown
 exit
end
```

### Router2 → R2

```ios
enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 description TO_R1_Gi0/0
 ip address 10.10.10.1 255.255.255.252
 no shutdown
 exit
interface gigabitEthernet1/0
 description TO_R3_Gi0/0
 ip address 10.10.10.9 255.255.255.252
 no shutdown
 exit
interface gigabitEthernet2/0
 description VLAN10_GATEWAY
 ip address 200.100.10.1 255.255.255.0
 no shutdown
 exit
end
```

### Router3 → R3

```ios
enable
configure terminal
hostname R3
interface gigabitEthernet0/0
 description TO_R2_Gi1/0
 ip address 10.10.10.10 255.255.255.252
 no shutdown
 exit
interface gigabitEthernet1/0
 description TO_R1_Gi1/0
 ip address 10.10.10.6 255.255.255.252
 no shutdown
 exit
interface gigabitEthernet2/0
 description VLAN30_GATEWAY
 ip address 200.100.30.1 255.255.255.0
 no shutdown
 exit
end
```

## 7. Verify directly connected networks

On every router:

```ios
show ip interface brief
show ip route connected
```

**Expected:** all three configured interfaces are `up/up`, with the addresses in section 2. The three attached subnets appear as connected routes. Some IOS images also show local `/32` routes.

Run these neighbor pings from the routers:

| Router | First test | Second test | Local PC test |
|---|---|---|---|
| R1 | `ping 10.10.10.1` | `ping 10.10.10.6` | `ping 200.100.20.5` |
| R2 | `ping 10.10.10.2` | `ping 10.10.10.10` | `ping 200.100.10.5` |
| R3 | `ping 10.10.10.9` | `ping 10.10.10.5` | `ping 200.100.30.5` |

On each PC, open **Desktop → Command Prompt**, run `ipconfig`, then ping its own default gateway. Repeat a ping if initial ARP resolution causes the first request to time out.

> [!tip] Checkpoint before OSPF
> All directly connected neighbor and local gateway tests should pass now. On a clean configuration, remote LAN communication is not expected until routing is configured. Fix local connectivity first.

## 8. Enable single-area OSPF

An OSPF `network` statement matches local interface IPv4 addresses using a wildcard mask and assigns the matching interfaces to an area. `/30` uses wildcard `0.0.0.3`; `/24` uses `0.0.0.255`. These are wildcard masks, not subnet masks. See the [Cisco OSPF command reference](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-i1.html).

### R1

```ios
configure terminal
router ospf 1
 router-id 1.1.1.1
 passive-interface default
 no passive-interface gigabitEthernet0/0
 no passive-interface gigabitEthernet1/0
 network 10.10.10.0 0.0.0.3 area 0
 network 10.10.10.4 0.0.0.3 area 0
 network 200.100.20.0 0.0.0.255 area 0
 exit
end
```

### R2

```ios
configure terminal
router ospf 1
 router-id 2.2.2.2
 passive-interface default
 no passive-interface gigabitEthernet0/0
 no passive-interface gigabitEthernet1/0
 network 10.10.10.0 0.0.0.3 area 0
 network 10.10.10.8 0.0.0.3 area 0
 network 200.100.10.0 0.0.0.255 area 0
 exit
end
```

### R3

```ios
configure terminal
router ospf 1
 router-id 3.3.3.3
 passive-interface default
 no passive-interface gigabitEthernet0/0
 no passive-interface gigabitEthernet1/0
 network 10.10.10.4 0.0.0.3 area 0
 network 10.10.10.8 0.0.0.3 area 0
 network 200.100.30.0 0.0.0.255 area 0
 exit
end
```

> [!important] Advertise the LAN while keeping it passive
> `passive-interface default` suppresses neighbor discovery on all OSPF interfaces. The two `no passive-interface` commands enable it on the router links. `Gi2/0` stays passive, but its connected LAN is still advertised because it matches a `network` statement. PCs and Layer 2 switches do not need to form OSPF neighbors. See [Cisco's passive-interface guide](https://www.cisco.com/c/en/us/td/docs/routers/ios-xe/ip-routing/b-ip-routing/m_iri-default-passive-interface.html).

If the simulator rejects `passive-interface default`, omit it and the two `no passive-interface` lines, then configure `passive-interface gigabitEthernet2/0` under `router ospf 1` instead. On a clean process this gives the same intended behavior for the three interfaces. Verify the passive state afterward.

## 9. Verify OSPF and routing

Allow time for neighbor discovery and database synchronization. Run these commands from privileged EXEC mode on each router:

```ios
show ip protocols
show ip ospf
show ip ospf neighbor
show ip ospf interface
show ip ospf database
show ip route ospf
show ip route
```

### 9.1 Neighbor checklist

Each router should have **two FULL neighbors** after convergence:

| Local router | Neighbor ID | Neighbor link address | Local interface |
|---|---|---|---|
| R1 | `2.2.2.2` | `10.10.10.1` | `Gi0/0` |
| R1 | `3.3.3.3` | `10.10.10.6` | `Gi1/0` |
| R2 | `1.1.1.1` | `10.10.10.2` | `Gi0/0` |
| R2 | `3.3.3.3` | `10.10.10.10` | `Gi1/0` |
| R3 | `2.2.2.2` | `10.10.10.9` | `Gi0/0` |
| R3 | `1.1.1.1` | `10.10.10.5` | `Gi1/0` |

The links use Ethernet's default **broadcast** OSPF network type even though their IP subnets are `/30`. Expect neighbor states such as `FULL/DR` or `FULL/BDR`; the role depends on the election. A `/30` mask does not change the OSPF network type. See [Cisco's interface state explanation](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13689-17.html).

There should be no neighbor on `Gi2/0`. Check it with:

```ios
show ip ospf interface gigabitEthernet2/0
```

Look for area 0 and a passive indication such as `No Hellos (Passive interface)`.

### 9.2 Expected LAN routes

With all links healthy and equal default Gigabit interface costs:

| Router | Remote LAN | Expected next hop | Exit interface |
|---|---|---|---|
| R1 | `200.100.10.0/24` | `10.10.10.1` | `Gi0/0` |
| R1 | `200.100.30.0/24` | `10.10.10.6` | `Gi1/0` |
| R2 | `200.100.20.0/24` | `10.10.10.2` | `Gi0/0` |
| R2 | `200.100.30.0/24` | `10.10.10.10` | `Gi1/0` |
| R3 | `200.100.10.0/24` | `10.10.10.9` | `Gi0/0` |
| R3 | `200.100.20.0/24` | `10.10.10.5` | `Gi1/0` |

Illustrative excerpt from R2; timers and formatting vary:

```text
O    200.100.20.0/24 [110/2] via 10.10.10.2, 00:00:18, GigabitEthernet0/0
O    200.100.30.0/24 [110/2] via 10.10.10.10, 00:00:18, GigabitEthernet1/0
```

`O` means an intra-area OSPF route. In `[110/2]`, `110` is the default administrative distance and `2` is the example path cost. Cost 2 assumes cost 1 on the transit interface and cost 1 on the destination LAN interface; inspect actual costs with `show ip ospf interface`.

Each router's own LAN remains a **connected (`C`)** route. The third, nonattached router-link subnet is also learned through OSPF and may have two equal-cost next hops. The table above intentionally lists only remote LAN routes.

### 9.3 Database check

In `show ip ospf database`, look for area 0 router LSAs associated with `1.1.1.1`, `2.2.2.2`, and `3.3.3.3`. Broadcast transit links can also produce network LSAs. A populated database is useful evidence, but remote routes and successful traffic tests are still required.

## 10. Test end-to-end connectivity

Run the following from the PC command prompts:

| Source | Local gateway | First remote PC | Second remote PC |
|---|---|---|---|
| PC0 | `ping 200.100.10.1` | `ping 200.100.20.5` | `ping 200.100.30.5` |
| PC1 | `ping 200.100.20.1` | `ping 200.100.10.5` | `ping 200.100.30.5` |
| PC2 | `ping 200.100.30.1` | `ping 200.100.10.5` | `ping 200.100.20.5` |

Repeat after convergence and ARP resolution if necessary. All six directed remote-PC tests should receive replies.

On PC0, inspect the path to PC2:

```text
tracert 200.100.30.5
```

With default equal link costs, the expected router path is **PC0 → R2 → R3 → PC2**. Displayed hop IPs can vary with the interface used to generate each ICMP response. On a router, the equivalent command is `traceroute 200.100.30.5`.

Optional: in Packet Tracer **Simulation** mode, filter for ARP, ICMP, and OSPF, then generate traffic and use Capture/Forward to inspect forwarding. Return to Realtime mode for ordinary convergence testing.

## 11. Test automatic failover

This test deliberately shuts the **R2–R3 transit link**, leaving both LAN gateways active.

### 11.1 Record the baseline

On R2:

```ios
show ip ospf neighbor
show ip route 200.100.30.0
```

Confirm two FULL neighbors and the next hop `10.10.10.10` for VLAN 30. On PC0, ping and trace to `200.100.30.5` as above.

### 11.2 Shut the direct link

On **R2 only**:

```ios
configure terminal
interface gigabitEthernet1/0
 shutdown
end
```

Do not save the shutdown state. Allow OSPF to converge, then run on R2:

```ios
show ip ospf neighbor
show ip route 200.100.30.0
```

Repeat on PC0:

```text
ping 200.100.30.5
tracert 200.100.30.5
```

**Expected after convergence:**

- R2 retains R1 as its only FULL neighbor. R3 also retains only R1; R1 still has both neighbors.
- R2 learns VLAN 30 through `10.10.10.2` on `Gi0/0`.
- Traffic follows **PC0 → R2 → R1 → R3 → PC2**.
- With cost 1 on each participating interface, the example route becomes `[110/3]`.
- Pings recover after a possible interruption. A detected physical link-down can be handled faster than a failure detected by the OSPF dead timer; exact timing depends on the simulation.

### 11.3 Restore the link

On R2:

```ios
configure terminal
interface gigabitEthernet1/0
 no shutdown
end
```

Wait for the R2–R3 adjacency to return to FULL. Verify two neighbors on each router, the direct R2 next hop `10.10.10.10`, and successful PC0-to-PC2 traffic again.

> [!important] Redundancy boundary
> The triangle provides an alternate route around a single transit-link failure. Each LAN still has only one gateway router and one uplink. OSPF cannot keep that LAN connected if its gateway router or sole LAN link fails.

## 12. Troubleshooting

Work from local connectivity toward routing. Recheck the exact addressing and cable endpoints before changing protocol settings.

| Symptom | Check | Corrective action |
|---|---|---|
| Interface is `administratively down` | `show ip interface brief` | Enter the correct interface and apply `no shutdown`. |
| Interface is down despite `no shutdown` | Cable endpoints, module, power, far-end port | Correct the physical connection and enable the far end. |
| Router reports overlapping networks | Interface IP addresses and masks | Use `/30` on all three transit subnets; `/24` would overlap them. |
| PC cannot ping its gateway | PC `ipconfig`; switch `show vlan brief` | Correct the PC mask/gateway and place both switch ports in the intended access VLAN. |
| Direct neighbor ping fails | Port mapping and both endpoint addresses | Correct the `/30` IP pair and verify `up/up` before OSPF. |
| No OSPF neighbors | `show ip protocols`; `show ip ospf interface` | Check network statements, area 0, nonpassive transit interfaces, matching Hello/dead timers, and matching authentication settings on both ends. |
| Neighbor remains in INIT | Both ends' configuration and traffic filtering | Check bidirectional Hellos and any ACL blocking OSPF, which uses IP protocol 89. |
| Neighbor stuck in EXSTART/EXCHANGE | Router IDs, interface MTU, network type | Give each router a unique ID and align link settings, including MTU. |
| Persistent 2-WAY on a two-router link | OSPF interface priority and DR/BDR state | With this default design, expect FULL. If both priorities were set to 0, restore the default priority 1 and allow an election. |
| FULL neighbors but missing remote LAN | Advertising router's LAN status and OSPF network statement | Enable/address `Gi2/0` and include its `/24`; keeping it passive is correct. |
| Static route appears instead of `O` | `show running-config`; `show ip route` | Remove the exact obsolete static route if the lab should use OSPF for that prefix. |
| Routes exist but remote PC ping fails | Destination PC, switch VLAN, return route, ACLs | Check the destination gateway and test in both directions. |
| First ping fails, later ones work | Repeat after ARP and convergence | A single initial timeout can be normal; persistent loss needs investigation. |
| Failover does not work | Remaining two links and neighbor states | Verify R2–R1 and R1–R3 are FULL and neither surviving transit interface is passive. |

### Useful inspection commands

```ios
show running-config
show ip interface brief
show interfaces gigabitEthernet0/0
show ip ospf interface gigabitEthernet0/0
show ip ospf neighbor
show ip protocols
show ip route
```

Repeat interface-specific commands for `Gi1/0` or `Gi2/0` as needed. If a Packet Tracer image rejects an optional command variation, use the broader command, such as `show ip ospf interface` or `show ip route`.

### Example: accidentally passive transit interface

If R2 `Gi1/0` is passive, fix it on R2:

```ios
configure terminal
router ospf 1
 no passive-interface gigabitEthernet1/0
end
```

Also verify the other end: R3 `Gi0/0` must be nonpassive.

### Example: router ID was changed after OSPF started

Check the active ID using `show ip ospf`. On IOS images that require a process restart to apply a changed ID, use this only on the affected router after correcting its `router-id`:

```ios
clear ip ospf process
```

Answer `yes` if prompted. This temporarily drops that router's OSPF adjacencies; wait for FULL and verify routes again. It is not a routine first troubleshooting step.

## 13. Save and completion checklist

After restoring all links, run on **all three routers and all three switches**:

```ios
copy running-config startup-config
```

Press Enter to accept the destination filename if prompted. Also save the Packet Tracer project with **File → Save As**, for example `Three-Router OSPF Lab.pkt`. Saving IOS configuration and saving the Packet Tracer project are separate actions.

- [ ] Physical ports match the diagram.
- [ ] All nine router interfaces have the planned IP addresses and masks.
- [ ] All used router interfaces are `up/up`.
- [ ] Each switch's PC port and router uplink share the correct access VLAN.
- [ ] Each PC has its `.5` address, `/24` mask, and `.1` gateway.
- [ ] All local gateway and direct router-neighbor pings succeed.
- [ ] Router IDs are unique and all OSPF interfaces are in area 0.
- [ ] Each router has two FULL neighbors with all links healthy.
- [ ] Each router advertises its passive LAN and learns the other two LANs through OSPF.
- [ ] All six remote-PC ping tests succeed.
- [ ] R2–R3 link failure reroutes PC0–PC2 traffic through R1.
- [ ] The direct link is restored and the original route returns.
- [ ] Device startup configurations and the `.pkt` project are saved.

## 14. Related notes and references

### In this vault

- [[OSPF - Open Shortest Path First]]
- [[OSPF Single Area]]
- [[OSPF Neighbourship]]
- [[OSPF Router ID]]
- [[OSPF Cost]]
- [[OSPF DR and BDR]]
- [[OSPF Troubleshooting]]
- [[Cisco Packet Tracer – Three-Router Static Routing Lab]] — compare configuration approaches; its transit address plan differs from this diagram.

### Cisco documentation

- [OSPF interface output, network types, cost, and neighbor state](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13689-17.html)
- [OSPF commands, including network area and router-id](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-i1.html)
- [Default passive interfaces and OSPF configuration examples](https://www.cisco.com/c/en/us/td/docs/routers/ios-xe/ip-routing/b-ip-routing/m_iri-default-passive-interface.html)

The linked IOS/IOS XE documentation explains command behavior; availability and output details depend on the router model and IOS subset simulated by Packet Tracer.
