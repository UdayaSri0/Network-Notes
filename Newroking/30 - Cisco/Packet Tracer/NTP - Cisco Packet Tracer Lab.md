---
title: Configure NTP in Cisco Packet Tracer
aliases:
  - Cisco Packet Tracer NTP Configuration
  - Packet Tracer NTP Lab
type: lab
status: complete
area: Networking
vendor: Cisco
platform: Cisco Packet Tracer
protocol: NTP
difficulty: beginner
keywords:
  - Cisco IOS
  - Cisco Packet Tracer
  - NTP configuration
  - time synchronization
  - UDP 123
  - NTP server
tags:
  - networking/ntp
  - cisco/packet-tracer
  - lab
created: 2026-08-11
updated: 2026-08-11
prerequisites:
  - "[[NTP - Overview]]"
related:
  - "[[Network Monitoring]]"
  - "[[Syslog - Cisco Packet Tracer Lab]]"
---

# Configure NTP in Cisco Packet Tracer

> [!abstract]
> Configure a Packet Tracer server as an NTP time source and synchronize a Cisco router to it using UDP port 123.

> [!note] Packet Tracer limitation
> Packet Tracer simulates a subset of NTP and Cisco IOS. Synchronization output and available commands can vary by device model and version.

## 1. Learning objectives

After this lab, you should be able to:

- Explain the NTP client-server relationship.
- Enable the NTP service on a Packet Tracer server.
- Configure a Cisco router to use an NTP server.
- Verify the NTP association and synchronization state.
- Explain why [[Syslog - Overview|Syslog]] depends on accurate time.

## 2. Prerequisites

- Basic Cisco IOS CLI navigation.
- Basic IPv4 addressing and ping testing.
- Familiarity with [[NTP - Overview|NTP fundamentals]].

## 3. Topology

```text
             Copper straight-through cable
    FastEthernet0                 GigabitEthernet0/0
+------------------+             +------------------+
| Server0          |-------------| Router0          |
| NTP Server       |             | NTP Client       |
| 192.168.1.10/24  |             | 192.168.1.1/24   |
+------------------+             +------------------+

                    NTP uses UDP 123
```

### Addressing table

| Device | Interface | IPv4 address | Subnet mask | Default gateway |
|---|---|---|---|---|
| `Router0` | `G0/0` | `192.168.1.1` | `255.255.255.0` | N/A |
| `Server0` | `FastEthernet0` | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` |

## 4. Build the topology

1. Add one Cisco router and one **Server-PT** device.
2. Connect `Server0 FastEthernet0` to `Router0 GigabitEthernet0/0`.
3. Use a **copper straight-through** cable.

> [!tip]
> Some router models use `FastEthernet0/0`. Run `show ip interface brief` and substitute the interface name shown by your router.

## 5. Configure Server0 addressing

Open **Server0 > Desktop > IP Configuration**, then enter:

| Setting | Value |
|---|---|
| IP address | `192.168.1.10` |
| Subnet mask | `255.255.255.0` |
| Default gateway | `192.168.1.1` |

## 6. Enable the NTP service

1. Open **Server0 > Services > NTP**.
2. Set the NTP service to **On**.
3. If date and time controls are available, set a recognizable test time.
4. Leave authentication disabled for this introductory lab.

> [!info]
> NTP distributes a common reference time. The client can display that time in a configured local timezone.

## 7. Configure Router0 addressing

Open **Router0 > CLI**, then enter:

```cisco
enable
configure terminal
hostname Router0

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit
end
```

Verify the interface:

```cisco
show ip interface brief
```

The connected interface should eventually show `up/up`.

## 8. Test IP connectivity

From **Router0 > CLI**, run:

```cisco
ping 192.168.1.10
```

Do not configure NTP until the ping succeeds.

> [!tip]
> The first ping can fail while ARP resolves Server0's MAC address. Repeat it before troubleshooting further.

## 9. Configure the NTP client

```cisco
configure terminal
ntp server 192.168.1.10
end
```

### Optional: configure Sri Lanka Standard Time

NTP synchronizes a common time reference. This command changes how Router0 displays local time:

```cisco
configure terminal
clock timezone SLST 5 30
end
```

For another location, replace `SLST 5 30` with the required timezone name and UTC offset.

## 10. Wait for synchronization

NTP synchronization is not always immediate.

1. Allow Packet Tracer simulation time to run.
2. Use the **Fast Forward Time** control if necessary.
3. Recheck the status after several simulated polling intervals.

```text
Configured association --> packets exchanged --> clock selected --> synchronized
```

## 11. Verify NTP

### Check the clock

```cisco
show clock
show clock detail
```

### Check the association

```cisco
show ntp associations
```

An asterisk (`*`) beside `192.168.1.10` normally indicates that the server is the selected synchronization source.

### Check synchronization status

```cisco
show ntp status
```

Look for information similar to:

```text
Clock is synchronized
reference is 192.168.1.10
```

> [!note]
> Packet Tracer may show simplified output. The association, clock, and server reachability together provide the best verification.

## 12. Save the configuration

```cisco
copy running-config startup-config
```

Press **Enter** to accept the default destination filename.

## 13. Troubleshooting

### Router cannot ping Server0

- [ ] Confirm both addresses are in `192.168.1.0/24`.
- [ ] Confirm the router interface is `up/up`.
- [ ] Check the cable and actual router interface name.
- [ ] Confirm Server0 has gateway `192.168.1.1`.

### Association remains unsynchronized

- [ ] Confirm **Server0 > Services > NTP** is **On**.
- [ ] Confirm `ntp server 192.168.1.10` appears in the running configuration.
- [ ] Allow more simulation time or use **Fast Forward Time**.
- [ ] Confirm the server is reachable with ping.
- [ ] Check whether the selected Packet Tracer router supports NTP.

### Router reports stratum 16

Stratum `16` means the router is not synchronized. Check reachability, the NTP service, and the configured server address.

### NTP command is unavailable

Use Cisco IOS contextual help:

```cisco
ntp ?
show ntp ?
```

If the commands are missing, try another Cisco router model in Packet Tracer.

## 14. Complete Router0 configuration

```cisco
enable
configure terminal
hostname Router0

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit

clock timezone SLST 5 30
ntp server 192.168.1.10

end
copy running-config startup-config
```

## 15. Completion checklist

- [ ] Server0 NTP service is on.
- [ ] Router0 can ping `192.168.1.10`.
- [ ] `show ntp associations` lists `192.168.1.10`.
- [ ] Router0 reports a synchronized clock.
- [ ] The running configuration is saved.

## 16. Key takeaways

- NTP normally uses UDP port `123`.
- The server supplies time; the router is the NTP client.
- Synchronization can require several polling intervals.
- A stratum value of `16` indicates an unsynchronized device.
- Accurate NTP time makes Syslog event correlation reliable.

---

**Parent:** [[NTP - Overview|NTP Overview]]  
**Next:** [[Syslog - Cisco Packet Tracer Lab|Configure Syslog in Cisco Packet Tracer]]  
**Home:** [[Network Notes Home]]
