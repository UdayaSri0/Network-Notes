---
title: Spanning Tree Protocol - Four-Switch Packet Tracer Lab
aliases:
  - STP Four-Switch Lab
  - Rapid PVST+ VLAN 10 and 20 Practical
tags:
  - networking
  - cisco
  - packet-tracer
  - stp
  - rapid-pvst
  - switching
created: 2026-09-20
---

# Spanning Tree Protocol - Four-Switch Packet Tracer Lab

## Goal and lab files

Use the supplied four-switch topology to configure **Rapid PVST+**, make the left multilayer switch the preferred root for VLAN 10, make the right multilayer switch the preferred root for VLAN 20, and prove that a redundant path takes over after an uplink fails.

- Packet Tracer project: [[STP.pkt]]
- Supplied topology image: [[Screenshot 2026-09-20 120030.png]]

![[Screenshot 2026-09-20 120030.png]]

> [!note] What the screenshot does and does not show
> The picture shows **two 3650 multilayer switches**, **two 2960 access switches**, four inter-switch links, four PCs, and VLAN 10/20 areas. Some device/port labels overlap. The names and addressing below are a clear **proposed lab configuration**, not settings proven to be saved in `STP.pkt`. Check the actual connected ports in Packet Tracer before pasting commands. The orange indicator in the screenshot alone does not prove a particular VLAN's final STP role.

## 1. Understand the topology

| Name used here | Device in image | Role |
|---|---|---|
| `DSW1` | Upper-left 3650 (`Multilayer Switch2`) | Preferred VLAN 10 root |
| `DSW2` | Upper-right 3650 | Preferred VLAN 20 root |
| `ASW10` | Lower-left 2960 (`Switch0`) | PC0 and PC1, VLAN 10 |
| `ASW20` | Lower-right 2960 | PC2 and PC3, VLAN 20 |

The four inter-switch links form a Layer 2 cycle: `DSW1 → ASW10 → DSW2 → ASW20 → DSW1`. Each link must carry **both VLAN 10 and VLAN 20** as an 802.1Q trunk for both VLANs to have redundant paths. The yellow and blue areas identify where the pictured PCs attach; they do not mean the uplinks carry only one VLAN.

### Cable and port map

| Link | First port | Second port | Configuration |
|---|---|---|---|
| Left vertical | `DSW1 Gi1/0/1` | `ASW10 Gi0/1` | Trunk, VLANs 10 and 20 |
| Left-to-right diagonal | `DSW1 Gi1/0/2` | `ASW20 Gi0/1` | Trunk, VLANs 10 and 20 |
| Right-to-left diagonal | `DSW2 Gi1/0/1` | `ASW10 Gi0/2` | Trunk, VLANs 10 and 20 |
| Right vertical | `DSW2 Gi1/0/2` | `ASW20 Gi0/2` | Trunk, VLANs 10 and 20 |
| PC0 | `PC0 Fa0` | `ASW10 Fa0/1` | Access VLAN 10 |
| PC1 | `PC1 Fa0` | `ASW10 Fa0/2` | Access VLAN 10 |
| PC2 | `PC2 Fa0` | `ASW20 Fa0/1` | Access VLAN 20 |
| PC3 | `PC3 Fa0` | `ASW20 Fa0/2` | Access VLAN 20 |

> [!important] Verify port labels first
> The upper-right labels are partly obscured. If a cable ends on a different `Gi` port in `STP.pkt`, use that real port in the commands. Packet Tracer's **Connections** view or clicking a cable gives both endpoints. Do not assume the diagonal lines connect at their visual crossing; there is no switch at that crossing.

## 2. STP concepts needed for this lab

- A Layer 2 loop can duplicate broadcast/unknown frames and cause MAC address instability. STP keeps a loop-free **forwarding** tree while retaining redundant physical links.
- Each Rapid PVST+ VLAN has its **own** tree and root bridge. A switch can be the root for VLAN 10 and another switch the root for VLAN 20.
- Switches elect the root by the **lowest bridge ID**: configured priority plus VLAN system ID extension, then MAC address. Lower priority wins. Priorities use increments of 4096.
- Each non-root switch selects a **root port** with the best path to the root. The root has only **designated** ports. A redundant path can become an **alternate** port in **discarding** state (some Packet Tracer output may call it **blocking**).
- The forwarding choice considers root path cost and then bridge/port ID tie breakers. The exact blocked physical port can depend on the switches' MAC addresses and link costs. Verify it; do not infer it from cable color.
- Rapid PVST+ uses forwarding, learning, and discarding states. Classic 802.1D STP also describes listening and blocking separately. In either mode, a blocked/discarding port still participates in STP through BPDUs.
- `PortFast` is for PC-facing edge ports. `BPDU Guard` disables such a port if it unexpectedly receives a BPDU. **Never enable PortFast on the four switch-to-switch trunks.**
- STP controls Layer 2 paths. It does **not** provide inter-VLAN routing or a default gateway.

### Intended root plan

| VLAN | Preferred root | Root priority | Other distribution switch | Its priority | Access switch priority |
|---|---|---:|---|---:|---:|
| 10 | `DSW1` | `24576` | `DSW2` | `28672` | default `32768` |
| 20 | `DSW2` | `24576` | `DSW1` | `28672` | default `32768` |

With the VLAN system ID extension, a displayed VLAN 10 priority of `24586` means base priority `24576` + VLAN ID `10`. VLAN 20 similarly displays `24596` on its preferred root. The backup priorities display `28682` and `28692`.

## 3. Prepare Packet Tracer

1. Open [[STP.pkt]] and save a working copy if you want to preserve its starting state.
2. Confirm that all four inter-switch cables and four PC cables match the port map above. Use Packet Tracer's automatic cable choice if rebuilding a link.
3. Open each device's **CLI** tab. If a device asks whether to enter the initial configuration dialog, answer `no` and press Enter.
4. If you already configured any of these VLANs or trunk ports, inspect their current configuration before applying this sample. The commands below assume a clean or compatible configuration.

## 4. Configure the switches

Create VLANs 10 and 20 on **all four switches**. Make the four uplinks trunks that allow both VLANs. Give only the host ports access VLAN membership.

### DSW1 — VLAN 10 root, VLAN 20 backup

```cisco
enable
configure terminal
hostname DSW1
spanning-tree mode rapid-pvst
vlan 10
 name VLAN10_USERS
exit
vlan 20
 name VLAN20_USERS
exit
interface range GigabitEthernet1/0/1 - 2
 description Inter-switch trunk
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 no shutdown
exit
spanning-tree vlan 10 priority 24576
spanning-tree vlan 20 priority 28672
end
copy running-config startup-config
```

### DSW2 — VLAN 20 root, VLAN 10 backup

```cisco
enable
configure terminal
hostname DSW2
spanning-tree mode rapid-pvst
vlan 10
 name VLAN10_USERS
exit
vlan 20
 name VLAN20_USERS
exit
interface range GigabitEthernet1/0/1 - 2
 description Inter-switch trunk
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 no shutdown
exit
spanning-tree vlan 10 priority 28672
spanning-tree vlan 20 priority 24576
end
copy running-config startup-config
```

### ASW10 — PC0 and PC1 in VLAN 10

```cisco
enable
configure terminal
hostname ASW10
spanning-tree mode rapid-pvst
vlan 10
 name VLAN10_USERS
exit
vlan 20
 name VLAN20_USERS
exit
interface range GigabitEthernet0/1 - 2
 description Inter-switch trunk
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 no shutdown
exit
interface range FastEthernet0/1 - 10
 description VLAN10 PCs
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit
end
copy running-config startup-config
```

### ASW20 — PC2 and PC3 in VLAN 20

```cisco
enable
configure terminal
hostname ASW20
spanning-tree mode rapid-pvst
vlan 10
 name VLAN10_USERS
exit
vlan 20
 name VLAN20_USERS
exit
interface range GigabitEthernet0/1 - 2
 description Inter-switch trunk
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 no shutdown
exit
interface range FastEthernet0/1 - 10
 description VLAN20 PCs
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit
end
copy running-config startup-config
```

> [!tip] If a 3650 rejects a trunk command
> First confirm the real interface name and that it is operating as a Layer 2 `switchport`. Some multilayer switch interfaces can be routed ports; enter `switchport` in interface configuration mode if the interface was previously changed to `no switchport`. The shown 3650/2960 trunks use 802.1Q; no `switchport trunk encapsulation dot1q` command is needed on models that offer only 802.1Q.

## 5. Set PC addresses

In each PC, open **Desktop → IP Configuration → Static**. These are private **sample** addresses for this isolated lab; the supplied image does not show IP addresses.

| PC  | VLAN | IP address      | Mask            | Default gateway |
| --- | ---: | --------------- | --------------- | --------------- |
| PC0 |   10 | `192.168.10.10` | `255.255.255.0` | leave blank     |
| PC1 |   10 | `192.168.10.11` | `255.255.255.0` | leave blank     |
| PC2 |   20 | `192.168.20.10` | `255.255.255.0` | leave blank     |
| PC3 |   20 | `192.168.20.11` | `255.255.255.0` | leave blank     |

No switch virtual interfaces or `ip routing` are required for the **STP-only baseline**. PC0↔PC1 and PC2↔PC3 should communicate within their own VLAN. PC0↔PC2 should **not** communicate until you complete the optional inter-VLAN routing extension in section 8.

## 6. Verify VLANs, trunks, and STP

Run these commands on **each switch** after the links settle:

```cisco
show vlan brief
show interfaces trunk
show spanning-tree summary
show spanning-tree vlan 10
show spanning-tree vlan 20
```

Check the results in order:

1. `show vlan brief`: VLANs 10 and 20 exist. ASW10 `Fa0/1-2` belong to VLAN 10; ASW20 `Fa0/1-2` belong to VLAN 20. Trunk ports normally do not appear as access members in this list.
2. `show interfaces trunk`: the two uplinks on every switch are trunking and show **10,20** in the allowed and active VLAN lists. A VLAN may be allowed but absent from **forwarding and not pruned** on one port because STP is discarding it; that is expected.
3. `show spanning-tree summary`: the mode is Rapid PVST+ (wording varies by software version).
4. `show spanning-tree vlan 10`: `DSW1` says **This bridge is the root**; every switch reports `DSW1`'s bridge ID as the root ID.
5. `show spanning-tree vlan 20`: `DSW2` says **This bridge is the root**; every switch reports `DSW2`'s bridge ID as the root ID.
6. In each VLAN's port table, identify `Root`, `Desg`, and `Altn` roles and `FWD`/`BLK` (or discarding) states. Expect at least one redundant inter-switch port per VLAN not to forward in a stable four-link cycle. The actual interface can differ between VLANs and Packet Tracer runs.

Record what **your** simulation shows:

| VLAN | Root switch seen | Alternate/discarding switch and port | Active trunk path between access switches |
|---|---|---|---|
| 10 | | | |
| 20 | | | |

> [!note] Why a PC ping alone is insufficient
> PC0 and PC1 are on **the same access switch**; so are PC2 and PC3. Their pings can pass locally even if an uplink is broken. Use the cross-switch test below to observe redundant-path failover in the data plane.

## 7. Test PC connectivity

From **PC0 → Desktop → Command Prompt**:

```text
ping 192.168.10.11
ping 192.168.20.10
```

The first should succeed after ARP resolves. The second should fail because it crosses VLANs without routing. From PC2, `ping 192.168.20.11` should succeed.

### Optional cross-switch VLAN 10 test that actually uses the uplinks

Temporarily use PC2 as a VLAN 10 host on **ASW20**. PC3 remains in VLAN 20. Do this only after recording the normal VLAN 20 baseline.

1. On ASW20, move only the PC2 port into VLAN 10:

   ```cisco
   enable
   configure terminal
   interface FastEthernet0/1
    switchport access vlan 10
   end
   ```

2. On PC2, change its address to `192.168.10.12 / 255.255.255.0`; leave the gateway blank.
3. From PC0, run `ping 192.168.10.12`. This traffic must cross the inter-switch network because the PCs are on different access switches.
4. Run `show spanning-tree vlan 10` on all four switches. Record the forwarding and alternate ports.
5. To simulate a failure, shut down **DSW1's link to ASW20** (shown as `Gi1/0/2`):

   ```cisco
   DSW1# configure terminal
   DSW1(config)# interface GigabitEthernet1/0/2
   DSW1(config-if)# shutdown
   DSW1(config-if)# end
   ```

6. Wait for reconvergence, then repeat the ping and `show spanning-tree vlan 10`. The remaining path through `DSW2` should carry the VLAN 10 traffic. A ping or two can time out during the change. Packet Tracer timing is illustrative; do not claim a measured recovery time from the picture.
7. Restore the uplink and check the roles again:

   ```cisco
   DSW1# configure terminal
   DSW1(config)# interface GigabitEthernet1/0/2
   DSW1(config-if)# no shutdown
   DSW1(config-if)# end
   ```

8. Restore ASW20 `Fa0/1` to VLAN 20 and PC2 to `192.168.20.10 / 255.255.255.0`:

   ```cisco
   ASW20# configure terminal
   ASW20(config)# interface FastEthernet0/1
   ASW20(config-if)# switchport access vlan 20
   ASW20(config-if)# end
   ```

9. Confirm PC2 can again ping PC3 at `192.168.20.11`. Save the restored switch configurations with `copy running-config startup-config` and save the Packet Tracer file if this is the state you want to keep.

For a VLAN 20 failover exercise, temporarily place one PC on ASW10 in VLAN 20 with a `192.168.20.x/24` address, keep a VLAN 20 PC on ASW20, and repeat the same method while taking down the appropriate **active** DSW2 uplink. Restore its VLAN and IP afterward.

## 8. Optional next step — enable inter-VLAN routing

Complete the STP baseline and restore any temporary PC/VLAN changes from section 7 first. To make **PC0/PC1 communicate with PC2/PC3**, use the upper-left **3650 DSW1** as the gateway for both VLANs. Keep the four links as Layer 2 trunks; their STP operation does not change. This is the simplest routing extension and needs no external router.

> [!important] Gateway placement
> The example gives DSW1 two switch virtual interfaces (SVIs), one per VLAN. DSW2 remains the VLAN 20 STP root but is **not** a gateway in this simple extension. DSW1 is a single gateway failure point: if DSW1 fails, STP can restore a Layer 2 path but the PCs cannot route between VLANs. For gateway redundancy, study [[HSRP - Hot Standby Router Protocol]] as a separate next step.

### Configure DSW1 as the router

First check `show ip interface brief` on DSW1 and confirm VLAN 10/20 do not already have addresses that conflict with these examples. Then enter:

```cisco
enable
configure terminal
ip routing
interface Vlan10
 description VLAN10 default gateway
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface Vlan20
 description VLAN20 default gateway
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit
end
copy running-config startup-config
```

The VLANs already exist on DSW1 from section 4. Each SVI needs an active Layer 2 path for its VLAN; if an SVI stays `down/down`, check the VLAN, trunk, and STP state. Do **not** configure these same `.1` gateway addresses on DSW2.

### Set the PC default gateways

In **Desktop → IP Configuration**, keep each PC's existing IP address and subnet mask, and fill in only its gateway:

| PCs | VLAN | Default gateway |
|---|---:|---|
| PC0 and PC1 | 10 | `192.168.10.1` |
| PC2 and PC3 | 20 | `192.168.20.1` |

### Verify routing

On DSW1:

```cisco
show ip interface brief
show ip route
show spanning-tree vlan 10
show spanning-tree vlan 20
```

Both `Vlan10` and `Vlan20` should be `up/up`. The routing table should show connected routes for `192.168.10.0/24` and `192.168.20.0/24`. STP should still show DSW1 as VLAN 10 root and DSW2 as VLAN 20 root.

From PC0, test in this order:

```text
ping 192.168.10.1
ping 192.168.20.1
ping 192.168.20.10
ping 192.168.20.11
```

From PC2, run `ping 192.168.10.10`. The first attempts may need to resolve ARP. With SVIs up, correct PC gateways, and both VLANs carried over the trunks, these cross-VLAN pings should now succeed.

If routing fails, verify the PC IP/mask/gateway, DSW1 `show ip interface brief`, `show ip route`, both VLANs in `show interfaces trunk`, and any existing ACLs. The 2960 switches do not need IP addresses for this traffic.

## 9. Troubleshooting

| Symptom | Check | Likely correction |
|---|---|---|
| Wrong root for a VLAN | `show spanning-tree vlan 10` / `20` on all switches | Compare priorities and VLAN IDs; ensure all four switches have the VLAN and matching STP mode. |
| No VLAN 10 or 20 tree on a switch | `show vlan brief`, `show interfaces trunk` | Create the VLAN locally and allow it on both relevant trunks. |
| Trunk is down or access mode | `show interfaces trunk`, `show interfaces status`, `show running-config interface ...` | Check cable/port names, `switchport mode trunk`, and `no shutdown`. |
| PC cannot reach same-VLAN peer | PC IP/mask, `show vlan brief`, `show interfaces status` | Put host ports in the intended access VLAN and correct addresses. First ping may wait for ARP. |
| Cross-VLAN ping fails in the STP-only baseline | `show vlan brief`; inspect gateway field | Expected until section 8 is configured. |
| Cross-VLAN ping fails after section 8 | PC gateway/IP/mask, DSW1 `show ip interface brief`, `show ip route`, and trunks | Bring both SVIs up, enable `ip routing`, and use each VLAN's correct `.1` gateway. |
| One trunk says alternate or blocking | `show spanning-tree vlan 10` / `20` | This is normal loop prevention; check that another trunk forwards and failover works. |
| Host port becomes `err-disabled` | `show interfaces status`, `show logging` | Find the source of the unexpected BPDU and remove the switch from the PC port. After fixing it, use `shutdown` then `no shutdown` on that port. |
| Loop-like flooding or MAC flapping | `show spanning-tree`, trunk/VLAN consistency, cabling | Do not disable STP or put PortFast on inter-switch links; correct inconsistent trunk settings. |

## 10. Completion checklist

- [ ] Image and `STP.pkt` open from this note.
- [ ] Four trunk links match the actual cable endpoints and allow VLANs 10,20.
- [ ] VLAN 10 and 20 exist on all four switches.
- [ ] DSW1 is root for VLAN 10 and DSW2 is root for VLAN 20.
- [ ] PC-facing ports have the proper access VLAN, PortFast, and BPDU Guard.
- [ ] In the STP-only baseline, same-VLAN pings succeed and cross-VLAN ping fails as expected.
- [ ] A cross-switch same-VLAN ping succeeds before and after an active uplink failure.
- [ ] Temporary test changes are restored; switch configs and the `.pkt` file are saved.
- [ ] If section 8 is used, both DSW1 SVIs are up, PC gateways are set, and cross-VLAN pings succeed.

## Related notes and references

- [[Lab 20 - STP]] and [[Lab 21 - RSTP]]
- [[STP - Spanning Tree Protocol]]
- [Cisco Catalyst 2960 spanning-tree configuration guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/release/15-2_2_e/configuration/guide/b_1522e_2960_2960c_2960s_2960sf_2960p_cg/m_1522e_layer2_stp_2960_2960s_cg.html) — Rapid PVST+ mode, per-VLAN root selection, and verification.
- [Cisco PortFast and BPDU Guard guide](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10586-65.html) — protect ports connected to end devices.
- [Cisco Catalyst 3650 IP routing guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3650/software/release/16-3/configuration_guide/b_163_consolidated_3650_cg/b_163_consolidated_3650_cg_chapter_01010011.html) — SVIs and `ip routing` for inter-VLAN routing.

> [!info] Validation boundary
> The STP and inter-VLAN routing command plans were checked against the supplied screenshot and Cisco guidance. The saved configurations inside `STP.pkt` and the resulting Packet Tracer forwarding and routing behavior have not been executed or verified here; use the CLI checks and tests above for your actual simulation.
