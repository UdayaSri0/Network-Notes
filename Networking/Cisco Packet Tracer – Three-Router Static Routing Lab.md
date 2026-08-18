## 1. Objective

Configure the three-router network shown in Packet Tracer so that:

- VLAN/LAN 10 can communicate with VLAN/LAN 20.
    
- VLAN/LAN 10 can communicate with VLAN/LAN 30.
    
- VLAN/LAN 20 can communicate with VLAN/LAN 30.
    
- Routers use **Static Routing** rather than RIP, OSPF, or another dynamic routing protocol.
    
- End devices can successfully ping devices in the other networks.
    

---

# 2. Network Topology

The network contains three routers.

```
                    VLAN 20
                200.100.20.0/24
                       |
                     R1
                   /    \
                  /      \
                R2        R3
                |          |
             VLAN 10    VLAN 30
          200.100.10.0 200.100.30.0
```

### Router Roles

|Router|Connected LAN|LAN Gateway|
|---|---|---|
|Router1|VLAN 20|200.100.20.1|
|Router2|VLAN 10|200.100.10.1|
|Router3|VLAN 30|200.100.30.1|

---

# 3. LAN Addressing

For this lab, each LAN uses a `/24` subnet.

|   |   |   |   |   |
|---|---|---|---|---|
|Network|Network Address|Subnet Mask|Gateway|Example PC|
|VLAN 10|200.100.10.0/24|255.255.255.0|200.100.10.1|200.100.10.5|
|VLAN 20|200.100.20.0/24|255.255.255.0|200.100.20.1|200.100.20.5|
|VLAN 30|200.100.30.0/24|255.255.255.0|200.100.30.1|200.100.30.5|

---

# 4. WAN Addressing Between Routers

The diagram does not currently show IP addresses for the router-to-router links.

We will therefore use `/30` point-to-point networks.

## Router1 ↔ Router2

Network:

```
10.0.12.0/30
```

|   |   |   |
|---|---|---|
|Device|Interface|IP Address|
|Router1|GigabitEthernet0/0|10.0.12.1|
|Router2|GigabitEthernet0/0|10.0.12.2|

Subnet mask:

```
255.255.255.252
```

---

## Router1 ↔ Router3

Network:

```
10.0.13.0/30
```

|   |   |   |
|---|---|---|
|Device|Interface|IP Address|
|Router1|GigabitEthernet1/0|10.0.13.1|
|Router3|GigabitEthernet1/0|10.0.13.2|

Subnet mask:

```
255.255.255.252
```

---

# 5. Complete IP Addressing Table

|   |   |   |   |   |
|---|---|---|---|---|
|Device|Interface|IP Address|Subnet Mask|Purpose|
|Router1|Gi2/0|200.100.20.1|255.255.255.0|VLAN 20 Gateway|
|Router1|Gi0/0|10.0.12.1|255.255.255.252|Link to R2|
|Router1|Gi1/0|10.0.13.1|255.255.255.252|Link to R3|
|Router2|Gi2/0|200.100.10.1|255.255.255.0|VLAN 10 Gateway|
|Router2|Gi0/0|10.0.12.2|255.255.255.252|Link to R1|
|Router3|Gi2/0|200.100.30.1|255.255.255.0|VLAN 30 Gateway|
|Router3|Gi1/0|10.0.13.2|255.255.255.252|Link to R1|
|PC0|Fa0|200.100.10.5|255.255.255.0|VLAN 10 PC|
|PC1|Fa0|200.100.20.5|255.255.255.0|VLAN 20 PC|
|PC2|Fa0|200.100.30.5|255.255.255.0|VLAN 30 PC|

---

# 6. Configure Router1

Router1 connects:

- VLAN 20
    
- Router2
    
- Router3
    

Enter:

```
enable
configure terminal

hostname R1
```

## Configure VLAN 20 Interface

```
interface gigabitEthernet2/0
 ip address 200.100.20.1 255.255.255.0
 no shutdown
 exit
```

## Configure Link to Router2

```
interface gigabitEthernet0/0
 ip address 10.0.12.1 255.255.255.252
 no shutdown
 exit
```

## Configure Link to Router3

```
interface gigabitEthernet1/0
 ip address 10.0.13.1 255.255.255.252
 no shutdown
 exit
```

---

# 7. Router1 Static Routes

Router1 already knows these networks because they are directly connected:

```
200.100.20.0/24
10.0.12.0/30
10.0.13.0/30
```

However, Router1 does not know:

```
200.100.10.0/24
200.100.30.0/24
```

Therefore add:

```
ip route 200.100.10.0 255.255.255.0 10.0.12.2
ip route 200.100.30.0 255.255.255.0 10.0.13.2
```

Save:

```
end
copy running-config startup-config
```

---

# 8. Configure Router2

Router2 connects:

- VLAN 10
    
- Router1
    

```
enable
configure terminal

hostname R2
```

## Configure VLAN 10 Interface

```
interface gigabitEthernet2/0
 ip address 200.100.10.1 255.255.255.0
 no shutdown
 exit
```

## Configure Link to Router1

```
interface gigabitEthernet0/0
 ip address 10.0.12.2 255.255.255.252
 no shutdown
 exit
```

---

# 9. Router2 Static Routes

Router2 directly knows:

```
200.100.10.0/24
10.0.12.0/30
```

Router2 does not know:

```
200.100.20.0/24
200.100.30.0/24
```

Both networks can be reached through Router1.

Configure:

```
ip route 200.100.20.0 255.255.255.0 10.0.12.1
ip route 200.100.30.0 255.255.255.0 10.0.12.1
```

Save:

```
end
copy running-config startup-config
```

---

# 10. Configure Router3

Router3 connects:

- VLAN 30
    
- Router1
    

```
enable
configure terminal

hostname R3
```

## Configure VLAN 30 Interface

```
interface gigabitEthernet2/0
 ip address 200.100.30.1 255.255.255.0
 no shutdown
 exit
```

## Configure Link to Router1

```
interface gigabitEthernet1/0
 ip address 10.0.13.2 255.255.255.252
 no shutdown
 exit
```

---

# 11. Router3 Static Routes

Router3 directly knows:

```
200.100.30.0/24
10.0.13.0/30
```

Router3 does not know:

```
200.100.10.0/24
200.100.20.0/24
```

Both networks are reachable through Router1.

Configure:

```
ip route 200.100.10.0 255.255.255.0 10.0.13.1
ip route 200.100.20.0 255.255.255.0 10.0.13.1
```

Save:

```
end
copy running-config startup-config
```

---

# 12. Configure the PCs

## PC0 – VLAN 10

Go to:

**PC0 → Desktop → IP Configuration**

Configure:

```
IP Address:      200.100.10.5
Subnet Mask:     255.255.255.0
Default Gateway: 200.100.10.1
```

---

## PC1 – VLAN 20

Configure:

```
IP Address:      200.100.20.5
Subnet Mask:     255.255.255.0
Default Gateway: 200.100.20.1
```

---

## PC2 – VLAN 30

Configure:

```
IP Address:      200.100.30.5
Subnet Mask:     255.255.255.0
Default Gateway: 200.100.30.1
```

---

# 13. Static Routing Summary

## Router1

```
ip route 200.100.10.0 255.255.255.0 10.0.12.2
ip route 200.100.30.0 255.255.255.0 10.0.13.2
```

## Router2

```
ip route 200.100.20.0 255.255.255.0 10.0.12.1
ip route 200.100.30.0 255.255.255.0 10.0.12.1
```

## Router3

```
ip route 200.100.10.0 255.255.255.0 10.0.13.1
ip route 200.100.20.0 255.255.255.0 10.0.13.1
```

---

# 14. How Static Routing Works

Static routing uses the command:

```
ip route DESTINATION_NETWORK SUBNET_MASK NEXT_HOP
```

Example:

```
ip route 200.100.30.0 255.255.255.0 10.0.12.1
```

This means:

> If Router2 receives a packet intended for network `200.100.30.0/24`, send the packet to the next router at `10.0.12.1`.

In this network:

```
PC0
200.100.10.5
   |
   v
Router2
   |
   | 10.0.12.2
   |
   v
10.0.12.1
Router1
   |
   | 10.0.13.1
   |
   v
10.0.13.2
Router3
   |
   v
PC2
200.100.30.5
```

---

# 15. Verify Router Interfaces

On each router run:

```
show ip interface brief
```

Expected interfaces should show:

```
Status     Protocol
up         up
```

For example:

```
R1# show ip interface brief
```

You should see approximately:

```
Interface              IP-Address       Status    Protocol
GigabitEthernet0/0     10.0.12.1       up        up
GigabitEthernet1/0     10.0.13.1       up        up
GigabitEthernet2/0     200.100.20.1    up        up
```

If an interface shows:

```
administratively down
```

enter:

```
interface gigabitEthernetX/X
no shutdown
```

---

# 16. Verify the Routing Table

Use:

```
show ip route
```

## Router1

You should see routes similar to:

```
C 200.100.20.0/24 is directly connected
C 10.0.12.0/30 is directly connected
C 10.0.13.0/30 is directly connected

S 200.100.10.0/24 via 10.0.12.2
S 200.100.30.0/24 via 10.0.13.2
```

`C` means:

```
Connected
```

`S` means:

```
Static
```

---

# 17. Test Router-to-Router Connectivity

## From Router1

```
ping 10.0.12.2
ping 10.0.13.2
```

Both should succeed.

---

## From Router2

```
ping 10.0.12.1
```

---

## From Router3

```
ping 10.0.13.1
```

Do not continue troubleshooting the PCs until these router-to-router pings work.

---

# 18. Test Local Gateway Connectivity

## PC0

```
ping 200.100.10.1
```

## PC1

```
ping 200.100.20.1
```

## PC2

```
ping 200.100.30.1
```

All should succeed.

---

# 19. Test End-to-End Connectivity

## VLAN 10 → VLAN 20

From PC0:

```
ping 200.100.20.5
```

Expected:

```
Reply from 200.100.20.5
```

---

## VLAN 10 → VLAN 30

From PC0:

```
ping 200.100.30.5
```

---

## VLAN 20 → VLAN 30

From PC1:

```
ping 200.100.30.5
```

---

## VLAN 30 → VLAN 10

From PC2:

```
ping 200.100.10.5
```

---

# 20. Test the Path Using Traceroute

From PC0:

```
tracert 200.100.30.5
```

The expected path is approximately:

```
PC0
 ↓
200.100.10.1      Router2
 ↓
10.0.12.1         Router1
 ↓
10.0.13.2         Router3
 ↓
200.100.30.5      PC2
```

This is useful evidence that the static routing configuration is working correctly.

---

# 21. Troubleshooting Commands

Use these commands when the network does not work.

### Check interfaces

```
show ip interface brief
```

### Check routing table

```
show ip route
```

### Check configuration

```
show running-config
```

### Check a specific route

```
show ip route 200.100.30.0
```

### Test next-hop router

```
ping 10.0.12.1
```

### Check the path

```
traceroute 200.100.30.5
```

---

# 22. Common Problems

## Problem 1 – Interface is Down

Check:

```
show ip interface brief
```

Fix:

```
interface gigabitEthernet0/0
no shutdown
```

---

## Problem 2 – Incorrect Default Gateway

A PC must use the router interface in its own network.

Correct examples:

```
PC0 → 200.100.10.1
PC1 → 200.100.20.1
PC2 → 200.100.30.1
```

PC0 must **not** use Router1 or Router3 as its gateway.

---

## Problem 3 – Missing Static Route

If Router2 does not have:

```
ip route 200.100.30.0 255.255.255.0 10.0.12.1
```

it will not know where to send packets destined for VLAN 30.

---

## Problem 4 – Forward Route Exists but Return Route Does Not

Routing must work in **both directions**.

For example, PC0 might send traffic toward PC2 successfully, but Router3 must also know how to return traffic to:

```
200.100.10.0/24
```

Therefore Router3 needs:

```
ip route 200.100.10.0 255.255.255.0 10.0.13.1
```

---

# 23. Alternative: Default Routes on Edge Routers

Because Router2 and Router3 each have only one way to reach other networks, their multiple static routes could be replaced with a **default route**.

## Router2

Instead of:

```
ip route 200.100.20.0 255.255.255.0 10.0.12.1
ip route 200.100.30.0 255.255.255.0 10.0.12.1
```

we could use:

```
ip route 0.0.0.0 0.0.0.0 10.0.12.1
```

Meaning:

> Send any network that Router2 does not already know about to Router1.

## Router3

```
ip route 0.0.0.0 0.0.0.0 10.0.13.1
```

Router1 would still require:

```
ip route 200.100.10.0 255.255.255.0 10.0.12.2
ip route 200.100.30.0 255.255.255.0 10.0.13.2
```

For teaching **basic static routing**, I recommend configuring the individual routes first because students can clearly see how each destination is reached.

---

# 24. Final Complete Configuration

## R1

```
enable
configure terminal

hostname R1

interface gigabitEthernet2/0
 ip address 200.100.20.1 255.255.255.0
 no shutdown
 exit

interface gigabitEthernet0/0
 ip address 10.0.12.1 255.255.255.252
 no shutdown
 exit

interface gigabitEthernet1/0
 ip address 10.0.13.1 255.255.255.252
 no shutdown
 exit

ip route 200.100.10.0 255.255.255.0 10.0.12.2
ip route 200.100.30.0 255.255.255.0 10.0.13.2

end
copy running-config startup-config
```

---

## R2

```
enable
configure terminal

hostname R2

interface gigabitEthernet2/0
 ip address 200.100.10.1 255.255.255.0
 no shutdown
 exit

interface gigabitEthernet0/0
 ip address 10.0.12.2 255.255.255.252
 no shutdown
 exit

ip route 200.100.20.0 255.255.255.0 10.0.12.1
ip route 200.100.30.0 255.255.255.0 10.0.12.1

end
copy running-config startup-config
```

---

## R3

```
enable
configure terminal

hostname R3

interface gigabitEthernet2/0
 ip address 200.100.30.1 255.255.255.0
 no shutdown
 exit

interface gigabitEthernet1/0
 ip address 10.0.13.2 255.255.255.252
 no shutdown
 exit

ip route 200.100.10.0 255.255.255.0 10.0.13.1
ip route 200.100.20.0 255.255.255.0 10.0.13.1

end
copy running-config startup-config
```

---

# 25. Quick Teaching Explanation

A simple way to explain static routing to students is:

> **A router automatically knows only the networks directly connected to it. If the destination is behind another router, we must tell the router where to send the packet.**

The syntax is:

```
ip route [destination network] [subnet mask] [next-hop IP]
```

For example:

```
ip route 200.100.30.0 255.255.255.0 10.0.12.1
```

can be read as:

> “To reach the `200.100.30.0` network, send the packet to router `10.0.12.1`.”

---

# 26. Verification Checklist

- All router LAN interfaces have the correct IP addresses.
    
- All WAN interfaces have `/30` addresses.
    
- All router interfaces are `up/up`.
    
- PC0 uses gateway `200.100.10.1`.
    
- PC1 uses gateway `200.100.20.1`.
    
- PC2 uses gateway `200.100.30.1`.
    
- R1 can ping R2.
    
- R1 can ping R3.
    
- Static routes appear with `S` in `show ip route`.
    
- PC0 can ping PC1.
    
- PC0 can ping PC2.
    
- PC1 can ping PC2.
    
- `tracert` shows traffic crossing the expected routers.
    
- Running configuration has been saved.