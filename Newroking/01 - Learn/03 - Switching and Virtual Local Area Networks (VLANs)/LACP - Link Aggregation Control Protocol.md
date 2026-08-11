---
title: "LACP - Link Aggregation Control Protocol"
category: "Switching"
difficulty: "Beginner"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[EtherChannel]]"
  - "[[PAgP - Port Aggregation Protocol]]"
tags:
  - networking
  - teaching
  - switching
aliases:
  - "LACP"
  - "Link Aggregation Control Protocol"
type: "reference"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# LACP - Link Aggregation Control Protocol

> [!abstract]
> LACP is the standards-based EtherChannel negotiation protocol using active and passive modes.

> [!info] Packet Tracer Support: Yes
> Packet Tracer can demonstrate the essential behavior in this note.

## 1. What Is It?

LACP is the standards-based EtherChannel negotiation protocol using active and passive modes.

## 2. Why Do We Use It?

It gives engineers a defined method to build, operate, verify, or troubleshoot this part of a network. Students should connect the concept to observable frames, packets, device state, and user impact.

## 3. Where Is It Used?

It is used in switching designs, Cisco IOS teaching labs, operational verification, and fault isolation. The exact platform support depends on the selected switch, router, server, or endpoint.

## 4. How It Works

1. Active initiates negotiation
2. Passive responds
3. At least one side must be active
4. Members must have consistent settings

## 5. Important Terminology

- **Key idea 1:** Active initiates negotiation
- **Key idea 2:** Passive responds
- **Key idea 3:** At least one side must be active
- **Key idea 4:** Members must have consistent settings

## 6. Technical Classification

| Item | Value |
|---|---|
| OSI layer | Layer 2 |
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

## 12. Step-by-Step Configuration

> [!note]
> Interface names are examples. Confirm the actual Packet Tracer device interfaces before applying the configuration.

```cisco
enable
configure terminal
interface range gigabitEthernet 0/1 - 2
 channel-group 1 mode active
interface port-channel 1
 switchport mode trunk
```

Save IOS configurations with:

```cisco
end
copy running-config startup-config
```

## 13. Verification Commands

- `show etherchannel summary`
- `show interfaces port-channel 1`

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

1. What problem does LACP solve?
2. Which device state or packet exchange proves it is working?
3. What is the most likely configuration error in a Packet Tracer lab?
4. What additional control would be required in production?

## 21. Quick Revision

- **What:** LACP is the standards-based EtherChannel negotiation protocol using active and passive modes.
- **Why:** To produce predictable, verifiable network behavior.
- **Verify:** Inspect the relevant interface, table, adjacency, service, or policy and then run an end-to-end test.
- **Troubleshoot:** Start with physical state and follow the path upward through the OSI model.

## 22. Lecturer Notes

- Start with the user-visible problem before introducing commands.
- Draw the packet or control-message path and ask students to predict the next step.
- Demonstrate one correct build and one deliberately broken build.
- Common Packet Tracer mistakes are wrong interfaces, missing `no shutdown`, mismatched VLANs, and premature testing.

## 23. Related Notes

- [[EtherChannel]]
- [[PAgP - Port Aggregation Protocol]]
