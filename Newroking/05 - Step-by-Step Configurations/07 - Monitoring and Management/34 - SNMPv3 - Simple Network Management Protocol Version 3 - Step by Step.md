---
title: "34 - SNMPv3 - Simple Network Management Protocol Version 3 - Step by Step"
aliases:
  - "SNMPv3 configuration"
  - "SNMPv3 configuration guide"
category: "Step-by-Step Configuration/Monitoring and Management"
difficulty: "Advanced"
packet_tracer_supported: "Partial"
related_protocols:
  - "[[33 - SNMPv2c - Simple Network Management Protocol Version 2c - Step by Step]]"
  - "[[35 - Syslog Central Logging - Step by Step]]"
  - "[[36 - CDP and LLDP - Cisco and Link Layer Discovery Protocols - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 34 - SNMPv3 - Simple Network Management Protocol Version 3 - Step by Step

> [!info] Outcome
> Configure authenticated and encrypted Simple Network Management Protocol Version 3 (SNMPv3) access with a restricted management source.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Partial**

## 2. Example Topology

```mermaid
flowchart LR
    NMS["Secure NMS 192.168.50.10"] --- SW1["SW1"] --- R1["R1 SNMPv3 Agent"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| NMS | SW1 F0/1 | Copper straight-through |
| SW1 G0/1 | R1 G0/0 | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 | 192.168.50.1 /24 | — |
| NMS | FastEthernet0 | 192.168.50.10 /24 | 192.168.50.1 |

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
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
access-list 10 permit host 192.168.50.10
snmp-server view CAMPUS-VIEW iso included
snmp-server group CAMPUS-GROUP v3 priv read CAMPUS-VIEW access 10
snmp-server user snmpadmin CAMPUS-GROUP v3 auth sha AuthPass123 priv aes 128 PrivPass123
snmp-server location Main-Campus-Room-201
snmp-server contact network-admin@campus.lab
end
copy running-config startup-config
```

### Step 5 — Configure the NMS

If your simulator supports SNMPv3, add user `snmpadmin`, SHA authentication password `AuthPass123`, AES-128 privacy password `PrivPass123`, and target `192.168.50.1`.

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### R1

```cisco
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
access-list 10 permit host 192.168.50.10
snmp-server view CAMPUS-VIEW iso included
snmp-server group CAMPUS-GROUP v3 priv read CAMPUS-VIEW access 10
snmp-server user snmpadmin CAMPUS-GROUP v3 auth sha AuthPass123 priv aes 128 PrivPass123
snmp-server location Main-Campus-Room-201
snmp-server contact network-admin@campus.lab
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> Packet Tracer may not provide a complete SNMPv3 manager or all IOS commands. Verify this configuration in CML, GNS3, EVE-NG, Linux net-snmp, or on real Cisco IOS.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show snmp user`
- `show snmp group`
- `show snmp view`
- `show access-lists 10`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| User | R1 | show snmp user | snmpadmin uses authentication and privacy |
| Secure poll | NMS | R1 | Authenticated encrypted response |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| User not visible in running config | IOS hides SNMPv3 secrets | Use show snmp user rather than expecting plaintext |
| Authentication failure | User/group/password/algorithm mismatch | Match SHA, AES-128, and both passphrases exactly |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[33 - SNMPv2c - Simple Network Management Protocol Version 2c - Step by Step]]
- [[35 - Syslog Central Logging - Step by Step]]
- [[36 - CDP and LLDP - Cisco and Link Layer Discovery Protocols - Step by Step]]

Return to [[Configuration Library Dashboard]].
