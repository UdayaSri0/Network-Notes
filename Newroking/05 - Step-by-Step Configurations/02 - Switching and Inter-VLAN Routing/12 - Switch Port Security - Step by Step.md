---
title: "12 - Switch Port Security - Step by Step"
aliases:
  - "Port security configuration"
  - "Port security configuration guide"
category: "Step-by-Step Configuration/Switching and Inter-VLAN Routing"
difficulty: "Beginner"
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

# 12 - Switch Port Security - Step by Step

> [!info] Outcome
> Limit an access port to learned Media Access Control (MAC) addresses and compare protect, restrict, and shutdown violation behaviour.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    PC1["Approved PC"] --- SW1["SW1 F0/1 secured"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| PC1 FastEthernet0 | SW1 F0/1 | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| PC1 | FastEthernet0 | 192.168.10.10 /24 | — |
| SW1 | F0/1 | Access VLAN 10 | — |

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
interface fastEthernet0/1
 description SECURED_USER_PORT
 switchport mode access
 switchport access vlan 10
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 switchport port-security violation restrict
 spanning-tree portfast
end
copy running-config startup-config
```

### Step 5 — Generate traffic from PC1

Assign `192.168.10.10/24`, then send a ping so SW1 learns the sticky MAC address.

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
interface fastEthernet0/1
 description SECURED_USER_PORT
 switchport mode access
 switchport access vlan 10
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 switchport port-security violation restrict
 spanning-tree portfast
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

- `show port-security`
- `show port-security interface fastEthernet0/1`
- `show mac address-table interface fastEthernet0/1`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Sticky learning | SW1 | F0/1 secure addresses | One secure MAC appears after PC1 sends traffic |
| Violation | Replacement PC | Send traffic through F0/1 | Violation counter increases in restrict mode |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| Port-security command rejected | Port is dynamic or trunk mode | Set switchport mode access first |
| Port is secure-shutdown | Violation mode shutdown triggered | Remove cause, then shutdown/no shutdown; clear secure MAC if needed |

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
