---
title: "Security Configuration Guide"
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

# Security Configuration Guide

Complete these notes in order. Each guide includes a topology, addressing plan, exact device configuration, verification, testing, and troubleshooting.

1. [[25 - SSH - Secure Shell Remote Management - Step by Step]] — Secure remote Cisco IOS management with Secure Shell (SSH) version 2, a local privileged user, RSA keys, and SSH-only virtual terminal lines.
2. [[26 - AAA - Authentication, Authorization, and Accounting with Local Users - Step by Step]] — Enable Authentication, Authorization, and Accounting (AAA), apply a local login method list to SSH, and preserve console recovery access.
3. [[27 - RADIUS and TACACS+ Central AAA - Step by Step]] — Authenticate SSH administrators against a central Remote Authentication Dial-In User Service (RADIUS) or Terminal Access Controller Access-Control System Plus (TACACS+) server with a local fallback.
4. [[28 - Standard IPv4 ACL - Access Control List - Step by Step]] — Use a standard IPv4 Access Control List (ACL) near the destination to block one source subnet while permitting all other sources.
5. [[29 - Extended and Named IPv4 ACL - Access Control List - Step by Step]] — Permit web and Domain Name System (DNS) traffic from a user subnet to a server while denying other traffic, using a named extended IPv4 ACL near the source.
6. [[30 - NAT and PAT - Network and Port Address Translation - Step by Step]] — Configure inside/outside roles and demonstrate static Network Address Translation (NAT), dynamic pooled NAT, and Port Address Translation (PAT) as separate alternatives.
7. [[30A - Telnet Legacy Remote Management - Step by Step]] — Configure Telnet only for a controlled legacy-protocol demonstration, observe that it lacks strong encryption, and then replace it with Secure Shell (SSH).

Return to [[Configuration Library Dashboard]].
