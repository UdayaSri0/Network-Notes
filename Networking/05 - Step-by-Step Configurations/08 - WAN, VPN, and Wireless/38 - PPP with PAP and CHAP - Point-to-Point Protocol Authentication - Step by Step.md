---
title: "38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step"
aliases:
  - "PPP PAP CHAP configuration"
  - "PPP PAP CHAP configuration guide"
category: "Step-by-Step Configuration/WAN, VPN, and Wireless"
difficulty: "Advanced"
packet_tracer_supported: "Partial"
related_protocols:
  - "[[37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step]]"
  - "[[39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step]]"
  - "[[40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step]]"
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# 38 - PPP with PAP and CHAP - Point-to-Point Protocol Authentication - Step by Step

> [!info] Outcome
> Configure a serial Point-to-Point Protocol (PPP) link and test Password Authentication Protocol (PAP) and Challenge Handshake Authentication Protocol (CHAP) as separate authentication methods.

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**Partial**

## 2. Example Topology

```mermaid
flowchart LR
    LAN1["192.168.10.0/24"] --- R1["R1 DCE"] ==>|"Serial PPP"| R2["R2 DTE"] --- LAN2["192.168.20.0/24"]
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
| R1 S0/0/0 | R2 S0/0/0 | Serial DCE/DTE; add compatible serial modules first |
| LAN PCs | Router G0/0 through switches | Copper straight-through |

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
| R1 | S0/0/0 | 10.0.12.1 /30 | — |
| R2 | S0/0/0 | 10.0.12.2 /30 | — |
| R1 | G0/0 | 192.168.10.1 /24 | — |
| R2 | G0/0 | 192.168.20.1 /24 | — |

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

### Step 4 — Configure R1 — CHAP Recommended

Open **R1 — CHAP Recommended → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname R1
username R2 password ChapSecret123
interface serial0/0/0
 ip address 10.0.12.1 255.255.255.252
 encapsulation ppp
 ppp authentication chap
 clock rate 64000
 no shutdown
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.0.12.2
end
copy running-config startup-config
```
### Step 5 — Configure R2 — CHAP Recommended

Open **R2 — CHAP Recommended → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
hostname R2
username R1 password ChapSecret123
interface serial0/0/0
 ip address 10.0.12.2 255.255.255.252
 encapsulation ppp
 ppp authentication chap
 no shutdown
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.12.1
end
copy running-config startup-config
```
### Step 6 — Configure PAP Alternative — R1 Interface

Open **PAP Alternative — R1 Interface → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
username R2 password PapSecret123
interface serial0/0/0
 ppp authentication pap
 ppp pap sent-username R1 password PapSecret123
end
copy running-config startup-config
```
### Step 7 — Configure PAP Alternative — R2 Interface

Open **PAP Alternative — R2 Interface → CLI**, press Enter, and enter the following commands exactly.

```cisco
enable
configure terminal
username R1 password PapSecret123
interface serial0/0/0
 ppp authentication pap
 ppp pap sent-username R2 password PapSecret123
end
copy running-config startup-config
```



## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

### R1 — CHAP Recommended

```cisco
enable
configure terminal
hostname R1
username R2 password ChapSecret123
interface serial0/0/0
 ip address 10.0.12.1 255.255.255.252
 encapsulation ppp
 ppp authentication chap
 clock rate 64000
 no shutdown
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.0.12.2
end
copy running-config startup-config
```
### R2 — CHAP Recommended

```cisco
enable
configure terminal
hostname R2
username R1 password ChapSecret123
interface serial0/0/0
 ip address 10.0.12.2 255.255.255.252
 encapsulation ppp
 ppp authentication chap
 no shutdown
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.12.1
end
copy running-config startup-config
```
### PAP Alternative — R1 Interface

```cisco
enable
configure terminal
username R2 password PapSecret123
interface serial0/0/0
 ppp authentication pap
 ppp pap sent-username R1 password PapSecret123
end
copy running-config startup-config
```
### PAP Alternative — R2 Interface

```cisco
enable
configure terminal
username R1 password PapSecret123
interface serial0/0/0
 ppp authentication pap
 ppp pap sent-username R2 password PapSecret123
end
copy running-config startup-config
```

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

> [!note] Teaching note
> PAP sends reusable credentials and is weaker than CHAP. Configure only one authentication alternative at a time.

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

- `show interfaces serial0/0/0`
- `show controllers serial0/0/0`
- `show ip interface brief`
- `debug ppp authentication`

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
| PPP state | R1/R2 | show interfaces serial0/0/0 | Line and protocol are up; encapsulation PPP |
| Neighbor ping | R1 | 10.0.12.2 | Success |
| Authentication failure | One router | Temporarily change secret | Line protocol fails |

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
| Serial interface missing | No serial module installed | Power off router, install supported HWIC/WIC, then recable |
| Line protocol down | Encapsulation, username, hostname, or secret mismatch | Match PPP mode and CHAP peer-hostname credentials |
| Clock rate rejected | Command entered on DTE side | Apply clock rate only to the DCE endpoint |

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

- [[37 - GRE - Generic Routing Encapsulation Tunnel - Step by Step]]
- [[39 - IPsec - Internet Protocol Security Site-to-Site VPN - Step by Step]]
- [[40 - WPA2 - Wi-Fi Protected Access 2 Wireless LAN - Step by Step]]

Return to [[Configuration Library Dashboard]].
