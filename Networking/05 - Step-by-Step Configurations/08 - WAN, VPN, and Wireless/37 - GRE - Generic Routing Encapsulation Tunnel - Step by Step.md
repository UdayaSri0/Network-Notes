---
title: "37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step"
aliases:
  - "GRE tunnel configuration"
  - "GRE tunnel configuration guide"
category: "Step-by-Step Configuration/WAN, VPN, and Wireless"
difficulty: "Advanced"
packet_tracer_supported: "Partial"
related_protocols:
  - "[[38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step]]"
  - "[[39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step]]"
  - "[[40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step

> [!info] Outcome
> Build a Generic Routing Encapsulation (GRE) tunnel between two routers, route private LAN traffic through it, and verify tunnel reachability.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Partial**

## 2. Example Topology

```mermaid
flowchart LR
    LAN1["192.168.10.0/24"] --- R1["R1 Tunnel0"] ---|"203.0.113.0/30 underlay"| R2["R2 Tunnel0"] --- LAN2["192.168.20.0/24"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| LAN1 PC | R1 G0/0 through switch | Copper straight-through |
| R1 G0/1 | R2 G0/1 | Copper crossover or Automatic underlay |
| R2 G0/0 | LAN2 PC through switch | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 | 192.168.10.1 /24 | — |
| R1 | G0/1 | 203.0.113.1 /30 | — |
| R1 | Tunnel0 | 10.10.10.1 /30 | — |
| R2 | G0/1 | 203.0.113.2 /30 | — |
| R2 | Tunnel0 | 10.10.10.2 /30 | — |
| R2 | G0/0 | 192.168.20.1 /24 | — |
| PC1 | FastEthernet0 | 192.168.10.10 /24 | 192.168.10.1 |
| PC2 | FastEthernet0 | 192.168.20.10 /24 | 192.168.20.1 |

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

### Step 4 — Configure R1

Open **R1 → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 no shutdown
interface tunnel0
 ip address 10.10.10.1 255.255.255.252
 tunnel source gigabitEthernet0/1
 tunnel destination 203.0.113.2
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.10.10.2
end
copy running-config startup-config
```
### Step 5 — Configure R2

Open **R2 → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.252
 no shutdown
interface tunnel0
 ip address 10.10.10.2 255.255.255.252
 tunnel source gigabitEthernet0/1
 tunnel destination 203.0.113.1
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.10.10.1
end
copy running-config startup-config
```

### Step 6 — Configure end PCs

Set PC1 and PC2 from the table and use each local router LAN address as the gateway.

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### R1

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 no shutdown
interface tunnel0
 ip address 10.10.10.1 255.255.255.252
 tunnel source gigabitEthernet0/1
 tunnel destination 203.0.113.2
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.10.10.2
end
copy running-config startup-config
```
### R2

```cisco
enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.252
 no shutdown
interface tunnel0
 ip address 10.10.10.2 255.255.255.252
 tunnel source gigabitEthernet0/1
 tunnel destination 203.0.113.1
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.10.10.1
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> GRE provides encapsulation but not encryption. Protect sensitive GRE traffic with IPsec on a capable platform.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show interfaces tunnel0`
- `show ip interface brief`
- `show ip route`
- `ping 10.10.10.2 source 10.10.10.1`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Underlay | R1 | 203.0.113.2 | Success |
| Tunnel | R1 | 10.10.10.2 | Success |
| Private LAN | PC1 | 192.168.20.10 | Success through Tunnel0 |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| Tunnel up/down | Destination route or far endpoint unavailable | Verify underlay connectivity and tunnel destination |
| Tunnel ping works but LAN fails | Static LAN route or PC gateway missing | Check routes and both host gateways |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step]]
- [[39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step]]
- [[40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step]]

Return to [[Configuration Library Dashboard]].
