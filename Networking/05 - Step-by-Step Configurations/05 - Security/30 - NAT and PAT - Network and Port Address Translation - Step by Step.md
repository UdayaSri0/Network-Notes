---
title: "30 - NAT and PAT - Network and Port Address Translation - Step by Step"
aliases:
  - "Static dynamic NAT PAT configuration"
  - "Static dynamic NAT PAT configuration guide"
category: "Step-by-Step Configuration/Security"
difficulty: "Advanced"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[25 - SSH - Secure Shell Remote Management - Step by Step]]"
  - "[[26 - AAA - Authentication, Authorization, and Accounting with Local Users - Step by Step]]"
  - "[[27 - RADIUS and TACACS+ Central AAA - Step by Step]]"
  - "[[28 - Standard IPv4 ACL - Access Control List - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 30 - NAT and PAT - Network and Port Address Translation - Step by Step

> [!info] Outcome
> Configure inside/outside roles and demonstrate static Network Address Translation (NAT), dynamic pooled NAT, and Port Address Translation (PAT) as separate alternatives.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    PC1["Inside PC 192.168.10.10"] --- R1["R1 NAT"] --- ISP["ISP 203.0.113.1"] --- WEB["Public Server 198.51.100.10"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| PC1 | R1 G0/0 through switch | Copper straight-through |
| R1 G0/1 | ISP G0/0 | Copper crossover or Automatic |
| ISP G0/1 | Public Server through switch | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 inside | 192.168.10.1 /24 | — |
| R1 | G0/1 outside | 203.0.113.2 /29 | — |
| ISP | G0/0 | 203.0.113.1 /29 | — |
| ISP | G0/1 | 198.51.100.1 /24 | — |
| PC1 | FastEthernet0 | 192.168.10.10 /24 | 192.168.10.1 |
| Public Server | FastEthernet0 | 198.51.100.10 /24 | 198.51.100.1 |

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

### Step 4 — Configure ISP

Open **ISP → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname ISP
interface gigabitEthernet0/0
 ip address 203.0.113.1 255.255.255.248
 no shutdown
interface gigabitEthernet0/1
 ip address 198.51.100.1 255.255.255.0
 no shutdown
end
copy running-config startup-config
```
### Step 5 — Configure R1 — PAT Recommended Exercise

Open **R1 — PAT Recommended Exercise → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip nat inside
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.248
 ip nat outside
 no shutdown
exit
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface gigabitEthernet0/1 overload
ip route 0.0.0.0 0.0.0.0 203.0.113.1
end
copy running-config startup-config
```
### Step 6 — Configure R1 — Static NAT Alternative

Open **R1 — Static NAT Alternative → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
no ip nat inside source list 1 interface gigabitEthernet0/1 overload
ip nat inside source static 192.168.10.10 203.0.113.3
end
copy running-config startup-config
```
### Step 7 — Configure R1 — Dynamic NAT Alternative

Open **R1 — Dynamic NAT Alternative → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
no ip nat inside source static 192.168.10.10 203.0.113.3
ip nat pool PUBLIC-POOL 203.0.113.4 203.0.113.6 netmask 255.255.255.248
ip nat inside source list 1 pool PUBLIC-POOL
end
copy running-config startup-config
```

### Step 8 — Configure the inside PC and public server

Set the static IP addresses and gateways in the table; enable HTTP on the public server for a browser test.

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### ISP

```cisco
enable
configure terminal
hostname ISP
interface gigabitEthernet0/0
 ip address 203.0.113.1 255.255.255.248
 no shutdown
interface gigabitEthernet0/1
 ip address 198.51.100.1 255.255.255.0
 no shutdown
end
copy running-config startup-config
```
### R1 — PAT Recommended Exercise

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip nat inside
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.248
 ip nat outside
 no shutdown
exit
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface gigabitEthernet0/1 overload
ip route 0.0.0.0 0.0.0.0 203.0.113.1
end
copy running-config startup-config
```
### R1 — Static NAT Alternative

```cisco
enable
configure terminal
no ip nat inside source list 1 interface gigabitEthernet0/1 overload
ip nat inside source static 192.168.10.10 203.0.113.3
end
copy running-config startup-config
```
### R1 — Dynamic NAT Alternative

```cisco
enable
configure terminal
no ip nat inside source static 192.168.10.10 203.0.113.3
ip nat pool PUBLIC-POOL 203.0.113.4 203.0.113.6 netmask 255.255.255.248
ip nat inside source list 1 pool PUBLIC-POOL
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> The documentation ranges 203.0.113.0/24 and 198.51.100.0/24 are used intentionally. In production, use only public addresses assigned and routed by the service provider.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show ip nat translations`
- `show ip nat statistics`
- `show access-lists`
- `clear ip nat translation *`
- `show ip route`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Outside ping | PC1 | 198.51.100.10 | Success with PAT exercise |
| Translation | R1 | show ip nat translations | Inside local 192.168.10.10 is translated |
| Statistics | R1 | show ip nat statistics | G0/0 inside and G0/1 outside |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| No translations | NAT roles, ACL, or traffic missing | Generate traffic and verify inside/outside plus ACL match |
| Route works only from router | PC gateway missing | Set PC1 gateway to 192.168.10.1 |
| Alternative conflicts | More than one example enabled | Remove the prior translation rule before testing another method |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[25 - SSH - Secure Shell Remote Management - Step by Step]]
- [[26 - AAA - Authentication, Authorization, and Accounting with Local Users - Step by Step]]
- [[27 - RADIUS and TACACS+ Central AAA - Step by Step]]
- [[28 - Standard IPv4 ACL - Access Control List - Step by Step]]

Return to [[Configuration Library Dashboard]].
