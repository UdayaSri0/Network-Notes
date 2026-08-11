---
title: "Subnetting Step by Step"
category: "IP Addressing and Subnetting"
difficulty: "Beginner"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[Subnetting Basics]]"
  - "[[VLSM]]"
tags:
  - networking
  - teaching
  - subnetting
type: "reference"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# Subnetting Step by Step

> [!abstract]
> A repeatable subnetting method calculates network, broadcast, first host, last host, and capacity from an address and prefix.

> [!info] Packet Tracer Support: Yes
> Packet Tracer can demonstrate the essential behavior in this note.

## 1. What Is It?

A repeatable subnetting method calculates network, broadcast, first host, last host, and capacity from an address and prefix.

## 2. Why Do We Use It?

It gives engineers a defined method to build, operate, verify, or troubleshoot this part of a network. Students should connect the concept to observable frames, packets, device state, and user impact.

## 3. Where Is It Used?

It is used in ip addressing and subnetting designs, Cisco IOS teaching labs, operational verification, and fault isolation. The exact platform support depends on the selected switch, router, server, or endpoint.

## 4. How It Works

1. Convert the prefix to a mask
2. Identify the interesting octet
3. Calculate block size as 256 minus the mask value
4. Locate the address inside its block
5. Derive usable boundaries

## 5. Important Terminology

- **Key idea 1:** Convert the prefix to a mask
- **Key idea 2:** Identify the interesting octet
- **Key idea 3:** Calculate block size as 256 minus the mask value
- **Key idea 4:** Locate the address inside its block
- **Key idea 5:** Derive usable boundaries

## 6. Technical Classification

| Item | Value |
|---|---|
| OSI layer | Varies |
| Port numbers | Not applicable |
| IP protocol number | Not applicable |
| Packet Tracer support | Yes |



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

1. What problem does Subnetting Step by Step solve?
2. Which device state or packet exchange proves it is working?
3. What is the most likely configuration error in a Packet Tracer lab?
4. What additional control would be required in production?

## 21. Quick Revision

- **What:** A repeatable subnetting method calculates network, broadcast, first host, last host, and capacity from an address and prefix.
- **Why:** To produce predictable, verifiable network behavior.
- **Verify:** Inspect the relevant interface, table, adjacency, service, or policy and then run an end-to-end test.
- **Troubleshoot:** Start with physical state and follow the path upward through the OSI model.

## 22. Lecturer Notes

- Start with the user-visible problem before introducing commands.
- Draw the packet or control-message path and ask students to predict the next step.
- Demonstrate one correct build and one deliberately broken build.
- Common Packet Tracer mistakes are wrong interfaces, missing `no shutdown`, mismatched VLANs, and premature testing.

## 23. Related Notes

- [[Subnetting Basics]]
- [[VLSM]]

## Worked Examples

### 192.168.1.0/27

- Mask: `255.255.255.224`
- Block size: `32`
- First subnet: network `.0`, hosts `.1-.30`, broadcast `.31`
- Second subnet: network `.32`, hosts `.33-.62`, broadcast `.63`

### 200.100.10.0/28

- Mask: `255.255.255.240`
- Block size: `16`
- First subnet: network `.0`, hosts `.1-.14`, broadcast `.15`
- Next subnet begins at `.16`

### Address 172.16.20.140/23

- Mask: `255.255.254.0`
- Third-octet block size: `2`
- Network: `172.16.20.0`
- Usable range: `172.16.20.1-172.16.21.254`
- Broadcast: `172.16.21.255`
