---
title: "39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step"
aliases:
  - "IPsec site-to-site VPN configuration"
  - "IPsec site-to-site VPN configuration guide"
category: "Step-by-Step Configuration/WAN, VPN, and Wireless"
difficulty: "Advanced"
packet_tracer_supported: "Partial"
related_protocols:
  - "[[37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step]]"
  - "[[38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step]]"
  - "[[40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step

> [!info] Outcome
> Protect traffic between two private LANs with an Internet Protocol Security (IPsec) site-to-site virtual private network using an Internet Key Exchange policy, transform set, crypto ACL, and crypto map.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Partial**

## 2. Example Topology

```mermaid
flowchart LR
    LAN1["192.168.10.0/24"] --- R1["R1 VPN Peer"] ---|"203.0.113.0/30"| R2["R2 VPN Peer"] --- LAN2["192.168.20.0/24"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| LAN PCs | Router G0/0 through switches | Copper straight-through |
| R1 G0/1 | R2 G0/1 | Copper crossover or Automatic WAN |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 | 192.168.10.1 /24 | — |
| R1 | G0/1 | 203.0.113.1 /30 | — |
| R2 | G0/1 | 203.0.113.2 /30 | — |
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
exit
ip route 192.168.20.0 255.255.255.0 203.0.113.2
access-list 110 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
crypto isakmp policy 10
 encr aes
 hash sha
 authentication pre-share
 group 2
exit
crypto isakmp key VPNkey123 address 203.0.113.2
crypto ipsec transform-set CAMPUS-SET esp-aes esp-sha-hmac
crypto map CAMPUS-MAP 10 ipsec-isakmp
 set peer 203.0.113.2
 set transform-set CAMPUS-SET
 match address 110
exit
interface gigabitEthernet0/1
 crypto map CAMPUS-MAP
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
exit
ip route 192.168.10.0 255.255.255.0 203.0.113.1
access-list 110 permit ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
crypto isakmp policy 10
 encr aes
 hash sha
 authentication pre-share
 group 2
exit
crypto isakmp key VPNkey123 address 203.0.113.1
crypto ipsec transform-set CAMPUS-SET esp-aes esp-sha-hmac
crypto map CAMPUS-MAP 10 ipsec-isakmp
 set peer 203.0.113.1
 set transform-set CAMPUS-SET
 match address 110
exit
interface gigabitEthernet0/1
 crypto map CAMPUS-MAP
end
copy running-config startup-config
```

### Step 6 — Configure both PCs

Assign the private LAN addresses and local router gateways, then generate PC-to-PC traffic to bring up the tunnel.

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
exit
ip route 192.168.20.0 255.255.255.0 203.0.113.2
access-list 110 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
crypto isakmp policy 10
 encr aes
 hash sha
 authentication pre-share
 group 2
exit
crypto isakmp key VPNkey123 address 203.0.113.2
crypto ipsec transform-set CAMPUS-SET esp-aes esp-sha-hmac
crypto map CAMPUS-MAP 10 ipsec-isakmp
 set peer 203.0.113.2
 set transform-set CAMPUS-SET
 match address 110
exit
interface gigabitEthernet0/1
 crypto map CAMPUS-MAP
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
exit
ip route 192.168.10.0 255.255.255.0 203.0.113.1
access-list 110 permit ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
crypto isakmp policy 10
 encr aes
 hash sha
 authentication pre-share
 group 2
exit
crypto isakmp key VPNkey123 address 203.0.113.1
crypto ipsec transform-set CAMPUS-SET esp-aes esp-sha-hmac
crypto map CAMPUS-MAP 10 ipsec-isakmp
 set peer 203.0.113.1
 set transform-set CAMPUS-SET
 match address 110
exit
interface gigabitEthernet0/1
 crypto map CAMPUS-MAP
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> The algorithms are chosen for broad simulator compatibility, not as a modern production security recommendation. Use current platform-supported IKEv2 and strong cryptography in production.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show crypto isakmp sa`
- `show crypto ipsec sa`
- `show crypto map`
- `show access-lists 110`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Underlay | R1 | 203.0.113.2 | Success |
| Interesting traffic | PC1 | 192.168.20.10 | Success and tunnel forms |
| Encrypted counters | R1/R2 | show crypto ipsec sa | Encaps/decaps counters increase |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| No ISAKMP security association | Peer, key, policy, or reachability mismatch | Compare both policies and ping public peer |
| ISAKMP up but no IPsec packets | Crypto ACLs are not mirrored or traffic does not match | Verify source/destination networks in ACL 110 |
| Commands unavailable | Packet Tracer image limitation | Move the lab to Cisco Modeling Labs, GNS3, EVE-NG, or real IOS |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step]]
- [[38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step]]
- [[40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step]]

Return to [[Configuration Library Dashboard]].
