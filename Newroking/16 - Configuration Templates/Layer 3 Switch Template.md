---
title: "Layer 3 Switch Template"
category: "Configuration Templates"
difficulty: "Intermediate"
packet_tracer_supported: "Yes"
related_protocols:
  - "[[Cisco Multilayer Switch Configuration]]"
  - "[[Cisco Troubleshooting Commands]]"
tags:
  - networking
  - cisco
  - configuration-template
type: "template"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# Layer 3 Switch Template

> [!abstract]
> Reusable Cisco IOS skeleton. Replace every angle-bracket placeholder and verify device interface names before use.

## 1. Placeholders

- `<INTERFACE>` or a named variant: actual interface from `show ip interface brief` or `show interfaces status`.
- `<NETWORK>`, `<SUBNET-MASK>`, and `<WILDCARD>`: values validated against the addressing plan.
- `<VLAN-ID>` and `<VLAN-LIST>`: values matching the VLAN and trunk tables.
- `<NEXT-HOP>` or server IP: reachable address in the correct routed path.
- Secrets and communities: unique classroom values that must be replaced in production.

## 2. Configuration

```cisco
enable
configure terminal
hostname <L3-SWITCH-NAME>
ip routing
vlan <VLAN-ID>
 name <VLAN-NAME>
interface vlan <VLAN-ID>
 ip address <GATEWAY> <SUBNET-MASK>
 no shutdown
interface <ROUTED-INTERFACE>
 no switchport
 ip address <TRANSIT-IP> <TRANSIT-MASK>
 no shutdown
end
copy running-config startup-config
```

## 3. Verification

```cisco
show running-config
show ip interface brief
```

Add the technology-specific `show` commands from the related note.

## 4. Quality Checklist

- [ ] Every placeholder was replaced.
- [ ] Interface names exist on the chosen model.
- [ ] Addresses, masks, and wildcards were recalculated.
- [ ] VLAN IDs match on access and trunk links.
- [ ] Required interfaces include `no shutdown`.
- [ ] Verification passed before the configuration was saved.

## 5. Related Notes

- [[Cisco Multilayer Switch Configuration]]
- [[Cisco Troubleshooting Commands]]
- [[Networking Dashboard]]
