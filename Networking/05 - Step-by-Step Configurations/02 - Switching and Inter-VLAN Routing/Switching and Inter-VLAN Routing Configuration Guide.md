---
title: "Switching and Inter-VLAN Routing Configuration Guide"
category: "Step-by-Step Configuration"
difficulty: "Mixed"
packet_tracer_supported: "Mixed"
related_protocols:
  - "[[Configuration Library Dashboard]]"
tags:
  - networking
  - cisco
  - configuration
  - index
---

# Switching and Inter-VLAN Routing Configuration Guide

Complete these notes in order. Each guide includes a topology, addressing plan, exact device configuration, verification, testing, and troubleshooting.

1. [[05 - VLAN - Virtual Local Area Network Configuration - Step by Step]] — Create three Virtual Local Area Networks (VLANs), assign access ports, and prove that each VLAN forms a separate Layer 2 broadcast domain.
2. [[06 - IEEE 802.1Q Trunk Configuration - Step by Step]] — Carry VLANs 10, 20, 30, and 99 between two switches over a statically configured IEEE 802.1Q trunk.
3. [[07 - Router-on-a-Stick Inter-VLAN Routing - Step by Step]] — Route traffic among VLANs 10, 20, and 30 by using one router interface with IEEE 802.1Q subinterfaces.
4. [[08 - Multilayer Switch Inter-VLAN Routing - Step by Step]] — Use switched virtual interfaces on a multilayer switch to route traffic among three VLANs.
5. [[09 - STP - Spanning Tree Protocol Root Bridge Configuration - Step by Step]] — Build a redundant triangle and deliberately select the primary and secondary Spanning Tree Protocol (STP) root bridges for VLAN 10.
6. [[10 - RSTP - Rapid Spanning Tree Protocol with PortFast and BPDU Guard - Step by Step]] — Enable Rapid Per-VLAN Spanning Tree, accelerate edge-port forwarding with PortFast, and protect an edge port with Bridge Protocol Data Unit (BPDU) Guard.
7. [[11 - EtherChannel with LACP and PAgP - Step by Step]] — Bundle two physical links into one logical trunk using Link Aggregation Control Protocol (LACP), and show the equivalent Port Aggregation Protocol (PAgP) modes.
8. [[12 - Switch Port Security - Step by Step]] — Limit an access port to learned Media Access Control (MAC) addresses and compare protect, restrict, and shutdown violation behaviour.
9. [[13 - DHCP Snooping, Dynamic ARP Inspection, and IP Source Guard - Step by Step]] — Protect a user VLAN from rogue Dynamic Host Configuration Protocol (DHCP) replies, forged Address Resolution Protocol (ARP) messages, and source-address spoofing.

Return to [[Configuration Library Dashboard]].
