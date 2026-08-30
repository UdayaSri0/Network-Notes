---
title: HSRP Gateway Redundancy Lab
aliases:
  - Cisco Packet Tracer HSRP Practical
  - HSRP Configuration Guide
tags:
  - networking
  - cisco
  - packet-tracer
  - hsrp
  - first-hop-redundancy
  - static-routing
created: 2026-08-25
---

# HSRP Gateway Redundancy Lab

## Lab objective

Configure a three-router Cisco Packet Tracer network that provides:

- A redundant default gateway for VLANs 10, 20, and 30 using **Hot Standby Router Protocol (HSRP)**.
- Automatic gateway failover when an active router or its forwarding interface fails.
- End-to-end communication between all three LANs.
- Primary and backup static routes between the LANs.
- Verification and failure testing with Cisco IOS commands.

> [!important] HSRP is not a routing protocol
> HSRP protects a host's default gateway. Static routes are still required so that the routers know how to reach remote LANs.

## Starting files

- Packet Tracer file: [[HSRP Gateway Redundancy Lab.pkt]]
- Original diagram: [[HSRP Original Topology.png]]

![[HSRP Original Topology.png]]

> [!warning] The original topology must be rewired
> In the original diagram, each LAN connects to only one router. HSRP requires two or more routers to share the same Layer 2 LAN/VLAN. A routed point-to-point link between two routers is not a redundant gateway for the PCs. Follow the cabling plan below before applying the HSRP configuration.

---

## 1. Corrected topology

Remove the three red router-to-router links. Connect each LAN switch to two routers instead.

```text
                       VLAN 20
                   200.100.20.0/24
                  SW20 ---- PC1
                   /  \
                 R1    R2
                 |      |
                 |      |
       VLAN 30   |      |   VLAN 10
  200.100.30.0   |      |   200.100.10.0
       PC2--SW30 |      | SW10--PC0
              \  |      |  /
                  R3----

Each LAN has two router interfaces and one HSRP virtual gateway.
```

### Cabling plan

| LAN | First connection | Second connection | PC connection |
|---|---|---|---|
| VLAN 10 / SW10 | R2 `Gi2/0` to SW10 `Gi0/1` | R3 `Gi1/0` to SW10 `Gi0/2` | PC0 `Fa0` to SW10 `Fa0/1` |
| VLAN 20 / SW20 | R1 `Gi2/0` to SW20 `Gi0/1` | R2 `Gi1/0` to SW20 `Gi0/2` | PC1 `Fa0` to SW20 `Fa0/1` |
| VLAN 30 / SW30 | R3 `Gi2/0` to SW30 `Gi0/1` | R1 `Gi1/0` to SW30 `Gi0/2` | PC2 `Fa0` to SW30 `Fa0/1` |

Use **Copper Straight-Through** cables. Packet Tracer's automatic cable option is also acceptable.

> [!note]
> The interface names above match the routers in the supplied topology. If a router module uses a different interface name, substitute the interface actually connected in your Packet Tracer file. Confirm it with `show ip interface brief`.

---

## 2. Addressing and HSRP plan

The `.1` address in every LAN is reserved for HSRP. Do not assign it directly to a physical router interface.

| VLAN | Network | HSRP virtual IP | Active router | Standby router | PC |
|---|---|---|---|---|---|
| 10 | `200.100.10.0/24` | `200.100.10.1` | R2 | R3 | `200.100.10.5` |
| 20 | `200.100.20.0/24` | `200.100.20.1` | R1 | R2 | `200.100.20.5` |
| 30 | `200.100.30.0/24` | `200.100.30.1` | R3 | R1 | `200.100.30.5` |

### Router interface addresses

| Router | Interface | LAN | Physical IP address |
|---|---|---|---|
| R1 | `Gi2/0` | VLAN 20 | `200.100.20.2/24` |
| R1 | `Gi1/0` | VLAN 30 | `200.100.30.3/24` |
| R2 | `Gi2/0` | VLAN 10 | `200.100.10.2/24` |
| R2 | `Gi1/0` | VLAN 20 | `200.100.20.3/24` |
| R3 | `Gi1/0` | VLAN 10 | `200.100.10.3/24` |
| R3 | `Gi2/0` | VLAN 30 | `200.100.30.2/24` |

### HSRP groups and priorities

| VLAN | HSRP group | Active priority | Standby priority |
|---|---:|---:|---:|
| 10 | 10 | R2 = `110` | R3 = `100` |
| 20 | 20 | R1 = `110` | R2 = `100` |
| 30 | 30 | R3 = `110` | R1 = `100` |

The router with the highest HSRP priority becomes active. `preempt` allows the preferred router to reclaim the active role after it recovers.

> [!caution]
> The `200.100.x.x` addresses are retained to match the supplied lab. They are not RFC 1918 private addresses and should not be copied into a real production network without an assigned address plan.

---

## 3. Configure the switches

Each switch carries only one VLAN in this practical. The two router ports and the PC port must belong to the same access VLAN.

### SW10

```cisco
enable
configure terminal
hostname SW10

vlan 10
 name USERS_VLAN_10
exit

interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 -
 no shutdown
exit

interface range gigabitEthernet0/1 - 2
 switchport mode access
 switchport access vlan 10
 no shutdown
exit

end
copy running-config startup-config
```

### SW20

```cisco
enable
configure terminal
hostname SW20

vlan 20
 name USERS_VLAN_20
exit

interface fastEthernet0/1
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 no shutdown
exit

interface range gigabitEthernet0/1 - 2
 switchport mode access
 switchport access vlan 20
 no shutdown
exit

end
copy running-config startup-config
```

### SW30

```cisco
enable
configure terminal
hostname SW30

vlan 30
 name USERS_VLAN_30
exit

interface fastEthernet0/1
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 no shutdown
exit

interface range gigabitEthernet0/1 - 2
 switchport mode access
 switchport access vlan 30
 no shutdown
exit

end
copy running-config startup-config
```

Verify each switch:

```cisco
show vlan brief
show interfaces status
```

---

## 4. Configure Router R1

R1 is active for VLAN 20 and standby for VLAN 30.

```cisco
enable
configure terminal
hostname R1

interface gigabitEthernet2/0
 description VLAN20_TO_SW20
 ip address 200.100.20.2 255.255.255.0
 standby 20 ip 200.100.20.1
 standby 20 priority 110
 standby 20 preempt
 standby 20 track gigabitEthernet1/0 20
 no shutdown
exit

interface gigabitEthernet1/0
 description VLAN30_TO_SW30
 ip address 200.100.30.3 255.255.255.0
 standby 30 ip 200.100.30.1
 standby 30 priority 100
 standby 30 preempt
 standby 30 track gigabitEthernet2/0 20
 no shutdown
exit

! Primary route to VLAN 10 through R2 on VLAN 20
ip route 200.100.10.0 255.255.255.0 200.100.20.3

! Floating backup route to VLAN 10 through R3 on VLAN 30
ip route 200.100.10.0 255.255.255.0 200.100.30.2 10

end
copy running-config startup-config
```

---

## 5. Configure Router R2

R2 is active for VLAN 10 and standby for VLAN 20.

```cisco
enable
configure terminal
hostname R2

interface gigabitEthernet2/0
 description VLAN10_TO_SW10
 ip address 200.100.10.2 255.255.255.0
 standby 10 ip 200.100.10.1
 standby 10 priority 110
 standby 10 preempt
 standby 10 track gigabitEthernet1/0 20
 no shutdown
exit

interface gigabitEthernet1/0
 description VLAN20_TO_SW20
 ip address 200.100.20.3 255.255.255.0
 standby 20 ip 200.100.20.1
 standby 20 priority 100
 standby 20 preempt
 standby 20 track gigabitEthernet2/0 20
 no shutdown
exit

! Primary route to VLAN 30 through R1 on VLAN 20
ip route 200.100.30.0 255.255.255.0 200.100.20.2

! Floating backup route to VLAN 30 through R3 on VLAN 10
ip route 200.100.30.0 255.255.255.0 200.100.10.3 10

end
copy running-config startup-config
```

---

## 6. Configure Router R3

R3 is active for VLAN 30 and standby for VLAN 10.

```cisco
enable
configure terminal
hostname R3

interface gigabitEthernet1/0
 description VLAN10_TO_SW10
 ip address 200.100.10.3 255.255.255.0
 standby 10 ip 200.100.10.1
 standby 10 priority 100
 standby 10 preempt
 standby 10 track gigabitEthernet2/0 20
 no shutdown
exit

interface gigabitEthernet2/0
 description VLAN30_TO_SW30
 ip address 200.100.30.2 255.255.255.0
 standby 30 ip 200.100.30.1
 standby 30 priority 110
 standby 30 preempt
 standby 30 track gigabitEthernet1/0 20
 no shutdown
exit

! Primary route to VLAN 20 through R1 on VLAN 30
ip route 200.100.20.0 255.255.255.0 200.100.30.3

! Floating backup route to VLAN 20 through R2 on VLAN 10
ip route 200.100.20.0 255.255.255.0 200.100.10.2 10

end
copy running-config startup-config
```

> [!tip] If interface tracking is unsupported
> Some older Packet Tracer router images may reject `standby <group> track <interface> 20`. HSRP will still handle a complete router failure without tracking. Remove only the rejected tracking line and continue the lab. For correct failover after an upstream-interface failure, choose a router/IOS image that supports HSRP interface tracking.

---

## 7. Configure the PCs

Open each PC and select **Desktop > IP Configuration**.

| PC | IP address | Subnet mask | Default gateway |
|---|---|---|---|
| PC0 / VLAN 10 | `200.100.10.5` | `255.255.255.0` | `200.100.10.1` |
| PC1 / VLAN 20 | `200.100.20.5` | `255.255.255.0` | `200.100.20.1` |
| PC2 / VLAN 30 | `200.100.30.5` | `255.255.255.0` | `200.100.30.1` |

The PC default gateways are the HSRP virtual IPs, not a router's physical `.2` or `.3` address.

---

## 8. Verify the configuration

### Step 1: Check router interfaces

Run on every router:

```cisco
show ip interface brief
```

Every connected interface should be `up/up`.

### Step 2: Check HSRP

Run on every router:

```cisco
show standby brief
show standby
```

Expected active roles:

| VLAN | Expected active | Expected standby | Virtual IP |
|---|---|---|---|
| 10 | R2 | R3 | `200.100.10.1` |
| 20 | R1 | R2 | `200.100.20.1` |
| 30 | R3 | R1 | `200.100.30.1` |

Allow several seconds for HSRP to leave the `Speak` state and elect the active and standby routers.

### Step 3: Check routes

```cisco
show ip route
show ip route static
```

The normal routing table installs the primary static route with administrative distance 1. The floating route with administrative distance 10 remains available as a backup.

### Step 4: Test local virtual gateways

From each PC command prompt:

```text
PC0> ping 200.100.10.1
PC1> ping 200.100.20.1
PC2> ping 200.100.30.1
```

### Step 5: Test end-to-end connectivity

From PC0:

```text
ping 200.100.20.5
ping 200.100.30.5
tracert 200.100.30.5
```

From PC1:

```text
ping 200.100.10.5
ping 200.100.30.5
```

From PC2:

```text
ping 200.100.10.5
ping 200.100.20.5
```

The first one or two pings may time out while ARP and HSRP information is learned. Repeating the test should succeed.

---

## 9. Test HSRP failover

Use a continuous ping from PC0 to PC2:

```text
ping -t 200.100.30.5
```

Then simulate a failed forwarding path on R2:

```cisco
R2# configure terminal
R2(config)# interface gigabitEthernet1/0
R2(config-if)# shutdown
```

What should happen:

1. R2's tracked interface goes down.
2. R2's VLAN 10 HSRP priority falls from 110 to 90.
3. R3, with priority 100, becomes active for VLAN 10.
4. R1's primary route toward VLAN 10 becomes unusable and its floating route through R3 is selected.
5. A few pings may be lost during convergence, after which communication resumes.

Verify on R2 and R3:

```cisco
show standby brief
```

Verify the changed route on R1:

```cisco
show ip route 200.100.10.0
```

Restore the link:

```cisco
R2# configure terminal
R2(config)# interface gigabitEthernet1/0
R2(config-if)# no shutdown
R2(config-if)# end
```

Because `preempt` is configured, R2 should become active for VLAN 10 again after the interface and HSRP state recover.

Other useful failure tests:

- Shut R1 `Gi1/0` to test VLAN 20 moving from R1 to R2.
- Shut R3 `Gi1/0` to test VLAN 30 moving from R3 to R1.
- Power off an active router to test complete-router failure.
- Always restore the interface or router after each test before starting the next one.

---

## 10. How the HSRP commands work

```cisco
standby 10 ip 200.100.10.1
```

Creates HSRP group 10 and assigns its shared virtual gateway address.

```cisco
standby 10 priority 110
```

Sets the router's election priority. The default is 100; the higher value wins.

```cisco
standby 10 preempt
```

Allows a higher-priority router to take back the active role after recovery.

```cisco
standby 10 track gigabitEthernet1/0 20
```

Reduces the HSRP priority by 20 if the tracked forwarding interface fails. In this lab, priority 110 becomes 90, allowing the standby router at priority 100 to take over.

```cisco
ip route 200.100.30.0 255.255.255.0 200.100.20.2
ip route 200.100.30.0 255.255.255.0 200.100.10.3 10
```

The first line is the normal route. The second is a floating static route with administrative distance 10, used when the normal next hop is unavailable.

---

## 11. Troubleshooting

### HSRP routers do not see each other

Check that both HSRP interfaces:

- Connect to the same switch/VLAN.
- Use different physical IP addresses in the same subnet.
- Use the same HSRP group and virtual IP.
- Are `up/up`.

Commands:

```cisco
show ip interface brief
show standby brief
show vlan brief
```

### Both routers appear active

This usually means HSRP hello messages are not crossing the LAN. Check cabling, access VLAN assignments, group numbers, and interface status.

### A PC reaches its gateway but not a remote PC

HSRP is working, but routing may be incomplete. Check:

```cisco
show ip route
show ip route static
ping <next-hop-address>
traceroute <remote-PC-address>
```

Confirm that both the forward path and return path exist.

### The gateway fails when the active router's other interface is shut

Check whether the tracking command was accepted:

```cisco
show standby
show running-config | section interface
```

Without tracking, HSRP may keep a router active when its local HSRP interface is still up even though it can no longer forward to other LANs.

### HSRP works, but the preferred router does not become active again

Confirm `preempt` is configured on the preferred router:

```cisco
standby <group> preempt
```

### Packet Tracer rejects an interface name

Find the installed interfaces:

```cisco
show ip interface brief
```

Then replace the guide's interface name with the actual connected interface.

---

## 12. Completion checklist

- [ ] The three original router-to-router links have been removed.
- [ ] Every LAN switch connects to two routers.
- [ ] All switch ports are assigned to the correct access VLAN.
- [ ] Every router interface uses its unique physical `.2` or `.3` address.
- [ ] The HSRP virtual `.1` address is not assigned as a physical interface address.
- [ ] PC0, PC1, and PC2 use the HSRP virtual IP as their default gateway.
- [ ] `show standby brief` displays one active and one standby router per VLAN.
- [ ] All PCs can ping the other LANs.
- [ ] A failure test causes the standby router to become active.
- [ ] Connectivity returns after HSRP and the floating static route converge.
- [ ] Running configurations are saved.

## Expected result

The PCs always send traffic to a stable `.1` virtual gateway. If the active gateway loses its forwarding path or fails completely, the standby router assumes the same virtual IP and continues forwarding traffic. The floating static routes provide an alternate Layer 3 path between the three LANs.

Obsidian 
