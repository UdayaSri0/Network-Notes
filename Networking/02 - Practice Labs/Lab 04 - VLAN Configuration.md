---
title: "Lab 04 - VLAN Configuration"
category: "Packet Tracer Labs"
difficulty: "Beginner"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[VLAN - Virtual Local Area Network]]"
  - "[[VLAN Configuration]]"
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

# Lab 04 - VLAN Configuration

> [!abstract]
> Create Administration, Staff, and Students VLANs and place endpoint ports correctly.

> [!info] Packet Tracer Support: Yes
> Confirm every required command on the selected Packet Tracer device model. Use GNS3, EVE-NG, Cisco CML, Wireshark, Linux, or real hardware when a listed feature is partial.

## 1. Learning Objectives

- Explain the purpose of the technology before configuring it.
- Build and address the topology from a documented plan.
- Apply device-specific configuration in the correct mode.
- Verify operation with commands and endpoint tests.
- Diagnose one controlled failure without erasing the configuration.

## 2. Required Devices

2 switches, 6 PCs

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

1. Create VLANs 10, 20, and 30 on both switches.
2. Assign two access ports per VLAN.
3. Verify VLAN membership before adding trunks.
4. Test same-switch same-VLAN behavior.

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
| Test 1 | Same-VLAN local pings succeed | Success |
| Test 2 | Different VLANs remain isolated | Success |

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

- [[VLAN - Virtual Local Area Network]]
- [[VLAN Configuration]]
- [[Networking Dashboard]]
