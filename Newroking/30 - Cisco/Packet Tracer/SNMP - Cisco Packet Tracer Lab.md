---
title: Configure SNMP in Cisco Packet Tracer
aliases:
  - Cisco Packet Tracer SNMP Configuration
  - Packet Tracer SNMP Lab
type: lab
status: complete
area: Networking
vendor: Cisco
platform: Cisco Packet Tracer
protocol: SNMPv2c
difficulty: beginner
keywords:
  - Cisco IOS
  - Cisco Packet Tracer
  - SNMP configuration
  - MIB Browser
  - community string
  - network monitoring
tags:
  - networking/snmp
  - cisco/packet-tracer
  - lab
created: 2026-08-11
updated: 2026-08-11
prerequisites:
  - "[[Network Monitoring]]"
  - "[[SNMP - Overview]]"
related:
  - "[[SNMP - Overview]]"
---

# Configure SNMP in Cisco Packet Tracer

> [!abstract]
> Configure a Cisco router as an SNMPv2c agent, use a Packet Tracer PC as the SNMP manager, and query standard system OIDs with the MIB Browser.

> [!note] Packet Tracer limitation
> Packet Tracer simulates a subset of Cisco IOS and SNMP. Available commands can vary by router model and Packet Tracer version.

## 1. Learning objectives

After this lab, you should be able to:

- Explain the manager-agent relationship.
- Configure an SNMPv2c read-only community.
- Configure the device contact and location.
- Query an OID from Packet Tracer's MIB Browser.
- Identify common causes of an SNMP timeout.

## 2. Prerequisites

- Basic Cisco IOS CLI navigation.
- Basic IPv4 addressing and ping testing.
- Familiarity with [[Network Monitoring]] and [[SNMP - Overview|SNMP fundamentals]].

## 3. Topology

```text
             Copper straight-through cable
    FastEthernet0                 GigabitEthernet0/0
+------------------+             +------------------+
| PC0              |-------------| Router0          |
| SNMP Manager     |             | SNMP Agent       |
| 192.168.1.10/24  |             | 192.168.1.1/24   |
+------------------+             +------------------+
```

### Addressing table

| Device | Interface | IPv4 address | Subnet mask | Default gateway |
|---|---|---|---|---|
| `Router0` | `G0/0` | `192.168.1.1` | `255.255.255.0` | N/A |
| `PC0` | `FastEthernet0` | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` |

## 4. Build the topology

1. Add one Cisco router and one PC to the workspace.
2. Connect `PC0 FastEthernet0` to `Router0 GigabitEthernet0/0`.
3. Use a **copper straight-through** cable.

> [!tip]
> Some router models use `FastEthernet0/0`. Run `show ip interface brief` and substitute the interface name shown by your router.

## 5. Configure the router interface

Open **Router0 > CLI**, then enter:

```cisco
enable
configure terminal
hostname Router0

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit
```

Verify the interface:

```cisco
show ip interface brief
```

Expected state for the connected interface:

```text
Status: up
Protocol: up
```

## 6. Configure SNMPv2c

### 6.1 Read-only access

```cisco
snmp-server community PT-RO ro
snmp-server location Network-Lab
snmp-server contact Network-Administrator
```

| Setting | Value | Purpose |
|---|---|---|
| Community | `PT-RO` | Shared SNMPv2c credential |
| Permission | `ro` | Read-only access |
| Location | `Network-Lab` | Physical or logical device location |
| Contact | `Network-Administrator` | Responsible administrator |

> [!important]
> Community strings are case-sensitive. `PT-RO` and `pt-ro` are different values.

### 6.2 Optional read-write access

Only configure this when a lab specifically requires SNMP write access:

```cisco
snmp-server community PT-RW rw
```

> [!warning]
> Read-write access can change supported device values. Prefer read-only access for monitoring labs.

### 6.3 Optional trap destination

Configure the manager PC as a trap destination:

```cisco
snmp-server host 192.168.1.10 version 2c PT-RO
snmp-server enable traps
```

## 7. Save the configuration

```cisco
end
copy running-config startup-config
```

Press **Enter** to accept the default destination filename.

## 8. Configure PC0

Open **PC0 > Desktop > IP Configuration** and enter:

| Setting | Value |
|---|---|
| IP address | `192.168.1.10` |
| Subnet mask | `255.255.255.0` |
| Default gateway | `192.168.1.1` |

## 9. Test IP connectivity

Open **PC0 > Desktop > Command Prompt**, then run:

```text
ping 192.168.1.1
```

> [!tip]
> The first ping can time out while ARP learns the router's MAC address. Repeat the ping before troubleshooting further.

Do not test SNMP until the ping succeeds.

## 10. Query the router with MIB Browser

1. Open **PC0 > Desktop > MIB Browser**.
2. Enter target address `192.168.1.1`.
3. Confirm destination port `161`, if shown.
4. Select **SNMP v2c**, if the version option is available.
5. Enter read community `PT-RO`.
6. Select or enter an OID.
7. Choose **Get**.

Start with the hostname OID:

```text
1.3.6.1.2.1.1.5.0
```

Expected value:

```text
Router0
```

### Useful test OIDs

| Object | OID | Expected information |
|---|---|---|
| `sysDescr.0` | `1.3.6.1.2.1.1.1.0` | Device and IOS description |
| `sysUpTime.0` | `1.3.6.1.2.1.1.3.0` | Agent uptime |
| `sysContact.0` | `1.3.6.1.2.1.1.4.0` | `Network-Administrator` |
| `sysName.0` | `1.3.6.1.2.1.1.5.0` | `Router0` |
| `sysLocation.0` | `1.3.6.1.2.1.1.6.0` | `Network-Lab` |

Use **Get** for a scalar OID ending in `.0`. Use **Get Next** to move through nearby objects in the MIB tree.

## 11. Verify on Router0

```cisco
show running-config | include snmp
show snmp
show snmp community
```

> [!note]
> If the simulated IOS rejects one of the `show snmp` commands, check the SNMP lines in `show running-config` and verify operation from the MIB Browser.

## 12. Troubleshooting

### MIB request times out

- [ ] Confirm `ping 192.168.1.1` succeeds from PC0.
- [ ] Confirm the router interface is `up/up`.
- [ ] Use the router address `192.168.1.1` as the MIB Browser target.
- [ ] Match SNMPv2c and community `PT-RO` exactly.
- [ ] Confirm UDP destination port `161`, if the field is available.
- [ ] Check `show running-config | include snmp`.

### Router interface is down

Return to the interface and enable it:

```cisco
configure terminal
interface gigabitEthernet 0/0
 no shutdown
end
```

Also confirm the cable and the actual interface name.

### SNMP command is unavailable

The selected router's simulated IOS may not implement that command. Try a different Cisco router model and use contextual help:

```cisco
snmp-server ?
show snmp ?
```

## 13. Complete Router0 configuration

```cisco
enable
configure terminal
hostname Router0

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit

snmp-server community PT-RO ro
snmp-server location Network-Lab
snmp-server contact Network-Administrator
snmp-server host 192.168.1.10 version 2c PT-RO
snmp-server enable traps

end
copy running-config startup-config
```

## 14. Completion checklist

- [ ] Router interface is `up/up`.
- [ ] PC0 can ping `192.168.1.1`.
- [ ] Router contains the `PT-RO` read-only community.
- [ ] MIB Browser returns `Router0` for `sysName.0`.
- [ ] Running configuration is saved.

## 15. Key takeaways

- The router is the **SNMP agent**; PC0 is the **SNMP manager**.
- SNMP queries normally use UDP port `161`.
- Traps and informs normally use UDP port `162`.
- SNMPv2c uses an unencrypted community string.
- SNMPv3 is preferable on real networks when supported.

---

**Parent:** [[SNMP - Overview|SNMP Overview]]  
**Home:** [[Network Notes Home]]
