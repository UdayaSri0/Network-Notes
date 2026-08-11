---
title: "11 - EtherChannel with LACP and PAgP - Step by Step"
aliases:
  - "EtherChannel LACP PAgP configuration"
  - "EtherChannel LACP PAgP configuration guide"
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

# 11 - EtherChannel with LACP and PAgP - Step by Step

> [!info] Outcome
> Bundle two physical links into one logical trunk using Link Aggregation Control Protocol (LACP), and show the equivalent Port Aggregation Protocol (PAgP) modes.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    SW1["SW1"] ==>|"G0/1 + G0/2, Port-channel 1"| SW2["SW2"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| SW1 G0/1 | SW2 G0/1 | Copper crossover or Automatic |
| SW1 G0/2 | SW2 G0/2 | Copper crossover or Automatic |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| SW1 | Port-channel1 | Layer 2 trunk | — |
| SW2 | Port-channel1 | Layer 2 trunk | — |

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

### Step 4 — Configure SW1 — LACP Active

Open **SW1 — LACP Active → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname SW1
vlan 10
vlan 20
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 channel-group 1 mode active
 no shutdown
exit
interface port-channel1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
end
copy running-config startup-config
```
### Step 5 — Configure SW2 — LACP Passive

Open **SW2 — LACP Passive → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname SW2
vlan 10
vlan 20
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 channel-group 1 mode passive
 no shutdown
exit
interface port-channel1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
end
copy running-config startup-config
```
### Step 6 — Configure PAgP Alternative — Use on Both Switches Instead of LACP

Open **PAgP Alternative — Use on Both Switches Instead of LACP → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
default interface range gigabitEthernet0/1-2
interface range gigabitEthernet0/1-2
 switchport mode trunk
 channel-group 1 mode desirable
 no shutdown
exit
interface port-channel1
 switchport mode trunk
end
copy running-config startup-config
```



## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### SW1 — LACP Active

```cisco
enable
configure terminal
hostname SW1
vlan 10
vlan 20
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 channel-group 1 mode active
 no shutdown
exit
interface port-channel1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
end
copy running-config startup-config
```
### SW2 — LACP Passive

```cisco
enable
configure terminal
hostname SW2
vlan 10
vlan 20
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 channel-group 1 mode passive
 no shutdown
exit
interface port-channel1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
end
copy running-config startup-config
```
### PAgP Alternative — Use on Both Switches Instead of LACP

```cisco
enable
configure terminal
default interface range gigabitEthernet0/1-2
interface range gigabitEthernet0/1-2
 switchport mode trunk
 channel-group 1 mode desirable
 no shutdown
exit
interface port-channel1
 switchport mode trunk
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> Do not configure LACP and PAgP simultaneously. The PAgP block is a separate alternative exercise.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show etherchannel summary`
- `show etherchannel port-channel`
- `show interfaces port-channel1`
- `show interfaces trunk`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Bundle state | SW1 and SW2 | show etherchannel summary | Po1(SU), member ports marked P |
| Resilience | Either switch | Disconnect one member link | Port-channel stays up |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| Ports show suspended | Speed, duplex, VLAN, trunk, or protocol mismatch | Make every member configuration identical on both ends |
| LACP does not form | Both ends passive | Use active on at least one endpoint |

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
