---
title: "09 - STP - Spanning Tree Protocol Root Bridge Configuration - Step by Step"
aliases:
  - "STP root bridge configuration"
  - "STP root bridge configuration guide"
category: "Step-by-Step Configuration/Switching and Inter-VLAN Routing"
difficulty: "Intermediate"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[05 - VLAN - Virtual Local Area Network Configuration - Step by Step]]"
  - "[[06 - IEEE 802.1Q Trunk Configuration - Step by Step]]"
  - "[[07 - Router-on-a-Stick Inter-VLAN Routing - Step by Step]]"
  - "[[08 - Multilayer Switch Inter-VLAN Routing - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 09 - STP - Spanning Tree Protocol Root Bridge Configuration - Step by Step

> [!info] Outcome
> Build a redundant triangle and deliberately select the primary and secondary Spanning Tree Protocol (STP) root bridges for VLAN 10.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart TD
    SW1["SW1 Root Primary"] --- SW2["SW2 Root Secondary"]
    SW1 --- SW3["SW3 Access"]
    SW2 --- SW3
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| SW1 G0/1 | SW2 G0/1 | Copper crossover or Automatic trunk |
| SW1 G0/2 | SW3 G0/1 | Copper crossover or Automatic trunk |
| SW2 G0/2 | SW3 G0/2 | Copper crossover or Automatic trunk |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| SW1 | VLAN 10 | Layer 2 only | — |
| SW2 | VLAN 10 | Layer 2 only | — |
| SW3 | VLAN 10 | Layer 2 only | — |

## 4. Before You Configure

1. Place and rename every device exactly as shown.
2. Connect the interfaces in the cabling table.
3. Wait for links to become active before troubleshooting Layer 3.
4. Erase or inspect old lab configuration so it does not conflict with this example.

## 5. Step-by-Step Configuration

### Step 1 — Build the topology

Place the listed devices, rename them, and make each connection shown above.

### Step 2 — Confirm the addressing plan

Check that every address is unique, belongs to the stated subnet, and uses the correct mask or prefix length.

### Step 3 — Open each device

For IOS devices, select **CLI** and press Enter. For PCs and servers, use the named Packet Tracer desktop or services panel.

### Step 4 — Configure SW1

Open **SW1 → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname SW1
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
spanning-tree vlan 10 root primary
end
copy running-config startup-config
```
### Step 5 — Configure SW2

Open **SW2 → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname SW2
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
spanning-tree vlan 10 root secondary
end
copy running-config startup-config
```
### Step 6 — Configure SW3

Open **SW3 → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname SW3
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
end
copy running-config startup-config
```



## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### SW1

```cisco
enable
configure terminal
hostname SW1
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
spanning-tree vlan 10 root primary
end
copy running-config startup-config
```
### SW2

```cisco
enable
configure terminal
hostname SW2
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
spanning-tree vlan 10 root secondary
end
copy running-config startup-config
```
### SW3

```cisco
enable
configure terminal
hostname SW3
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> A blocked redundant port is normal STP operation, not a failure.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show spanning-tree vlan 10`
- `show spanning-tree root`
- `show interfaces trunk`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Root election | SW1 | show spanning-tree vlan 10 | This bridge is the root |
| Loop prevention | SW3 | show spanning-tree vlan 10 | One redundant path is alternate/blocking |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| Wrong root elected | Priority command missing or applied to wrong VLAN | Compare bridge IDs and configure root primary for VLAN 10 |
| No port blocks | Triangle is not physically complete or VLAN 10 is absent | Verify all three trunks and allowed VLANs |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[05 - VLAN - Virtual Local Area Network Configuration - Step by Step]]
- [[06 - IEEE 802.1Q Trunk Configuration - Step by Step]]
- [[07 - Router-on-a-Stick Inter-VLAN Routing - Step by Step]]
- [[08 - Multilayer Switch Inter-VLAN Routing - Step by Step]]

Return to [[Configuration Library Dashboard]].
