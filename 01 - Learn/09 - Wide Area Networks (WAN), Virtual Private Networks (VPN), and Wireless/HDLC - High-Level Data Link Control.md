---
title: "HDLC - High-Level Data Link Control"
category: "WAN and VPN"
difficulty: "Beginner"
packet_tracer_supported: "Partial"
related_protocols:
  - "[[HDLC vs PPP]]"
  - "[[PPP - Point-to-Point Protocol]]"
tags:
  - networking
  - teaching
  - wan
aliases:
  - "HDLC"
  - "High-Level Data Link Control"
type: "reference"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# HDLC - High-Level Data Link Control

> [!abstract]
> Cisco HDLC is the default proprietary serial encapsulation on many Cisco router interfaces.

> [!info] Packet Tracer Support: Partial
> Packet Tracer demonstrates only part of this technology. Use Wireshark, GNS3, EVE-NG, Cisco CML, Linux, or real hardware for missing behavior.

## 1. What Is It?

Cisco HDLC is the default proprietary serial encapsulation on many Cisco router interfaces.

## 2. Why Do We Use It?

It gives engineers a defined method to build, operate, verify, or troubleshoot this part of a network. Students should connect the concept to observable frames, packets, device state, and user impact.

## 3. Where Is It Used?

It is used in wan and vpn designs, Cisco IOS teaching labs, operational verification, and fault isolation. The exact platform support depends on the selected switch, router, server, or endpoint.

## 4. How It Works

1. Frames carry a Cisco type field
2. No authentication is provided
3. Both ends must use compatible encapsulation

## 5. Important Terminology

- **Key idea 1:** Frames carry a Cisco type field
- **Key idea 2:** No authentication is provided
- **Key idea 3:** Both ends must use compatible encapsulation

## 6. Technical Classification

| Item | Value |
|---|---|
| OSI layer | Layer 2 |
| Port numbers | Not applicable |
| IP protocol number | Not applicable |
| Packet Tracer support | Partial |



## 8. Advantages

- Provides a standard and repeatable operational method.
- Improves visibility, interoperability, availability, or control when designed correctly.
- Can be verified with explicit state, counters, messages, or packet captures.

## 9. Limitations and Risks

- Incorrect addressing, interface state, VLAN membership, timers, or policy can prevent operation.
- Packet Tracer may omit advanced features or detailed debug output.
- Security and scale requirements are greater in production than in a classroom lab.

## 10. Requirements

- A documented topology and addressing plan.
- Correct device and interface capabilities.
- Baseline connectivity before advanced configuration.
- A verification and rollback plan.

## 11. Practical Topology

```text
Source/Client ---- Network Device(s) ---- Destination/Service
        |                 |
        +------ verification points -----+
```

## 12. Configuration or Demonstration

This focused note explains one part of the subject. Use the related configuration note or Packet Tracer lab for device-by-device commands. For a theory-only topic, demonstrate the behavior with Packet Tracer Simulation Mode or Wireshark rather than inventing an IOS configuration.

## 13. Verification Commands

- Confirm the expected state at every participating device.

## 14. Expected Result

The intended adjacency, route, service, security policy, or forwarding state should be visible in verification output and confirmed with an end-to-end test.

## 15. Testing Procedure

1. Verify cabling and interface state.
2. Verify Layer 2 membership and forwarding where applicable.
3. Verify IP addressing and routing.
4. Verify the technology-specific state or service.
5. Test from an endpoint.
6. Introduce one controlled failure and confirm the expected response.

## 16. Troubleshooting

| Check | Expected | Typical fix |
|---|---|---|
| Physical/interface state | Required interfaces are up | Correct cable, module, interface, or `no shutdown` |
| Addressing or VLAN | Matches the design table | Correct address, mask, gateway, VLAN, or trunk list |
| Protocol/service state | Required relationship is established | Correct peer, timer, process, server, or policy |
| End-to-end test | Expected traffic succeeds | Follow the path and isolate the first failing hop |

## 17. Common Errors

- Applying a correct command to the wrong device or interface.
- Using an address, mask, wildcard, VLAN, or next hop that does not match the plan.
- Testing an advanced feature before baseline connectivity works.
- Assuming Packet Tracer supports every production IOS command.

## 18. Security Considerations

Use least privilege, authenticated management, trusted peers, restricted infrastructure access, and logging. Replace classroom passwords, community strings, and shared keys before production use.

## 19. Student Exercise

### Beginner

Draw the message or forwarding path and identify every device, address, interface, and verification point.

### Intermediate

Build a small Packet Tracer topology and prove the expected behavior with at least two verification commands.

### Advanced

Introduce one realistic fault, diagnose it without deleting the configuration, repair it, and document the evidence.

## 20. Viva Questions

1. What problem does HDLC solve?
2. Which device state or packet exchange proves it is working?
3. What is the most likely configuration error in a Packet Tracer lab?
4. What additional control would be required in production?

## 21. Quick Revision

- **What:** Cisco HDLC is the default proprietary serial encapsulation on many Cisco router interfaces.
- **Why:** To produce predictable, verifiable network behavior.
- **Verify:** Inspect the relevant interface, table, adjacency, service, or policy and then run an end-to-end test.
- **Troubleshoot:** Start with physical state and follow the path upward through the OSI model.

## 22. Lecturer Notes

- Start with the user-visible problem before introducing commands.
- Draw the packet or control-message path and ask students to predict the next step.
- Demonstrate one correct build and one deliberately broken build.
- Common Packet Tracer mistakes are wrong interfaces, missing `no shutdown`, mismatched VLANs, and premature testing.

## 23. Related Notes

- [[HDLC vs PPP]]
- [[PPP - Point-to-Point Protocol]]
