---
title: "29 - Extended and Named IPv4 ACL - Access Control List - Step by Step"
aliases:
  - "Extended named ACL configuration"
  - "Extended named ACL configuration guide"
category: "Step-by-Step Configuration/Security"
difficulty: "Intermediate"
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

# 29 - Extended and Named IPv4 ACL - Access Control List - Step by Step

> [!info] Outcome
> Permit web and Domain Name System (DNS) traffic from a user subnet to a server while denying other traffic, using a named extended IPv4 ACL near the source.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    USER["User PC 192.168.10.10"] --- R1["R1 ACL inbound"] --- SERVER["Server 192.168.50.10"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| User PC | R1 G0/0 through switch | Copper straight-through |
| R1 G0/1 | Server through switch | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 | 192.168.10.1 /24 | — |
| R1 | G0/1 | 192.168.50.1 /24 | — |
| User PC | FastEthernet0 | 192.168.10.10 /24 | 192.168.10.1 |
| Server | FastEthernet0 | 192.168.50.10 /24 | 192.168.50.1 |

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
 ip access-group USER-TO-SERVER in
 no shutdown
interface gigabitEthernet0/1
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
ip access-list extended USER-TO-SERVER
 remark Permit DNS, HTTP, and HTTPS to the server
 permit udp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 53
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 80
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 443
 deny ip 192.168.10.0 0.0.0.255 host 192.168.50.10
 permit ip any any
end
copy running-config startup-config
```

### Step 5 — Configure and enable server services

Set `192.168.50.10/24`, gateway `192.168.50.1`; enable DNS, HTTP, and HTTPS where available.
### Step 6 — Configure User PC

Set `192.168.10.10/24`, gateway `192.168.10.1`, and DNS `192.168.50.10`.

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### R1

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip access-group USER-TO-SERVER in
 no shutdown
interface gigabitEthernet0/1
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
ip access-list extended USER-TO-SERVER
 remark Permit DNS, HTTP, and HTTPS to the server
 permit udp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 53
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 80
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 443
 deny ip 192.168.10.0 0.0.0.255 host 192.168.50.10
 permit ip any any
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

- `show access-lists USER-TO-SERVER`
- `show ip interface gigabitEthernet0/0`
- `show running-config | section ip access-list`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| HTTP | User PC | http://192.168.50.10 | Allowed |
| HTTPS | User PC | https://192.168.50.10 | Allowed if service supported |
| ICMP | User PC | 192.168.50.10 | Denied |
| Other destinations | User PC | Unrelated routed host | Allowed by final permit |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| DNS still fails | Only UDP or wrong server address permitted | Confirm DNS server IP and add TCP 53 if the lesson requires it |
| All later traffic denied | Final permit ip any any missing | Account for the implicit deny at the end |

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
