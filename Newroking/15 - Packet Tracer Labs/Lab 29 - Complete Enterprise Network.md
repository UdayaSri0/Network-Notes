---
title: "Lab 29 - Complete Enterprise Network"
category: "Packet Tracer Labs"
difficulty: "Advanced"
packet_tracer_supported: "Partial"
related_protocols:
  - "[[Complete Enterprise Network Design]]"
  - "[[Testing Matrix Template]]"
tags:
  - networking
  - packet-tracer
  - lab
  - teaching
type: "lab"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# Lab 29 - Complete Enterprise Network

> [!abstract]
> Integrate hierarchical switching, routing, centralized services, security, monitoring, redundancy, and Internet simulation.

> [!info] Packet Tracer Support: Partial
> Confirm every required command on the selected Packet Tracer device model. Use GNS3, EVE-NG, Cisco CML, Wireshark, Linux, or real hardware when a listed feature is partial.

## 1. Learning Objectives

- Explain the purpose of the technology before configuring it.
- Build and address the topology from a documented plan.
- Apply device-specific configuration in the correct mode.
- Verify operation with commands and endpoint tests.
- Diagnose one controlled failure without erasing the configuration.

## 2. Required Devices

Multiple routers, multilayer and access switches, VLANs, servers, endpoints, ISP

## 3. Topology

```text
Endpoint(s) ---- Access/Distribution ---- Router or Service ---- Destination
       |                 |                       |
       +----------- verification points --------+
```

Draw the exact port-to-port topology before cabling. Record any interface name that differs from the related configuration note.

## 4. Addressing and Interface Plan

| Device | Interface | Address/VLAN | Connected to | Purpose |
|---|---|---|---|---|
| Complete before configuration | | | | |

> [!important]
> Validate every network address, mask, wildcard, VLAN, gateway, and next hop before entering IOS commands.

## 5. Implementation Tasks

1. Create VLANs 10 Administration, 20 Staff, 30 Students, 40 IT, 50 Servers, and 99 Management.
2. Build redundant trunks and EtherChannels with deterministic STP roots.
3. Configure HSRP gateways and inter-VLAN routing.
4. Run OSPF between routed infrastructure devices.
5. Use dedicated DHCP server 200.100.10.5 with relay; do not create router pools.
6. Add DNS, NTP, Syslog, SNMP, AAA, SSH, ACL, NAT/PAT, and port security.
7. Document every interface, address, cable, and test.

## 6. Configuration Rules

1. Configure one device at a time and label every code block with the device name.
2. Verify directly connected operation before adding routing, services, or security.
3. Use `no shutdown` on required routed interfaces.
4. Save only after the current stage passes its tests.
5. Use the linked subject notes for verified command syntax and explanations.

## 7. Baseline Verification

```cisco
show ip interface brief
show interfaces status
show vlan brief
show interfaces trunk
show ip route
```

Run only the commands relevant to each device type.

## 8. Testing Matrix

| Test | Requirement | Expected |
|---|---|---|
| Test 1 | Every VLAN receives correct DHCP | Success |
| Test 2 | DNS and web service work | Success |
| Test 3 | Routing survives one path failure | Success |
| Test 4 | HSRP and STP failover succeed | Success |
| Test 5 | Management and monitoring records are visible | Success |
| Test 6 | Internet simulation follows ACL and NAT policy | Success |

## 9. Controlled Failure

Select one cable, interface, route, VLAN, service, or policy directly related to the lab. Record the symptom, predict which verification output will change, introduce the fault, confirm the prediction, repair it, and repeat the testing matrix.

## 10. Troubleshooting Record

| Symptom | Possible cause | Command/evidence | Fix | Verification |
|---|---|---|---|---|
| | | | | |

## 11. Student Exercise

### Beginner

Complete the core implementation tasks with the addressing plan provided by the lecturer.

### Intermediate

Change the addressing or VLAN plan while preserving the same functional requirements.

### Advanced

Exchange a topology with another student, insert two documented faults, and troubleshoot without revealing the faults.

## 12. Lecturer Solution

Use the related configuration notes and templates to build a validated reference solution. Keep the final device configurations hidden until students submit their topology, verification evidence, and fault report.

## 13. Viva Questions

1. What user-visible problem does this lab solve?
2. Which command provides the strongest proof of correct protocol state?
3. Which wrong address, mask, VLAN, interface, or policy would cause the same symptom?
4. What Packet Tracer limitation would require another platform?

## 14. Related Notes

- [[Complete Enterprise Network Design]]
- [[Testing Matrix Template]]
- [[Networking Dashboard]]

## 15. Validated Enterprise Reference Design

> [!important]
> This design intentionally uses the required teaching address `200.100.10.5` for DHCP. It is a classroom value, not a recommendation to use unassigned public space in production.

### 15.1 Logical topology

```mermaid
flowchart TB
ISP[ISP Router] --- EDGE[EDGE1]
EDGE --- D1[DSW1]
EDGE --- D2[DSW2]
D1 == LACP Port-channel1 == D2
D1 --- A1[ASW1]
D2 --- A1
D1 --- A2[ASW2]
D2 --- A2
A1 --- USERS[Administration / Staff / Students / IT]
A2 --- SERVERS[DHCP / DNS / NTP / Syslog / SNMP / AAA / Web]
```

### 15.2 Device list

| Device | Suggested Packet Tracer type | Role |
|---|---|---|
| ISP | Cisco ISR router | Internet simulation and test loopback |
| EDGE1 | Cisco 2911 or equivalent | OSPF edge, default route, NAT/PAT |
| DSW1, DSW2 | Cisco 3560 multilayer switches | SVIs, HSRP, OSPF, STP roots |
| ASW1, ASW2 | Cisco 2960 switches | User and server access |
| Seven Server-PT devices | Packet Tracer servers | Central services |
| Client PCs | Packet Tracer PCs | DHCP and policy tests |

### 15.3 VLAN and IP plan

| VLAN | Name | Subnet | HSRP gateway | DSW1 | DSW2 |
|---:|---|---|---|---|---|
| 10 | Administration | `192.168.10.0/24` | `192.168.10.1` | `.2` | `.3` |
| 20 | Staff | `192.168.20.0/24` | `192.168.20.1` | `.2` | `.3` |
| 30 | Students | `192.168.30.0/24` | `192.168.30.1` | `.2` | `.3` |
| 40 | IT | `192.168.40.0/24` | `192.168.40.1` | `.2` | `.3` |
| 50 | Servers | `200.100.10.0/24` | `200.100.10.1` | `.2` | `.3` |
| 99 | Management | `192.168.99.0/24` | `192.168.99.1` | `.2` | `.3` |

Routed links:

| Link | First address | Second address |
|---|---|---|
| EDGE1 G0/0 to DSW1 G0/1 | `10.255.0.1/30` | `10.255.0.2/30` |
| EDGE1 G0/1 to DSW2 G0/1 | `10.255.0.5/30` | `10.255.0.6/30` |
| ISP G0/0 to EDGE1 G0/2 | `203.0.113.1/30` | `203.0.113.2/30` |
| ISP Loopback0 | `198.51.100.1/32` | Internet test destination |

### 15.4 Cable and interface plan

| Connection | Interfaces | Cable/port mode |
|---|---|---|
| ISP to EDGE1 | `G0/0` to `G0/2` | Copper, routed |
| EDGE1 to DSW1 | `G0/0` to `G0/1` | Copper, routed |
| EDGE1 to DSW2 | `G0/1` to `G0/1` | Copper, routed |
| DSW1 to DSW2 | `F0/23-24` on both | Two copper links, LACP trunk |
| DSWs to ASW1 | DSW `G0/2`, ASW `G0/1-2` | Redundant trunks |
| DSWs to ASW2 | DSW `F0/21-22`, ASW `G0/1-2` | Redundant trunks |
| End devices | Access switch FastEthernet ports | Copper straight-through, access mode |

Confirm actual interfaces before configuration and adjust consistently if the chosen model differs.

## 16. Server Configuration

All servers use mask `255.255.255.0` and gateway `200.100.10.1`.

| Server | Address | Packet Tracer service |
|---|---|---|
| DHCP | `200.100.10.5` | DHCP On |
| DNS | `200.100.10.10` | DNS On |
| NTP | `200.100.10.15` | NTP On |
| Syslog | `200.100.10.20` | SYSLOG On |
| SNMP manager | `200.100.10.25` | MIB Browser/manager PC if preferred |
| AAA | `200.100.10.30` | AAA On; add infrastructure clients |
| Web | `200.100.10.40` | HTTP/HTTPS On |

### Dedicated DHCP pools

Create these pools on Server0; do not configure router DHCP pools.

| Pool | Network/mask | Default gateway | DNS | Start IP | Maximum users |
|---|---|---|---|---|---:|
| ADMIN | `192.168.10.0/24` | `192.168.10.1` | `200.100.10.10` | `192.168.10.21` | 200 |
| STAFF | `192.168.20.0/24` | `192.168.20.1` | `200.100.10.10` | `192.168.20.21` | 200 |
| STUDENTS | `192.168.30.0/24` | `192.168.30.1` | `200.100.10.10` | `192.168.30.21` | 200 |
| IT | `192.168.40.0/24` | `192.168.40.1` | `200.100.10.10` | `192.168.40.21` | 200 |

Create DNS record `intranet.network.lab` pointing to `200.100.10.40`.

## 17. EDGE1 Full Configuration

```cisco
enable
configure terminal
hostname EDGE1
ip domain-name network.lab
username admin privilege 15 secret <STRONG-SECRET>
crypto key generate rsa modulus 2048
ip ssh version 2

interface gigabitEthernet 0/0
 description TO-DSW1
 ip address 10.255.0.1 255.255.255.252
 ip nat inside
 no shutdown
interface gigabitEthernet 0/1
 description TO-DSW2
 ip address 10.255.0.5 255.255.255.252
 ip nat inside
 no shutdown
interface gigabitEthernet 0/2
 description TO-ISP
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
 no shutdown

access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface gigabitEthernet 0/2 overload
ip route 0.0.0.0 0.0.0.0 203.0.113.1

router ospf 1
 router-id 3.3.3.3
 network 10.255.0.0 0.0.0.3 area 0
 network 10.255.0.4 0.0.0.3 area 0
 default-information originate

ntp server 200.100.10.15
service timestamps log datetime msec
logging 200.100.10.20
logging trap informational
snmp-server community TEACHING-RO ro
snmp-server location Enterprise-Lab
snmp-server contact Lecturer

line vty 0 4
 login local
 transport input ssh
end
copy running-config startup-config
```

## 18. ISP Full Configuration

```cisco
enable
configure terminal
hostname ISP
interface gigabitEthernet 0/0
 description TO-EDGE1
 ip address 203.0.113.1 255.255.255.252
 no shutdown
interface loopback 0
 ip address 198.51.100.1 255.255.255.255
ip route 200.100.10.0 255.255.255.0 203.0.113.2
end
copy running-config startup-config
```

## 19. DSW1 Full Configuration

```cisco
enable
configure terminal
hostname DSW1
ip routing
spanning-tree mode rapid-pvst
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 40
 name IT
vlan 50
 name SERVERS
vlan 99
 name MANAGEMENT

interface gigabitEthernet 0/1
 no switchport
 ip address 10.255.0.2 255.255.255.252
 no shutdown
interface gigabitEthernet 0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface fastEthernet 0/21
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface range fastEthernet 0/23 - 24
 channel-group 1 mode active
 no shutdown
interface port-channel 1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99

interface vlan 10
 ip address 192.168.10.2 255.255.255.0
 standby 10 ip 192.168.10.1
 standby 10 priority 110
 standby 10 preempt
 ip helper-address 200.100.10.5
interface vlan 20
 ip address 192.168.20.2 255.255.255.0
 standby 20 ip 192.168.20.1
 standby 20 priority 100
 standby 20 preempt
 ip helper-address 200.100.10.5
interface vlan 30
 ip address 192.168.30.2 255.255.255.0
 standby 30 ip 192.168.30.1
 standby 30 priority 110
 standby 30 preempt
 ip helper-address 200.100.10.5
 ip access-group STUDENT-IN in
interface vlan 40
 ip address 192.168.40.2 255.255.255.0
 standby 40 ip 192.168.40.1
 standby 40 priority 100
 standby 40 preempt
 ip helper-address 200.100.10.5
interface vlan 50
 ip address 200.100.10.2 255.255.255.0
 standby 50 ip 200.100.10.1
 standby 50 priority 110
 standby 50 preempt
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 standby 99 ip 192.168.99.1
 standby 99 priority 100
 standby 99 preempt

ip access-list extended STUDENT-IN
 deny ip 192.168.30.0 0.0.0.255 192.168.10.0 0.0.0.255
 permit ip any any

spanning-tree vlan 10,30,50 root primary
spanning-tree vlan 20,40,99 root secondary
router ospf 1
 router-id 1.1.1.1
 passive-interface default
 no passive-interface gigabitEthernet 0/1
 network 10.255.0.0 0.0.0.3 area 0
 network 192.168.0.0 0.0.255.255 area 0
 network 200.100.10.0 0.0.0.255 area 0

ntp server 200.100.10.15
logging 200.100.10.20
snmp-server community TEACHING-RO ro
end
copy running-config startup-config
```

## 20. DSW2 Configuration Differences

Use the complete DSW1 block with these deliberate replacements; every unlisted VLAN, trunk, ACL, helper, NTP, Syslog, and SNMP line remains identical.

| Item | DSW2 value |
|---|---|
| Hostname | `DSW2` |
| Routed uplink | `G0/1 = 10.255.0.6/30` |
| OSPF router ID | `2.2.2.2` |
| OSPF transit network | `10.255.0.4 0.0.0.3 area 0` |
| SVI physical address | Use `.3` instead of `.2` |
| Priority 110 | VLANs 20, 40, 99 |
| Priority 100 | VLANs 10, 30, 50 |
| STP root primary | VLANs 20, 40, 99 |
| STP root secondary | VLANs 10, 30, 50 |

This alignment keeps the HSRP active gateway on the same distribution switch as the STP root for each VLAN.

## 21. ASW1 Full Configuration

```cisco
enable
configure terminal
hostname ASW1
spanning-tree mode rapid-pvst
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 40
 name IT
vlan 50
 name SERVERS
vlan 99
 name MANAGEMENT
interface gigabitEthernet 0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface gigabitEthernet 0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface range fastEthernet 0/1 - 4
 switchport mode access
 switchport access vlan 10
interface range fastEthernet 0/5 - 8
 switchport mode access
 switchport access vlan 20
interface range fastEthernet 0/9 - 12
 switchport mode access
 switchport access vlan 30
interface range fastEthernet 0/13 - 16
 switchport mode access
 switchport access vlan 40
interface range fastEthernet 0/1 - 16
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation restrict
interface vlan 99
 ip address 192.168.99.11 255.255.255.0
 no shutdown
ip default-gateway 192.168.99.1
end
copy running-config startup-config
```

## 22. ASW2 Full Configuration

```cisco
enable
configure terminal
hostname ASW2
spanning-tree mode rapid-pvst
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 40
 name IT
vlan 50
 name SERVERS
vlan 99
 name MANAGEMENT
interface gigabitEthernet 0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface gigabitEthernet 0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface range fastEthernet 0/1 - 7
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
interface vlan 99
 ip address 192.168.99.12 255.255.255.0
 no shutdown
ip default-gateway 192.168.99.1
end
copy running-config startup-config
```

## 23. Client Configuration

Set user PCs to **DHCP**. Verify that each client receives an address from its VLAN pool, the correct HSRP gateway, and DNS server `200.100.10.10`.

Use static management addresses for infrastructure devices and static addresses for all servers.

## 24. Enterprise Acceptance Matrix

| Test | Source | Destination | Expected |
|---|---|---|---|
| DHCP | Each user VLAN | `200.100.10.5` | Correct lease through relay |
| DNS | User PC | `intranet.network.lab` | Resolves to `200.100.10.40` |
| Inter-VLAN | Administration PC | Staff PC | Success |
| Student policy | Student PC | Administration PC | Denied |
| Web | User PC | `200.100.10.40` | Page loads |
| NTP | EDGE1 and DSWs | `200.100.10.15` | Synchronized |
| Syslog | Infrastructure | `200.100.10.20` | Events received |
| SNMP | Manager `.25` | Infrastructure | System OIDs returned |
| OSPF | DSW1/DSW2 | EDGE1 | Full neighbors and routes |
| PAT | Private user VLAN | `198.51.100.1` | Success with translation |
| Server Internet | Web server | `198.51.100.1` | Success through routed public classroom subnet |
| HSRP | Client | VLAN virtual gateway | Survives active DSW failure |
| STP | PC on ASW1 | Server on ASW2 | Survives one trunk failure |
| EtherChannel | DSW1 | DSW2 | Survives one member failure |

## 25. Enterprise Troubleshooting Order

1. Verify physical links and interface state.
2. Verify VLAN creation, access membership, trunks, EtherChannel, and STP.
3. Verify SVIs, HSRP roles, helper addresses, and ACL placement.
4. Verify routed uplinks and OSPF neighbors/routes.
5. Verify each central service by IP before testing by name.
6. Verify NAT only after inside-to-edge routing works.
7. Test one redundancy failure at a time and allow convergence.
8. Record evidence in [[Testing Matrix Template]].
