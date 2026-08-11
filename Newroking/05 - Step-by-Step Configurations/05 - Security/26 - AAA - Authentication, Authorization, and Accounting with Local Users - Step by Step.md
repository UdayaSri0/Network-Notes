---
title: "26 - AAA - Authentication, Authorization, and Accounting with Local Users - Step by Step"
aliases:
  - "Local AAA configuration"
  - "Local AAA configuration guide"
category: "Step-by-Step Configuration/Security"
difficulty: "Intermediate"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[25 - SSH - Secure Shell Remote Management - Step by Step]]"
  - "[[27 - RADIUS and TACACS+ Central AAA - Step by Step]]"
  - "[[28 - Standard IPv4 ACL - Access Control List - Step by Step]]"
  - "[[29 - Extended and Named IPv4 ACL - Access Control List - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 26 - AAA - Authentication, Authorization, and Accounting with Local Users - Step by Step

> [!info] Outcome
> Enable Authentication, Authorization, and Accounting (AAA), apply a local login method list to SSH, and preserve console recovery access.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    ADMIN["Admin PC"] --- SW1["SW1"] --- R1["R1 Local AAA"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| Admin PC | SW1 F0/1 | Copper straight-through |
| SW1 G0/1 | R1 G0/0 | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 | 192.168.99.1 /24 | — |
| Admin PC | FastEthernet0 | 192.168.99.10 /24 | 192.168.99.1 |

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
ip domain-name campus.lab
username netadmin privilege 15 secret LocalAAA!23
aaa new-model
aaa authentication login VTY-LOCAL local
aaa authorization exec VTY-AUTHZ local
interface gigabitEthernet0/0
 ip address 192.168.99.1 255.255.255.0
 no shutdown
exit
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
 login authentication VTY-LOCAL
 authorization exec VTY-AUTHZ
 transport input ssh
exit
line console 0
 login local
end
copy running-config startup-config
```

### Step 5 — Test from the Admin PC

Configure `192.168.99.10/24`, then use `ssh -l netadmin 192.168.99.1`.

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### R1

```cisco
enable
configure terminal
hostname R1
ip domain-name campus.lab
username netadmin privilege 15 secret LocalAAA!23
aaa new-model
aaa authentication login VTY-LOCAL local
aaa authorization exec VTY-AUTHZ local
interface gigabitEthernet0/0
 ip address 192.168.99.1 255.255.255.0
 no shutdown
exit
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
 login authentication VTY-LOCAL
 authorization exec VTY-AUTHZ
 transport input ssh
exit
line console 0
 login local
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> Configure and test the local user before enabling AAA so you do not lock yourself out.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show running-config | section aaa`
- `show running-config | section line vty`
- `show users`
- `debug aaa authentication`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| AAA login | Admin PC | SSH as netadmin | Login succeeds and privileged EXEC is available |
| Invalid login | Admin PC | Wrong password | Access denied |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| All logins fail | Method list references no valid database | Use console recovery and verify local user before applying the VTY list |
| User lands without expected rights | Authorization or privilege not configured | Check username privilege 15 and exec authorization |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[25 - SSH - Secure Shell Remote Management - Step by Step]]
- [[27 - RADIUS and TACACS+ Central AAA - Step by Step]]
- [[28 - Standard IPv4 ACL - Access Control List - Step by Step]]
- [[29 - Extended and Named IPv4 ACL - Access Control List - Step by Step]]

Return to [[Configuration Library Dashboard]].
