---
title: Configure STP in Cisco Packet Tracer
aliases:
  - Cisco Packet Tracer STP Configuration
  - Packet Tracer Spanning Tree Lab
type: lab
status: complete
area: Networking
vendor: Cisco
platform: Cisco Packet Tracer
protocol: Rapid PVST+
difficulty: intermediate
keywords:
  - Cisco IOS
  - Cisco Packet Tracer
  - spanning tree configuration
  - root bridge
  - redundant links
  - PortFast
  - BPDU Guard
  - Rapid PVST+
tags:
  - networking/stp
  - cisco/packet-tracer
  - switching
  - lab
created: 2026-08-11
updated: 2026-08-11
prerequisites:
  - "[[STP]]"
related:
  - "[[Network Monitoring]]"
  - "[[HSRP]]"
category: "Packet Tracer Labs"
packet_tracer_supported: "Yes"
related_protocols: []
---

# Configure STP in Cisco Packet Tracer

> [!abstract]
> Build a redundant three-switch topology, configure Rapid PVST+ for VLAN 10, select Switch1 as root and Switch2 as backup root, protect endpoint ports, and verify reconvergence after a link failure.

> [!note] Packet Tracer limitation
> Packet Tracer simulates a subset of Cisco spanning-tree behavior. Interface labels, transition timing, and supported verification commands can vary by switch model and version.

## 1. Learning objectives

After this lab, you should be able to:

- Build a redundant Layer 2 topology without creating a forwarding loop.
- Configure Rapid PVST+ consistently on three switches.
- Select a deterministic root bridge and backup root.
- Identify root, designated, and alternate ports.
- Protect endpoint-facing ports with PortFast and BPDU Guard.
- Verify traffic reconverges after the active path fails.

## 2. Prerequisites

- Basic Cisco IOS switch configuration.
- VLAN and trunk fundamentals.
- IPv4 addressing and ping testing.
- Familiarity with [[STP|STP concepts]].

## 3. Topology

```text
                       Switch1
                    Root for VLAN 10
                    Priority: 24576
                   F0/1       F0/2
                     /           \
                    /             \
                   /               \
              F0/1                 F0/1
          +----------+           +----------+
          | Switch2  |-----------| Switch3  |
          | Backup   | F0/2 F0/2 | Default  |
          | Pri 28672|           | Pri 32768|
          +-----+----+           +-----+----+
              F0/10                  F0/10
                |                      |
           +----+-----+           +----+-----+
           | PC1      |           | PC2      |
           | .10.11   |           | .10.12   |
           +----------+           +----------+

All switch-to-switch links: VLAN 10 trunks
PC-facing ports: VLAN 10 access ports
```

## 4. Port and addressing plan

### Switch links

| Link | First port | Second port | Mode |
|---|---|---|---|
| Switch1 to Switch2 | `Switch1 F0/1` | `Switch2 F0/1` | Trunk |
| Switch1 to Switch3 | `Switch1 F0/2` | `Switch3 F0/1` | Trunk |
| Switch2 to Switch3 | `Switch2 F0/2` | `Switch3 F0/2` | Trunk |
| PC1 to Switch2 | `Switch2 F0/10` | `PC1 FastEthernet0` | Access VLAN 10 |
| PC2 to Switch3 | `Switch3 F0/10` | `PC2 FastEthernet0` | Access VLAN 10 |

### Endpoint addressing

| Device | IPv4 address | Subnet mask | Default gateway |
|---|---|---|---|
| `PC1` | `192.168.10.11` | `255.255.255.0` | Blank |
| `PC2` | `192.168.10.12` | `255.255.255.0` | Blank |

No router is required because both PCs are in the same VLAN and subnet.

## 5. Build the topology

1. Add three Cisco 2960 switches or another supported Layer 2 model.
2. Add two PCs.
3. Connect the switches in a triangle using the port plan above.
4. Use **Automatic Connection** or copper crossover cables between switches.
5. Use copper straight-through cables from the PCs to their switches.
6. Wait for all physical links to become active.

> [!warning]
> Do not disable spanning tree. The triangle contains a physical Layer 2 loop, and STP must keep one redundant path from forwarding.

## 6. Configure Switch1

Switch1 will become the root bridge for VLAN 10.

```cisco
enable
configure terminal
hostname Switch1

spanning-tree mode rapid-pvst

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 2
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit

spanning-tree vlan 10 priority 24576

end
copy running-config startup-config
```

### Switch1 purpose

| Setting | Purpose |
|---|---|
| Rapid PVST+ | Use rapid per-VLAN convergence |
| VLAN 10 | Carry the user LAN through all three switches |
| F0/1 and F0/2 trunks | Connect Switch1 to both downstream switches |
| Priority `24576` | Make Switch1 the intended VLAN 10 root |

## 7. Configure Switch2

Switch2 will be the planned backup root and will connect PC1.

```cisco
enable
configure terminal
hostname Switch2

spanning-tree mode rapid-pvst

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 2
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit

interface fastEthernet 0/10
 description PC1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit

spanning-tree vlan 10 priority 28672

end
copy running-config startup-config
```

Switch2's priority is higher than Switch1's but lower than the default `32768`, making it the preferred backup root.

## 8. Configure Switch3

Switch3 keeps the default priority and connects PC2.

```cisco
enable
configure terminal
hostname Switch3

spanning-tree mode rapid-pvst

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 2
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit

interface fastEthernet 0/10
 description PC2
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit

end
copy running-config startup-config
```

## 9. Configure PC1 and PC2

### PC1

Open **PC1 > Desktop > IP Configuration**:

| Setting | Value |
|---|---|
| IP address | `192.168.10.11` |
| Subnet mask | `255.255.255.0` |
| Default gateway | Leave blank |

### PC2

Open **PC2 > Desktop > IP Configuration**:

| Setting | Value |
|---|---|
| IP address | `192.168.10.12` |
| Subnet mask | `255.255.255.0` |
| Default gateway | Leave blank |

## 10. Verify VLANs and trunks

Run on all switches:

```cisco
show vlan brief
show interfaces trunk
```

Confirm:

- VLAN 10 exists on every switch.
- Each switch-to-switch link is trunking.
- VLAN 10 is allowed and active on the trunks.
- `F0/10` is an access port in VLAN 10 on Switch2 and Switch3.

## 11. Verify the root bridge

Run on Switch1:

```cisco
show spanning-tree vlan 10
```

Look for wording similar to:

```text
This bridge is the root
```

Switch1's root ID and bridge ID should match.

Run the same command on Switch2 and Switch3. Their **Root ID** should identify Switch1.

## 12. Verify expected port roles

### Switch1

Both trunk ports should be designated and forwarding:

```text
F0/1  Designated  Forwarding
F0/2  Designated  Forwarding
```

### Switch2

The direct link to Switch1 should be the root port. Switch2 should win the designated role on the Switch2-Switch3 segment because its bridge priority is lower than Switch3's:

```text
F0/1  Root        Forwarding
F0/2  Designated  Forwarding
```

### Switch3

The direct link to Switch1 should be the root port. The link to Switch2 should be alternate and non-forwarding:

```text
F0/1  Root        Forwarding
F0/2  Alternate   Discarding or Blocking
```

> [!note]
> Packet Tracer output can abbreviate these values as `Root FWD`, `Desg FWD`, and `Altn BLK`.

## 13. Test endpoint connectivity

Open **PC1 > Desktop > Command Prompt**:

```text
ping 192.168.10.12
```

The first ping can fail while ARP and switch MAC tables are populated. Repeat it if necessary.

Expected active path:

```text
PC1 --> Switch2 --> Switch1 --> Switch3 --> PC2

Switch2 -------- blocked/discarding at Switch3 F0/2 -------- Switch3
```

## 14. Inspect PortFast and BPDU Guard

On Switch2 and Switch3:

```cisco
show running-config interface fastEthernet 0/10
show spanning-tree interface fastEthernet 0/10 detail
```

Confirm that the PC-facing port has PortFast and BPDU Guard enabled.

> [!warning]
> Never configure PortFast on the three normal switch-to-switch trunk links in this lab.

## 15. Test redundant-path reconvergence

The current Switch3 root port is `F0/1`, which connects directly to Switch1. Shut that interface from Switch3's CLI:

```cisco
configure terminal
interface fastEthernet 0/1
 shutdown
end
```

Allow spanning tree to reconverge, then run:

```cisco
show spanning-tree vlan 10
```

Expected Switch3 change:

```text
Before failure:
F0/1  Root       Forwarding
F0/2  Alternate  Discarding

After failure:
F0/1  Down
F0/2  Root       Forwarding
```

The new path becomes:

```text
PC2 --> Switch3 --> Switch2 --> Switch1
```

## 16. Test connectivity after failure

From PC1:

```text
ping 192.168.10.12
```

Connectivity should recover through the Switch2-Switch3 link. A small number of packets can be lost while the topology changes.

Use **Fast Forward Time** if Packet Tracer has not completed the transition.

## 17. Restore the preferred topology

On Switch3:

```cisco
configure terminal
interface fastEthernet 0/1
 no shutdown
end
```

Wait for reconvergence and verify:

```cisco
show spanning-tree vlan 10
```

Switch3 should return to:

```text
F0/1  Root        Forwarding
F0/2  Alternate   Discarding or Blocking
```

Test the PC-to-PC ping again.

## 18. Optional BPDU Guard test

This test intentionally places a protected port into an error-disabled state.

1. Save the Switch2 configuration.
2. Disconnect PC1 from `Switch2 F0/10`.
3. Connect another switch to `Switch2 F0/10`.
4. Allow the new switch to send BPDUs.
5. Check Switch2:

```cisco
show interfaces status
show interfaces fastEthernet 0/10
```

The protected port should become error-disabled when BPDU Guard detects a BPDU.

Recover the port after reconnecting PC1:

```cisco
configure terminal
interface fastEthernet 0/10
 shutdown
 no shutdown
end
```

> [!note]
> Packet Tracer's BPDU Guard simulation can vary by switch model. If the port does not disable, confirm the configuration and treat this as a conceptual extension.

## 19. Troubleshooting

### The wrong switch becomes root

- [ ] Confirm Switch1 priority is `24576` for VLAN 10.
- [ ] Confirm VLAN 10 exists and is active on Switch1.
- [ ] Confirm all switches use the same spanning-tree mode.
- [ ] Run `show spanning-tree vlan 10` on every switch.

Correct Switch1 if necessary:

```cisco
configure terminal
spanning-tree vlan 10 priority 24576
end
```

### No port is alternate or blocking

- [ ] Confirm all three switch-to-switch links are physically connected.
- [ ] Confirm all three links are trunks carrying VLAN 10.
- [ ] Confirm VLAN 10 exists on every switch.
- [ ] Check whether one interface is down or error-disabled.

In a healthy triangle, STP must prevent one path from forwarding for VLAN 10.

### PC1 cannot ping PC2

- [ ] Confirm both PCs use `192.168.10.0/24` addresses.
- [ ] Confirm both PC ports are access ports in VLAN 10.
- [ ] Confirm VLAN 10 is allowed on every trunk.
- [ ] Check the active STP path with `show spanning-tree vlan 10`.
- [ ] Repeat the ping after ARP completes.

### A trunk does not carry VLAN 10

```cisco
configure terminal
interface fastEthernet 0/1
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
end
```

Apply the correction to the actual affected trunk port.

### An access port is error-disabled

Check whether BPDU Guard detected a BPDU:

```cisco
show interfaces status
show logging
```

Remove the unauthorized switch or loop before recovering the port with `shutdown` followed by `no shutdown`.

### STP commands are unavailable

Use contextual help:

```cisco
spanning-tree ?
show spanning-tree ?
```

If necessary, use a Cisco 2960 switch or another Packet Tracer model that supports the required commands.

## 20. Complete configurations

### Switch1

```cisco
enable
configure terminal
hostname Switch1
spanning-tree mode rapid-pvst

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 2
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit

spanning-tree vlan 10 priority 24576

end
copy running-config startup-config
```

### Switch2

```cisco
enable
configure terminal
hostname Switch2
spanning-tree mode rapid-pvst

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 2
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit

interface fastEthernet 0/10
 description PC1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit

spanning-tree vlan 10 priority 28672

end
copy running-config startup-config
```

### Switch3

```cisco
enable
configure terminal
hostname Switch3
spanning-tree mode rapid-pvst

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 2
 switchport mode trunk
 switchport trunk allowed vlan 10
 no shutdown
exit

interface fastEthernet 0/10
 description PC2
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit

end
copy running-config startup-config
```

## 21. Completion checklist

- [ ] VLAN 10 exists on all three switches.
- [ ] All switch links are trunks carrying VLAN 10.
- [ ] Switch1 is root with priority `24576`.
- [ ] Switch2 is the preferred backup root with priority `28672`.
- [ ] Switch3 has one alternate/discarding trunk port.
- [ ] PC-facing ports use PortFast and BPDU Guard.
- [ ] PC1 can ping PC2.
- [ ] Switch3's alternate link forwards after its root port fails.
- [ ] The preferred topology returns after the link is restored.
- [ ] All configurations are saved.

## 22. Key takeaways

- STP blocks redundant Layer 2 paths to prevent switching loops.
- The lowest bridge ID becomes the root bridge.
- Root bridge placement should be configured intentionally.
- Rapid PVST+ provides a separate rapid tree for each VLAN.
- PortFast and BPDU Guard belong on endpoint-facing access ports.
- An alternate path becomes active when the preferred path fails.

## 23. References

- [Cisco STP configuration guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/stp/stp-configuration-guide/m-stp.html)
- [Cisco PortFast and BPDU Guard guidance](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10586-65.html)

---

**Parent:** [[STP|Spanning Tree Protocol Overview]]  
**Home:** [[Networking Dashboard]]
