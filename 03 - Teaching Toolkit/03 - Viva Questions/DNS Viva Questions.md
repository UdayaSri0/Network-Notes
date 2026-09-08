---
title: "DNS Viva Questions"
category: "Viva and Revision Questions"
difficulty: "Mixed"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[DNS - Domain Name System]]"
  - "[[Packet Tracer DNS Server]]"
  - "[[DNS Troubleshooting]]"
tags:
  - networking
  - viva
  - teaching
type: "question-bank"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# DNS Viva Questions

> [!abstract]
> 25 questions with answers: 10 beginner, 10 intermediate, and 5 advanced.

## Beginner Questions

### 1. What is DNS?

**Answer:** DNS resolves names into addresses and stores other domain information in distributed records.

### 2. Why is DNS used?

**Answer:** It provides predictable network behavior that can be designed, verified, and troubleshot rather than relying on accidental defaults.

### 3. Which OSI layer is most closely associated with DNS?

**Answer:** Layer 7

### 4. Which port or protocol number is important for DNS?

**Answer:** UDP/TCP 53

### 5. Name two important DNS terms.

**Answer:** A resolver sends a query, Recursive servers follow referrals or use cache, Authoritative servers answer for their zones, The result is cached for its TTL

### 6. Is DNS supported in Packet Tracer?

**Answer:** Packet Tracer Support: Yes. Always confirm the selected model and image.

### 7. What should be checked before configuring DNS?

**Answer:** Check cabling, interface state, addressing, VLANs, and baseline reachability first.

### 8. Which command can help verify DNS?

**Answer:** the relevant show command and an end-to-end test

### 9. What is one common classroom mistake with DNS?

**Answer:** Students often use the correct command on the wrong interface or with values that do not match the topology plan.

### 10. How should a student prove DNS works?

**Answer:** Show the relevant device state and then demonstrate the expected end-to-end traffic or service result.

## Intermediate Questions

### 1. Describe the operational sequence for DNS.

**Answer:** Follow these core ideas in order: A resolver sends a query, Recursive servers follow referrals or use cache, Authoritative servers answer for their zones, The result is cached for its TTL. Explain the control information and resulting forwarding or service state.

### 2. How would you design a small DNS lab?

**Answer:** Use the fewest devices that still expose the control exchange, one successful path, one verification point, and one controlled failure.

### 3. How do you distinguish a DNS fault from a physical fault?

**Answer:** Verify link and interface state first. If Layer 1 is healthy, compare the technology-specific state and counters.

### 4. How do you distinguish a DNS fault from an IP addressing fault?

**Answer:** Verify the local address, mask, gateway, and routing independently before interpreting protocol state.

### 5. What output would you record before changing DNS?

**Answer:** Record the relevant show command and an end-to-end test, interface state, relevant configuration, and an endpoint test.

### 6. Why should only one variable be changed during DNS troubleshooting?

**Answer:** A controlled change preserves evidence and shows whether the tested theory was correct.

### 7. What security concern applies to DNS?

**Answer:** Restrict infrastructure access, authenticate peers or managers where supported, use least privilege, and log changes.

### 8. What Packet Tracer limitation can affect DNS?

**Answer:** Packet Tracer may omit advanced commands, packet details, scale, timers, cryptography, or production debug output.

### 9. How would you document a working DNS configuration?

**Answer:** Record topology, interface and address tables, device-specific blocks, verification output, tests, and known platform limitations.

### 10. How would you create a useful DNS failure demonstration?

**Answer:** Introduce one realistic fault, ask students to predict the changed output, verify the symptom, repair the cause, and retest.

## Advanced Questions

### 1. How would DNS change in a larger enterprise?

**Answer:** Add hierarchy, redundancy, security policy, scale boundaries, centralized monitoring, configuration standards, and rollback planning.

### 2. How would you validate DNS during a change window?

**Answer:** Capture a baseline, apply staged changes, run protocol and end-to-end tests, monitor logs, and execute rollback if acceptance criteria fail.

### 3. Which hidden dependency can make DNS appear correctly configured but still fail?

**Answer:** Return routing, an upstream policy, time, name resolution, VLAN transport, or a platform capability can fail outside the local configuration.

### 4. How would you secure and monitor DNS in production?

**Answer:** Use trusted peers, authentication and encryption where available, infrastructure ACLs, centralized logs, metrics, and alert thresholds.

### 5. How would you teach DNS without encouraging command memorization?

**Answer:** Begin with the failure it solves, visualize the packet or state transition, have students predict output, then map each command to one design requirement.

## Related Notes

- [[DNS - Domain Name System]]
- [[Packet Tracer DNS Server]]
- [[DNS Troubleshooting]]
