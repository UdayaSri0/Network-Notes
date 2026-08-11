---
title: Configure HSRP in Cisco Packet Tracer
aliases:
  - Cisco Packet Tracer HSRP Configuration
  - Packet Tracer HSRP Lab
type: lab
status: complete
area: Networking
vendor: Cisco
platform: Cisco Packet Tracer
protocol: HSRP
difficulty: intermediate
keywords:
  - Cisco IOS
  - Cisco Packet Tracer
  - HSRP configuration
  - first-hop redundancy
  - virtual gateway
  - active router
  - standby router
  - preempt
tags:
  - networking/hsrp
  - cisco/packet-tracer
  - redundancy
  - lab
created: 2026-08-11
updated: 2026-08-11
prerequisites:
  - "[[HSRP]]"
related:
  - "[[Network Monitoring]]"
category: "Packet Tracer Labs"
packet_tracer_supported: "Yes"
related_protocols: []
---

# Configure HSRP in Cisco Packet Tracer

> [!abstract]
> Configure two Cisco routers to provide the shared virtual gateway `192.168.10.1`. Router1 will normally be active, Router2 will be standby, and Router2 will take over when Router1 fails.

> [!note] Packet Tracer limitation
> Packet Tracer simulates a subset of HSRP and Cisco IOS. Use router models that accept the `standby` interface command; available verification commands may vary.

## 1. Learning objectives

After this lab, you should be able to:

- Build an HSRP topology with two routers and one access LAN.
- Configure a shared virtual default gateway.
- Control active-router selection with priority.
- Restore the preferred router with preemption.
- Verify HSRP roles and test gateway failover.
- Diagnose common group, VLAN, and addressing mistakes.

## 2. Prerequisites

- Basic Cisco IOS CLI navigation.
- IPv4 addressing and subnetting.
- Basic switch access-port configuration.
- Familiarity with [[HSRP|HSRP concepts]].

## 3. Topology

```text
                         HSRP group 1
                    Virtual IP: 192.168.10.1
                              |
               +--------------+--------------+
               |                             |
        G0/0   |                      G0/0   |
   192.168.10.2/24               192.168.10.3/24
      Priority 110                  Priority 100
   +----------------+             +----------------+
   | Router1        |             | Router2        |
   | Preferred      |             | Backup         |
   | Active         |             | Standby        |
   +-------+--------+             +--------+-------+
           | F0/2                          | F0/3
           +---------------+---------------+
                           |
                    +------+-------+
                    | Switch0      |
                    | VLAN 10      |
                    +------+-------+
                           | F0/1
                    +------+-------+
                    | PC0          |
                    | 192.168.10.10|
                    | GW: .10.1    |
                    +--------------+
```

## 4. Addressing plan

| Device | Interface | IPv4 address | Mask | Purpose |
|---|---|---|---|---|
| HSRP group 1 | Virtual | `192.168.10.1` | `255.255.255.0` | PC default gateway |
| `Router1` | `G0/0` | `192.168.10.2` | `255.255.255.0` | Preferred active router |
| `Router2` | `G0/0` | `192.168.10.3` | `255.255.255.0` | Standby router |
| `PC0` | `FastEthernet0` | `192.168.10.10` | `255.255.255.0` | Test endpoint |

> [!important]
> The two physical router addresses and the virtual IP must be unique addresses in the same subnet.

## 5. Cable and switch-port plan

| Connection | Switch port | Cable |
|---|---|---|
| `PC0 FastEthernet0` to `Switch0` | `F0/1` | Copper straight-through |
| `Router1 G0/0` to `Switch0` | `F0/2` | Copper straight-through |
| `Router2 G0/0` to `Switch0` | `F0/3` | Copper straight-through |

Use two routers that support the `standby` command, such as a supported Packet Tracer ISR model.

## 6. Configure Switch0

Open **Switch0 > CLI**, then enter:

```cisco
enable
configure terminal
hostname Switch0

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 3
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
exit

end
copy running-config startup-config
```

> [!tip]
> If different switch ports were used, replace `fastEthernet 0/1 - 3` with the actual connected ports.

Verify VLAN membership:

```cisco
show vlan brief
```

Ports `F0/1`, `F0/2`, and `F0/3` should appear in VLAN 10.

## 7. Configure Router1 addressing

Open **Router1 > CLI**, then enter:

```cisco
enable
configure terminal
hostname Router1

interface gigabitEthernet 0/0
 description HSRP-LAN
 ip address 192.168.10.2 255.255.255.0
 no shutdown
exit
end
```

Verify the interface:

```cisco
show ip interface brief
```

`GigabitEthernet0/0` should eventually show `up/up`.

## 8. Configure Router2 addressing

Open **Router2 > CLI**, then enter:

```cisco
enable
configure terminal
hostname Router2

interface gigabitEthernet 0/0
 description HSRP-LAN
 ip address 192.168.10.3 255.255.255.0
 no shutdown
exit
end
```

Verify the interface:

```cisco
show ip interface brief
```

## 9. Test physical-address connectivity

From Router1:

```cisco
ping 192.168.10.3
```

From Router2:

```cisco
ping 192.168.10.2
```

Do not configure HSRP until the routers can ping each other.

> [!tip]
> The first ping can fail while ARP resolves the destination MAC address. Repeat it before troubleshooting further.

## 10. Configure HSRP on Router1

Router1 will be the preferred active router because it receives priority `110`.

```cisco
configure terminal
interface gigabitEthernet 0/0
 standby 1 ip 192.168.10.1
 standby 1 priority 110
 standby 1 preempt
exit
end
```

### Router1 command explanation

| Command | Purpose |
|---|---|
| `standby 1 ip 192.168.10.1` | Create HSRP group 1 with virtual IP `.1` |
| `standby 1 priority 110` | Make Router1 preferable to the default priority of 100 |
| `standby 1 preempt` | Let Router1 reclaim the active role after recovery |

## 11. Configure HSRP on Router2

Router2 will start with priority `100` and should become the standby router.

```cisco
configure terminal
interface gigabitEthernet 0/0
 standby 1 ip 192.168.10.1
 standby 1 priority 100
 standby 1 preempt
exit
end
```

> [!note]
> Preemption on Router2 is not required for the basic two-router failure test, but it keeps the behavior explicit if priorities or tracked objects are changed later.

## 12. Wait for HSRP convergence

Allow several seconds of simulation time for the election to finish. Use **Fast Forward Time** in Packet Tracer if necessary.

Expected roles:

```text
Router1: Active  - priority 110
Router2: Standby - priority 100
```

## 13. Verify HSRP status

Run on both routers:

```cisco
show standby brief
show standby
```

### Expected Router1 summary

```text
Interface   Grp  Pri  P  State   Active  Standby       Virtual IP
Gi0/0       1    110  P  Active  local   192.168.10.3  192.168.10.1
```

### Expected Router2 summary

```text
Interface   Grp  Pri  P  State    Active        Standby  Virtual IP
Gi0/0       1    100  P  Standby  192.168.10.2  local    192.168.10.1
```

The exact columns and interface abbreviation can differ in Packet Tracer.

## 14. Configure PC0

Open **PC0 > Desktop > IP Configuration**, then enter:

| Setting | Value |
|---|---|
| IP address | `192.168.10.10` |
| Subnet mask | `255.255.255.0` |
| Default gateway | `192.168.10.1` |

> [!warning]
> Do not use `192.168.10.2` or `192.168.10.3` as the PC gateway. Endpoints must use the HSRP virtual IP `192.168.10.1`.

## 15. Test the virtual gateway

Open **PC0 > Desktop > Command Prompt**, then run:

```text
ping 192.168.10.1
ping 192.168.10.2
ping 192.168.10.3
```

All three addresses should respond.

Optional ARP inspection:

```text
arp -a
```

For HSRPv1 group 1, the virtual MAC commonly ends in `ac01`. Packet Tracer may not display the virtual entry consistently.

## 16. Test active-router failure

Keep Router1's CLI available, then shut down its LAN interface:

```cisco
configure terminal
interface gigabitEthernet 0/0
 shutdown
end
```

Allow HSRP time to converge, then check Router2:

```cisco
show standby brief
```

Expected result:

```text
Router2 state: Active
Active router: local
Virtual IP: 192.168.10.1
```

From PC0, test the same gateway again:

```text
ping 192.168.10.1
```

The virtual gateway should respond through Router2. A small number of packets can be lost during failover.

## 17. Restore the preferred router

On Router1:

```cisco
configure terminal
interface gigabitEthernet 0/0
 no shutdown
end
```

Wait for convergence and verify both routers:

```cisco
show standby brief
```

Because Router1 has the higher priority and `preempt` is configured, the roles should return to:

```text
Router1: Active
Router2: Standby
```

## 18. Optional upstream-interface tracking

The basic failure test shuts down Router1's LAN interface. In a real network, the LAN interface might stay up while Router1 loses its upstream connection. HSRP tracking can reduce Router1's priority in that condition.

Only use this extension after adding and enabling a real upstream link on `G0/1`:

```cisco
configure terminal
interface gigabitEthernet 0/0
 standby 1 track gigabitEthernet 0/1 20
end
```

Priority calculation after the tracked link fails:

```text
Router1 normal priority:       110
Tracking decrement:           -20
Router1 priority after fault:   90
Router2 priority:              100

Result: Router2 becomes preferred.
```

> [!warning]
> Do not track an unused or permanently down interface. Doing so keeps the priority reduced.

## 19. Save all configurations

Run on Router1 and Router2:

```cisco
copy running-config startup-config
```

Press **Enter** to accept the default destination filename.

## 20. Troubleshooting

### The `standby` command is missing

Use interface configuration mode and check contextual help:

```cisco
interface gigabitEthernet 0/0
standby ?
```

If the command is unavailable, select another Packet Tracer router model that supports HSRP.

### Both routers report Active

- [ ] Confirm the routers are connected to the same switch VLAN.
- [ ] Confirm both LAN interfaces are `up/up`.
- [ ] Confirm both sides use HSRP group `1`.
- [ ] Confirm both sides use compatible HSRP versions.
- [ ] Check for an authentication mismatch if authentication was added.
- [ ] Verify the switch ports are not isolated or placed in different VLANs.

This condition indicates that the routers are not hearing one another's HSRP messages.

### HSRP remains in Initial state

- [ ] Run `show ip interface brief`.
- [ ] Apply `no shutdown` to the LAN interface.
- [ ] Confirm a working cable connects the interface to Switch0.
- [ ] Confirm the interface has the intended IP address and mask.

### Router2 becomes Active first

This can happen if Router2 starts before Router1. After Router1 joins, `standby 1 preempt` should let its higher priority take over.

Check:

```cisco
show standby brief
show running-config interface gigabitEthernet 0/0
```

### PC0 cannot reach the virtual gateway

- [ ] Confirm PC0 is in `192.168.10.0/24`.
- [ ] Confirm PC0's gateway is `192.168.10.1`.
- [ ] Confirm Switch0 port `F0/1` is in VLAN 10.
- [ ] Confirm at least one router reports `Active`.
- [ ] Ping both physical router addresses to isolate the fault.

### Router1 does not reclaim Active after recovery

Confirm Router1 has both the higher priority and preemption:

```cisco
standby 1 priority 110
standby 1 preempt
```

## 21. Complete configurations

### Switch0

```cisco
enable
configure terminal
hostname Switch0

vlan 10
 name USERS
exit

interface range fastEthernet 0/1 - 3
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
exit

end
copy running-config startup-config
```

### Router1

```cisco
enable
configure terminal
hostname Router1

interface gigabitEthernet 0/0
 description HSRP-LAN
 ip address 192.168.10.2 255.255.255.0
 standby 1 ip 192.168.10.1
 standby 1 priority 110
 standby 1 preempt
 no shutdown
exit

end
copy running-config startup-config
```

### Router2

```cisco
enable
configure terminal
hostname Router2

interface gigabitEthernet 0/0
 description HSRP-LAN
 ip address 192.168.10.3 255.255.255.0
 standby 1 ip 192.168.10.1
 standby 1 priority 100
 standby 1 preempt
 no shutdown
exit

end
copy running-config startup-config
```

## 22. Completion checklist

- [ ] All three switch ports are access ports in VLAN 10.
- [ ] Router1 and Router2 can ping each other.
- [ ] Both routers use group `1` and virtual IP `192.168.10.1`.
- [ ] Router1 is Active with priority `110`.
- [ ] Router2 is Standby with priority `100`.
- [ ] PC0 uses `192.168.10.1` as its default gateway.
- [ ] Router2 becomes Active when Router1's LAN interface fails.
- [ ] Router1 reclaims Active after recovery.
- [ ] All configurations are saved.

## 23. Key takeaways

- HSRP gives endpoints one virtual default gateway backed by multiple routers.
- Higher priority wins the active-router election; the default priority is `100`.
- Preemption allows a recovered higher-priority router to reclaim Active.
- Both routers must share a Layer 2 segment, group number, and virtual IP.
- Interface or object tracking detects failures beyond the local LAN interface.

## 24. References

- [Cisco: HSRP configuration guide](https://www.cisco.com/c/en/us/td/docs/routers/ios-xe/network-services/network-services/m_fhp-hsrp-0.html)
- [Cisco: HSRP preemption and interface tracking](https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/13780-6.html)

---

**Parent:** [[HSRP|HSRP Overview]]  
**Home:** [[Networking Dashboard]]
