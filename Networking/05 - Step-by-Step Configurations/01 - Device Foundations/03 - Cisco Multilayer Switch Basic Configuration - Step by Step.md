---
title: "03 - Cisco Multilayer Switch Basic Configuration - Step by Step"
aliases:
  - "Multilayer switch configuration"
  - "Multilayer switch configuration guide"
category: "Step-by-Step Configuration/Device Foundations"
difficulty: "Intermediate"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[01 - Cisco Router Basic Configuration - Step by Step]]"
  - "[[02 - Cisco Switch Basic Configuration - Step by Step]]"
  - "[[04 - TFTP - Trivial File Transfer Protocol Backup and Restore - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 03 - Cisco Multilayer Switch Basic Configuration - Step by Step

> [!info] Outcome
> Enable Layer 3 routing on a multilayer switch and configure both switched virtual interfaces and a routed uplink.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    PC10["PC VLAN 10"] --- MLS1["MLS1"] --- R1["R1"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| PC10 | MLS1 F0/1 | Copper straight-through |
| MLS1 G0/1 | R1 G0/0 | Copper straight-through routed link |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| MLS1 | VLAN 10 | 192.168.10.1 /24 | — |
| MLS1 | G0/1 | 10.0.0.1 /30 | — |
| R1 | G0/0 | 10.0.0.2 /30 | — |
| PC10 | FastEthernet0 | 192.168.10.10 /24 | 192.168.10.1 |

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

### Step 4 — Configure MLS1

Open **MLS1 → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname MLS1
ip routing
vlan 10
 name USERS
exit
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
exit
interface gigabitEthernet0/1
 no switchport
 description ROUTED_LINK_TO_R1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 10.0.0.2
end
copy running-config startup-config
```
### Step 5 — Configure R1

Open **R1 → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.0.1
end
copy running-config startup-config
```

### Step 6 — Configure PC10

Set `192.168.10.10/24` and gateway `192.168.10.1`.

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### MLS1

```cisco
enable
configure terminal
hostname MLS1
ip routing
vlan 10
 name USERS
exit
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
exit
interface gigabitEthernet0/1
 no switchport
 description ROUTED_LINK_TO_R1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 10.0.0.2
end
copy running-config startup-config
```
### R1

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.0.1
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.



## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show ip interface brief`
- `show interfaces switchport`
- `show ip route`
- `show vlan brief`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| VLAN gateway | PC10 | 192.168.10.1 | Success |
| Routed uplink | MLS1 | 10.0.0.2 | Success |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| IP address rejected on G0/1 | Port is still Layer 2 | Enter no switchport before the IP address |
| SVI networks do not route | ip routing is missing | Enable ip routing globally |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[01 - Cisco Router Basic Configuration - Step by Step]]
- [[02 - Cisco Switch Basic Configuration - Step by Step]]
- [[04 - TFTP - Trivial File Transfer Protocol Backup and Restore - Step by Step]]

Return to [[Configuration Library Dashboard]].
