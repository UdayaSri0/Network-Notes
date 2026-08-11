---
title: "Lab 07 - Multilayer Switch Inter-VLAN Routing"
category: "Packet Tracer Labs"
difficulty: "Intermediate"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[Layer 3 Switch Inter-VLAN Routing]]"
  - "[[SVI Routing]]"
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

# Lab 07 - Multilayer Switch Inter-VLAN Routing

> [!abstract]
> Use SVIs and ip routing to route between VLANs on a multilayer switch.

> [!info] Packet Tracer Support: Yes
> Confirm every required command on the selected Packet Tracer device model. Use GNS3, EVE-NG, Cisco CML, Wireshark, Linux, or real hardware when a listed feature is partial.

## 1. Learning Objectives

- Explain the purpose of the technology before configuring it.
- Build and address the topology from a documented plan.
- Apply device-specific configuration in the correct mode.
- Verify operation with commands and endpoint tests.
- Diagnose one controlled failure without erasing the configuration.

## 2. Required Devices

1 multilayer switch, 2 access switches, 6 PCs

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

1. Create VLANs on all switches.
2. Configure access and trunk ports.
3. Create one SVI per VLAN on the multilayer switch.
4. Enable ip routing and verify connected routes.

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
| Test 1 | SVIs are up/up | Success |
| Test 2 | All VLANs route through the multilayer switch | Success |

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

- [[Layer 3 Switch Inter-VLAN Routing]]
- [[SVI Routing]]
- [[Networking Dashboard]]
