---
title: "40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step"
aliases:
  - "WPA2 wireless configuration"
  - "WPA2 wireless configuration guide"
category: "Step-by-Step Configuration/WAN, VPN, and Wireless"
difficulty: "Beginner"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step]]"
  - "[[38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step]]"
  - "[[39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step

> [!info] Outcome
> Create a secured wireless local area network with a service set identifier (SSID), Wi-Fi Protected Access 2 (WPA2) pre-shared key, DHCP, and client association.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    LAPTOP["Wireless Laptop"] -. "SSID CAMPUS-WIFI" .-> AP["Access Point"] --- SW1["SW1"] --- R1["R1 Gateway"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| Access Point Ethernet | SW1 F0/1 | Copper straight-through |
| SW1 G0/1 | R1 G0/0 | Copper straight-through |
| Laptop | Access Point | 802.11 wireless association |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 | 192.168.40.1 /24 | — |
| Access Point | Management | 192.168.40.2 /24 | 192.168.40.1 |
| Laptop | Wireless0 | DHCP 192.168.40.100+ | 192.168.40.1 |

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
 ip address 192.168.40.1 255.255.255.0
 no shutdown
exit
ip dhcp excluded-address 192.168.40.1 192.168.40.99
ip dhcp pool WIRELESS-USERS
 network 192.168.40.0 255.255.255.0
 default-router 192.168.40.1
 dns-server 192.168.40.1
end
copy running-config startup-config
```

### Step 5 — Configure the access point

Set management IP `192.168.40.2/24` and gateway `192.168.40.1`. Set SSID `CAMPUS-WIFI`, security **WPA2-PSK**, encryption **AES**, and key `CampusWiFi!23`. Choose a non-overlapping channel appropriate to the classroom.
### Step 6 — Configure the laptop

Install/enable its wireless interface if required. Open **Desktop → PC Wireless**, select `CAMPUS-WIFI`, choose WPA2-PSK, enter `CampusWiFi!23`, then request DHCP.

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### R1

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.40.1 255.255.255.0
 no shutdown
exit
ip dhcp excluded-address 192.168.40.1 192.168.40.99
ip dhcp pool WIRELESS-USERS
 network 192.168.40.0 255.255.255.0
 default-router 192.168.40.1
 dns-server 192.168.40.1
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> WPA3 and enterprise 802.1X support are limited in Packet Tracer. Use a wireless controller lab, real access point, or suitable emulator for production-grade demonstrations.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show ip dhcp binding`
- `show ip dhcp pool`
- `Laptop: ipconfig /all`
- `Laptop: ping 192.168.40.1`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Association | Laptop | CAMPUS-WIFI | Connected with WPA2 |
| DHCP | Laptop | WIRELESS-USERS pool | Receives 192.168.40.100 or later |
| Gateway | Laptop | 192.168.40.1 | Success |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| SSID not visible | Radio off or SSID differs | Enable AP radio and match the exact SSID |
| Authentication fails | Security mode or key mismatch | Use WPA2-PSK/AES and the exact same key |
| Associated but no address | DHCP or wired uplink issue | Check AP-to-switch link and router DHCP pool |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step]]
- [[38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step]]
- [[39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step]]

Return to [[Configuration Library Dashboard]].
