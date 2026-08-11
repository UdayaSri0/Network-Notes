---
title: "35 - Syslog Central Logging - Step by Step"
aliases:
  - "Syslog configuration"
  - "Syslog configuration guide"
category: "Step-by-Step Configuration/Monitoring and Management"
difficulty: "Beginner"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[33 - SNMPv2c - Simple Network Management Protocol Version 2c - Step by Step]]"
  - "[[34 - SNMPv3 - Simple Network Management Protocol Version 3 - Step by Step]]"
  - "[[36 - CDP and LLDP - Cisco and Link Layer Discovery Protocols - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 35 - Syslog Central Logging - Step by Step

> [!info] Outcome
> Send timestamped informational Cisco IOS messages to a central Syslog server and verify local and remote logging.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Yes**

## 2. Example Topology

```mermaid
flowchart LR
    R1["R1"] --- SW1["SW1"] --- SYSLOG["Syslog Server 192.168.50.10"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| R1 G0/0 | SW1 G0/1 | Copper straight-through |
| Syslog Server | SW1 F0/1 | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | G0/0 | 192.168.50.1 /24 | — |
| Syslog Server | FastEthernet0 | 192.168.50.10 /24 | 192.168.50.1 |

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
service timestamps log datetime msec
logging host 192.168.50.10
logging trap informational
logging source-interface gigabitEthernet0/0
logging buffered 16384 informational
end
copy running-config startup-config
```

### Step 5 — Configure the Syslog server

Set `192.168.50.10/24`, gateway `192.168.50.1`. Open **Services → SYSLOG** and switch it **On**.

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
service timestamps log datetime msec
logging host 192.168.50.10
logging trap informational
logging source-interface gigabitEthernet0/0
logging buffered 16384 informational
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

- `show logging`
- `show clock`
- `ping 192.168.50.10`
- `show running-config | include logging`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| Reachability | R1 | 192.168.50.10 | Success |
| Test message | R1 | Shutdown/no shutdown a spare interface | Messages appear on server |
| Timestamp | Syslog Server | Received entry | Date/time included |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| No remote logs | Service off, wrong address, routing issue, or severity too restrictive | Enable server, ping it, and inspect show logging |
| Wrong source IP | No source interface set | Use a stable reachable management interface |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[33 - SNMPv2c - Simple Network Management Protocol Version 2c - Step by Step]]
- [[34 - SNMPv3 - Simple Network Management Protocol Version 3 - Step by Step]]
- [[36 - CDP and LLDP - Cisco and Link Layer Discovery Protocols - Step by Step]]

Return to [[Configuration Library Dashboard]].
