---
title: Configure Syslog in Cisco Packet Tracer
aliases:
  - Cisco Packet Tracer Syslog Configuration
  - Packet Tracer Syslog Lab
type: lab
status: complete
area: Networking
vendor: Cisco
platform: Cisco Packet Tracer
protocol: Syslog
difficulty: beginner
keywords:
  - Cisco IOS
  - Cisco Packet Tracer
  - Syslog configuration
  - logging server
  - severity levels
  - UDP 514
  - event monitoring
tags:
  - networking/syslog
  - cisco/packet-tracer
  - lab
created: 2026-08-11
updated: 2026-08-11
prerequisites:
  - "[[Syslog]]"
related:
  - "[[Network Monitoring]]"
  - "[[NTP - Network Time Protocol]]"
  - "[[Lab 13 - NTP Server]]"
category: "Packet Tracer Labs"
packet_tracer_supported: "Yes"
related_protocols: []
---

# Configure Syslog in Cisco Packet Tracer

> [!abstract]
> Configure a Cisco router to timestamp event messages and send informational-and-higher Syslog events to a Packet Tracer server.

> [!note] Packet Tracer limitation
> Packet Tracer provides a simplified Syslog service. Physical Cisco IOS devices and production log collectors offer additional transport, filtering, storage, and security features.

## 1. Learning objectives

After this lab, you should be able to:

- Enable the Packet Tracer Syslog service.
- Configure a Cisco router with a remote logging destination.
- Select an appropriate severity threshold.
- Generate and verify interface event messages.
- Explain why synchronized timestamps are important.

## 2. Prerequisites

- Basic Cisco IOS CLI navigation.
- Basic IPv4 addressing and ping testing.
- Familiarity with [[Syslog|Syslog severity levels]].
- Recommended: complete [[Lab 13 - NTP Server|the NTP lab]] first.

## 3. Topology

```text
             Copper straight-through cable
    FastEthernet0                 GigabitEthernet0/0
+------------------+             +------------------+
| Server0          |-------------| Router0          |
| Syslog Server    |             | Log Source       |
| 192.168.1.10/24  |             | 192.168.1.1/24   |
+------------------+             +------------------+

              Syslog commonly uses UDP 514
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

## 6. Enable the Syslog service

1. Open **Server0 > Services > SYSLOG**.
2. Set the service to **On**.
3. Leave the Syslog message table open when testing, or return to it later.

The table will display messages received from configured devices.

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

Do not configure remote logging until the ping succeeds.

## 9. Configure timestamps and remote logging

```cisco
configure terminal
service timestamps log datetime msec
logging on
logging 192.168.1.10
logging trap informational
end
```

### Command explanation

| Command | Purpose |
|---|---|
| `service timestamps log datetime msec` | Add date, time, and milliseconds to log messages |
| `logging on` | Enable the IOS logging process |
| `logging 192.168.1.10` | Set Server0 as the remote Syslog destination |
| `logging trap informational` | Send severity levels `0` through `6` |

> [!important] Severity behavior
> `informational` includes emergencies, alerts, critical, errors, warnings, notifications, and informational events. It excludes only debugging messages at level `7`.

### Optional local buffer

If supported by the simulated IOS, retain recent messages in router memory:

```cisco
configure terminal
logging buffered 4096 informational
end
```

The local buffer is useful for comparison with messages received by Server0.

## 10. Generate test events safely

Create a loopback interface so the test does not disconnect the link to Server0:

```cisco
configure terminal
interface loopback 0
 description SYSLOG-TEST
 ip address 10.0.0.1 255.255.255.255
 shutdown
 no shutdown
end
```

This should generate messages similar to:

```text
%LINK-5-CHANGED: Interface Loopback0, changed state to administratively down
%LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback0, changed state to down
%LINK-5-CHANGED: Interface Loopback0, changed state to up
%LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback0, changed state to up
```

The exact wording and number of messages can vary.

## 11. Verify on Server0

Open **Server0 > Services > SYSLOG** and confirm the message table contains events from Router0.

Check for:

- Source address `192.168.1.1`.
- `LINK` or `LINEPROTO` messages.
- Severity `5` notification events.
- Timestamps on the received messages.

## 12. Verify on Router0

```cisco
show logging
show running-config | include logging
show running-config | include service timestamps
```

`show logging` should identify `192.168.1.10` as a logging host. If local buffering is configured, it should also show recent interface events.

## 13. Improve timestamp accuracy with NTP

Manually set clocks can drift. For dependable timestamps, configure Router0 with [[Lab 13 - NTP Server|the NTP Packet Tracer lab]].

```text
NTP Server ---> correct time ---> Router0 ---> timestamped events ---> Syslog Server
```

After NTP is synchronized, generate another loopback event and compare the timestamp on Server0.

## 14. Save the configuration

```cisco
copy running-config startup-config
```

Press **Enter** to accept the default destination filename.

## 15. Troubleshooting

### No messages appear on Server0

- [ ] Confirm Router0 can ping `192.168.1.10`.
- [ ] Confirm **Server0 > Services > SYSLOG** is **On**.
- [ ] Confirm `logging 192.168.1.10` is in the running configuration.
- [ ] Confirm the trap level includes the generated event.
- [ ] Generate a fresh event after remote logging is configured.
- [ ] Check the actual source address with `show logging`.

### Link messages do not appear

Link-state messages commonly use severity `5`. Ensure the threshold is `notifications`, `informational`, or `debugging`. This lab uses:

```cisco
logging trap informational
```

### Timestamps are incorrect

`service timestamps` adds a timestamp but does not synchronize the router clock. Complete the [[Lab 13 - NTP Server|NTP lab]] and verify `show ntp status`.

### Logging command is unavailable

Use contextual help:

```cisco
logging ?
show logging ?
```

If required commands are missing, try another Cisco router model.

## 16. Complete Router0 configuration

```cisco
enable
configure terminal
hostname Router0

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit

service timestamps log datetime msec
logging on
logging 192.168.1.10
logging trap informational
logging buffered 4096 informational

interface loopback 0
 description SYSLOG-TEST
 ip address 10.0.0.1 255.255.255.255
 no shutdown
exit

end
copy running-config startup-config
```

## 17. Completion checklist

- [ ] Server0 Syslog service is on.
- [ ] Router0 can ping `192.168.1.10`.
- [ ] Router0 lists Server0 as a logging host.
- [ ] Server0 receives a Loopback0 event.
- [ ] Messages contain timestamps.
- [ ] The running configuration is saved.

## 18. Key takeaways

- Traditional Syslog commonly uses UDP port `514`.
- A lower numeric severity represents a more serious event.
- A configured threshold includes that level and all more severe levels.
- Central logging preserves and correlates messages from multiple devices.
- NTP synchronization is necessary for trustworthy log timestamps.

---

**Parent:** [[Syslog|Syslog Overview]]  
**Previous:** [[Lab 13 - NTP Server|Configure NTP in Cisco Packet Tracer]]  
**Home:** [[Networking Dashboard]]
