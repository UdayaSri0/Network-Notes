from pathlib import Path


VAULT = Path(__file__).resolve().parents[1] / "Newroking"
ROOT = VAULT / "05 - Step-by-Step Configurations"

CATEGORIES = {
    "01": "Device Foundations",
    "02": "Switching and Inter-VLAN Routing",
    "03": "Routing Protocols",
    "04": "Network Services",
    "05": "Security",
    "06": "High Availability",
    "07": "Monitoring and Management",
    "08": "WAN, VPN, and Wireless",
    "09": "Internet Protocol Version 6 (IPv6)",
    "10": "Integrated Enterprise Configuration",
}

TOPICS = []


def add(number, category, title, short, difficulty, support, objective, topology,
        connections, addressing, configs, verify, tests, troubleshoot,
        gui_steps=None, notes=None):
    TOPICS.append({
        "number": number,
        "category": category,
        "title": title,
        "short": short,
        "difficulty": difficulty,
        "support": support,
        "objective": objective,
        "topology": topology,
        "connections": connections,
        "addressing": addressing,
        "configs": configs,
        "verify": verify,
        "tests": tests,
        "troubleshoot": troubleshoot,
        "gui_steps": gui_steps or [],
        "notes": notes or [],
    })


def rows(items):
    return "\n".join("| " + " | ".join(item) + " |" for item in items)


def code_block(label, code):
    return f"### {label}\n\n```cisco\n{code.strip()}\n```"


def category_guide_title(name):
    return f"{name} Guide" if name.endswith("Configuration") else f"{name} Configuration Guide"


def render_note(topic):
    filename = f"{topic['number']} - {topic['title']} - Step by Step"
    related = [f"[[{other['number']} - {other['title']} - Step by Step]]"
               for other in TOPICS
               if other["category"] == topic["category"] and other is not topic][:4]
    related_yaml = "\n".join(f'  - "{link}"' for link in related) or "  - none"
    guide_alias = (f"{topic['short']} guide" if "configuration" in topic["short"].lower()
                   else f"{topic['short']} configuration guide")
    aliases = [topic["short"], guide_alias]
    alias_yaml = "\n".join(f'  - "{alias}"' for alias in aliases)
    connection_rows = rows(topic["connections"])
    address_rows = rows(topic["addressing"])
    config_sections = []
    step_sections = []
    step_number = 4
    for device, config in topic["configs"]:
        config_sections.append(code_block(device, config))
        step_sections.append(
            f"### Step {step_number} — Configure {device}\n\n"
            f"Open **{device} → CLI**, press Enter, and enter the following commands exactly.\n\n"
            f"```cisco\n{config.strip()}\n```"
        )
        step_number += 1
    gui_sections = []
    for heading, instructions in topic["gui_steps"]:
        gui_sections.append(f"### Step {step_number} — {heading}\n\n{instructions}")
        step_number += 1
    verify_lines = "\n".join(f"- `{command}`" for command in topic["verify"])
    test_rows = rows(topic["tests"])
    trouble_rows = rows(topic["troubleshoot"])
    note_callouts = "\n\n".join(f"> [!note] Teaching note\n> {note}" for note in topic["notes"])
    related_lines = "\n".join(f"- {link}" for link in related) or "- [[Configuration Library Dashboard]]"
    return f'''---
title: "{filename}"
aliases:
{alias_yaml}
category: "Step-by-Step Configuration/{CATEGORIES[topic['category']]}"
difficulty: "{topic['difficulty']}"
packet_tracer_supported: "{topic['support']}"
related_protocols:
{related_yaml}
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - step-by-step
---

# {filename}

> [!info] Outcome
> {topic['objective']}

> [!warning] Interface-name check
> The examples use Cisco 2911/1941 router interfaces such as `GigabitEthernet0/0` and Cisco 2960 switch ports such as `FastEthernet0/1`. Check the labels on your Packet Tracer device and substitute the actual interface name when it differs.

## 1. Packet Tracer Support

**{topic['support']}**

## 2. Example Topology

```mermaid
{topic['topology']}
```

### Devices and Cabling

| From | To | Cable / Link |
|---|---|---|
{connection_rows}

## 3. Addressing Plan

| Device | Interface | Address / Setting | Default Gateway |
|---|---|---|---|
{address_rows}

## 4. Before You Configure

1. Place and rename every device exactly as shown.
2. Connect the interfaces in the cabling table.
3. Wait for links to become active before troubleshooting Layer 3.
4. Erase or inspect old lab configuration so it does not conflict with this example.

## 5. Step-by-Step Configuration

### Step 1 — Build the topology

Place the listed devices, rename them, and make each connection shown above.

### Step 2 — Confirm the addressing plan

Check that every address is unique, belongs to the stated subnet, and uses the correct mask or prefix length.

### Step 3 — Open each device

For IOS devices, select **CLI** and press Enter. For PCs and servers, use the named Packet Tracer desktop or services panel.

{chr(10).join(step_sections)}

{chr(10).join(gui_sections)}

## 6. Complete Device Configurations

Use these blocks when rebuilding the example from an empty Packet Tracer file. Each block belongs only to the device named above it.

{chr(10).join(config_sections)}

## 7. Key Configuration Logic

- Configure physical or logical interfaces before depending on a protocol that uses them.
- Use `no shutdown` on routed interfaces and switched virtual interfaces when required.
- Keep VLAN IDs, IP networks, masks, wildcard masks, and default gateways consistent with the addressing table.
- Save the configuration only after verification succeeds.

{note_callouts}

## 8. Verification Commands

Run the commands relevant to the device and compare the result with the addressing and topology tables.

{verify_lines}

## 9. Testing Matrix

| Test | Source | Destination / Check | Expected Result |
|---|---|---|---|
{test_rows}

## 10. Troubleshooting

| Symptom | Likely Cause | Check or Fix |
|---|---|---|
{trouble_rows}

## 11. Save and Finish

On every IOS device whose tests pass:

```cisco
copy running-config startup-config
```

Then save the Packet Tracer activity file with a descriptive version number.

## 12. Related Configuration Notes

{related_lines}

Return to [[Configuration Library Dashboard]].
'''


add(
    "01", "01", "Cisco Router Basic Configuration", "Router basic configuration",
    "Beginner", "Yes",
    "Configure a router hostname, secure local access, IPv4 interfaces, Secure Shell (SSH), and saved startup configuration.",
    'flowchart LR\n    PC1["PC1"] --- SW1["SW1"] --- R1["R1"]',
    [("PC1 FastEthernet0", "SW1 FastEthernet0/1", "Copper straight-through"),
     ("SW1 GigabitEthernet0/1", "R1 GigabitEthernet0/0", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1")],
    [("R1", '''enable
configure terminal
hostname R1
no ip domain-lookup
enable secret ClassEnable!23
service password-encryption
banner motd #Authorised users only#
username admin privilege 15 secret AdminSSH!23
ip domain-name campus.lab
interface gigabitEthernet0/0
 description LAN_TO_SW1
 ip address 192.168.10.1 255.255.255.0
 no shutdown
 exit
crypto key generate rsa modulus 1024
ip ssh version 2
line console 0
 password Console!23
 login
 logging synchronous
 exec-timeout 10 0
 exit
line vty 0 4
 login local
 transport input ssh
 exec-timeout 10 0
end
copy running-config startup-config''')],
    ["show ip interface brief", "show running-config", "show ip ssh", "show users"],
    [("Gateway ping", "PC1", "192.168.10.1", "Success"),
     ("SSH login", "PC1", "ssh -l admin 192.168.10.1", "Password prompt and R1 CLI")],
    [("G0/0 is administratively down", "Missing no shutdown", "Enter interface mode and use no shutdown"),
     ("SSH fails", "Hostname, domain name, key, or VTY login missing", "Check show ip ssh and the VTY configuration")],
    gui_steps=[("Configure PC1", "Open **PC1 → Desktop → IP Configuration**. Enter IP `192.168.10.10`, mask `255.255.255.0`, and gateway `192.168.10.1`.")],
    notes=["Packet Tracer may offer only a 1024-bit RSA key on some router images. Use 2048 bits on modern real equipment when supported."]
)

add(
    "02", "01", "Cisco Switch Basic Configuration", "Switch basic configuration",
    "Beginner", "Yes",
    "Configure a Layer 2 switch hostname, management switched virtual interface (SVI), default gateway, console security, and SSH access.",
    'flowchart LR\n    PC1["Admin PC"] --- SW1["SW1"] --- R1["Gateway R1"]',
    [("Admin PC", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through")],
    [("R1", "G0/0", "192.168.99.1 /24", "—"),
     ("SW1", "VLAN 99", "192.168.99.2 /24", "192.168.99.1"),
     ("Admin PC", "FastEthernet0", "192.168.99.10 /24", "192.168.99.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.99.1 255.255.255.0
 no shutdown
end
copy running-config startup-config'''),
     ("SW1", '''enable
configure terminal
hostname SW1
no ip domain-lookup
enable secret ClassEnable!23
service password-encryption
vlan 99
 name MANAGEMENT
exit
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 no shutdown
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 99
 spanning-tree portfast
exit
interface gigabitEthernet0/1
 switchport mode access
 switchport access vlan 99
exit
ip default-gateway 192.168.99.1
username admin privilege 15 secret AdminSSH!23
ip domain-name campus.lab
crypto key generate rsa modulus 1024
ip ssh version 2
line console 0
 password Console!23
 login
 logging synchronous
exit
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config''')],
    ["show ip interface brief", "show vlan brief", "show interfaces status", "show ip ssh"],
    [("Management ping", "Admin PC", "192.168.99.2", "Success"),
     ("Gateway ping", "SW1", "192.168.99.1", "Success")],
    [("VLAN 99 SVI is down", "No active port belongs to VLAN 99", "Bring up an access or trunk port carrying VLAN 99"),
     ("Remote subnet cannot reach SW1", "Missing ip default-gateway", "Configure 192.168.99.1 as the Layer 2 switch gateway")],
    gui_steps=[("Configure the Admin PC", "Set `192.168.99.10/24` with default gateway `192.168.99.1` in **Desktop → IP Configuration**.")]
)

add(
    "03", "01", "Cisco Multilayer Switch Basic Configuration", "Multilayer switch configuration",
    "Intermediate", "Yes",
    "Enable Layer 3 routing on a multilayer switch and configure both switched virtual interfaces and a routed uplink.",
    'flowchart LR\n    PC10["PC VLAN 10"] --- MLS1["MLS1"] --- R1["R1"]',
    [("PC10", "MLS1 F0/1", "Copper straight-through"),
     ("MLS1 G0/1", "R1 G0/0", "Copper straight-through routed link")],
    [("MLS1", "VLAN 10", "192.168.10.1 /24", "—"),
     ("MLS1", "G0/1", "10.0.0.1 /30", "—"),
     ("R1", "G0/0", "10.0.0.2 /30", "—"),
     ("PC10", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1")],
    [("MLS1", '''enable
configure terminal
hostname MLS1
ip routing
vlan 10
 name USERS
exit
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
exit
interface gigabitEthernet0/1
 no switchport
 description ROUTED_LINK_TO_R1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 10.0.0.2
end
copy running-config startup-config'''),
     ("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.0.1
end
copy running-config startup-config''')],
    ["show ip interface brief", "show interfaces switchport", "show ip route", "show vlan brief"],
    [("VLAN gateway", "PC10", "192.168.10.1", "Success"),
     ("Routed uplink", "MLS1", "10.0.0.2", "Success")],
    [("IP address rejected on G0/1", "Port is still Layer 2", "Enter no switchport before the IP address"),
     ("SVI networks do not route", "ip routing is missing", "Enable ip routing globally")],
    gui_steps=[("Configure PC10", "Set `192.168.10.10/24` and gateway `192.168.10.1`.")]
)

add(
    "04", "01", "TFTP - Trivial File Transfer Protocol Backup and Restore", "TFTP backup and restore",
    "Beginner", "Yes",
    "Back up a router running configuration to a Packet Tracer TFTP server and restore it safely.",
    'flowchart LR\n    R1["R1 192.168.50.1"] --- SW1["SW1"] --- S1["TFTP Server 192.168.50.10"]',
    [("R1 G0/0", "SW1 G0/1", "Copper straight-through"),
     ("Server FastEthernet0", "SW1 F0/1", "Copper straight-through")],
    [("R1", "G0/0", "192.168.50.1 /24", "—"),
     ("TFTP Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1")],
    [("R1 — Prepare and Back Up", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
end
ping 192.168.50.10
copy running-config startup-config
copy running-config tftp:
192.168.50.10
R1-running-config'''),
     ("R1 — Restore", '''enable
copy tftp: running-config
192.168.50.10
R1-running-config
show running-config
copy running-config startup-config''')],
    ["show running-config", "show startup-config", "dir flash:", "ping 192.168.50.10"],
    [("Reachability", "R1", "192.168.50.10", "Success before copying"),
     ("Backup file", "TFTP Server", "R1-running-config", "File appears in TFTP services")],
    [("Timed out", "No IP reachability or TFTP service disabled", "Ping the server and enable Services → TFTP"),
     ("Wrong configuration merged", "Restored directly into running-config", "Inspect the file first and use a controlled maintenance window")],
    gui_steps=[("Configure the TFTP server", "Open **Server → Desktop → IP Configuration** and set `192.168.50.10/24`, gateway `192.168.50.1`. Then open **Services → TFTP** and switch the service **On**.")],
    notes=["Copying to running-config merges commands. For a clean replacement, validate the file and use an appropriate reload/startup-config workflow on real equipment."]
)

add(
    "05", "02", "VLAN - Virtual Local Area Network Configuration", "VLAN configuration",
    "Beginner", "Yes",
    "Create three Virtual Local Area Networks (VLANs), assign access ports, and prove that each VLAN forms a separate Layer 2 broadcast domain.",
    'flowchart LR\n    PC10["PC10 VLAN 10"] --- SW1["SW1"] --- PC20["PC20 VLAN 20"]\n    PC30["PC30 VLAN 30"] --- SW1',
    [("PC10", "SW1 F0/1", "Copper straight-through"),
     ("PC20", "SW1 F0/2", "Copper straight-through"),
     ("PC30", "SW1 F0/3", "Copper straight-through")],
    [("PC10", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC20", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1"),
     ("PC30", "FastEthernet0", "192.168.30.10 /24", "192.168.30.1")],
    [("SW1", '''enable
configure terminal
hostname SW1
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
exit
interface fastEthernet0/1
 description PC10_ADMIN
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
exit
interface fastEthernet0/2
 description PC20_STAFF
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
exit
interface fastEthernet0/3
 description PC30_STUDENTS
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
end
copy running-config startup-config''')],
    ["show vlan brief", "show interfaces fastEthernet0/1 switchport", "show mac address-table dynamic"],
    [("VLAN membership", "SW1", "show vlan brief", "F0/1, F0/2, and F0/3 appear in VLANs 10, 20, and 30"),
     ("Isolation", "PC10", "192.168.20.10", "Fails until inter-VLAN routing exists")],
    [("Port remains in VLAN 1", "Access VLAN command missing or wrong interface", "Re-enter switchport access vlan on the connected port"),
     ("Same-VLAN hosts cannot ping", "Incorrect PC subnet or port down", "Check IP settings, cable, and show interfaces status")],
    gui_steps=[("Configure the PCs", "Set each PC address from the table. The gateways are reserved for a later inter-VLAN routing guide.")]
)

add(
    "06", "02", "IEEE 802.1Q Trunk Configuration", "802.1Q trunk configuration",
    "Beginner", "Yes",
    "Carry VLANs 10, 20, 30, and 99 between two switches over a statically configured IEEE 802.1Q trunk.",
    'flowchart LR\n    PC1["PC1 VLAN 10"] --- SW1["SW1"] ==>|"802.1Q trunk"| SW2["SW2"] --- PC2["PC2 VLAN 10"]',
    [("PC1", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "SW2 G0/1", "Copper crossover or Automatic"),
     ("SW2 F0/1", "PC2", "Copper straight-through")],
    [("PC1", "FastEthernet0", "192.168.10.10 /24", "—"),
     ("PC2", "FastEthernet0", "192.168.10.20 /24", "—"),
     ("Native VLAN", "VLAN 99", "No host address required", "—")],
    [("SW1", '''enable
configure terminal
hostname SW1
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 99
 name NATIVE_MANAGEMENT
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
exit
interface gigabitEthernet0/1
 description TRUNK_TO_SW2
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99
end
copy running-config startup-config'''),
     ("SW2", '''enable
configure terminal
hostname SW2
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 99
 name NATIVE_MANAGEMENT
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
exit
interface gigabitEthernet0/1
 description TRUNK_TO_SW1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99
end
copy running-config startup-config''')],
    ["show interfaces trunk", "show interfaces gigabitEthernet0/1 switchport", "show vlan brief"],
    [("Same VLAN across trunk", "PC1", "192.168.10.20", "Success"),
     ("Allowed VLAN list", "SW1 and SW2", "show interfaces trunk", "10,20,30,99")],
    [("Trunk not listed", "One side is access mode or link is down", "Set switchport mode trunk on both ends"),
     ("Native VLAN mismatch", "Different native VLAN on each switch", "Configure VLAN 99 on both trunk endpoints")],
    gui_steps=[("Configure PC addresses", "Set PC1 to `192.168.10.10/24` and PC2 to `192.168.10.20/24`. A gateway is unnecessary for the same-subnet test.")]
)

add(
    "07", "02", "Router-on-a-Stick Inter-VLAN Routing", "Router-on-a-stick configuration",
    "Intermediate", "Yes",
    "Route traffic among VLANs 10, 20, and 30 by using one router interface with IEEE 802.1Q subinterfaces.",
    'flowchart LR\n    PC10["PC10 VLAN 10"] --- SW1["SW1"] ==>|"802.1Q trunk"| R1["R1 subinterfaces"]\n    PC20["PC20 VLAN 20"] --- SW1\n    PC30["PC30 VLAN 30"] --- SW1',
    [("PC10", "SW1 F0/1", "Copper straight-through"),
     ("PC20", "SW1 F0/2", "Copper straight-through"),
     ("PC30", "SW1 F0/3", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through trunk")],
    [("R1", "G0/0.10", "192.168.10.1 /24", "—"),
     ("R1", "G0/0.20", "192.168.20.1 /24", "—"),
     ("R1", "G0/0.30", "192.168.30.1 /24", "—"),
     ("PC10", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC20", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1"),
     ("PC30", "FastEthernet0", "192.168.30.10 /24", "192.168.30.1")],
    [("SW1", '''enable
configure terminal
hostname SW1
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
interface fastEthernet0/2
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
interface fastEthernet0/3
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
interface gigabitEthernet0/1
 description TRUNK_TO_R1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
end
copy running-config startup-config'''),
     ("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 no ip address
 no shutdown
exit
interface gigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
exit
interface gigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
exit
interface gigabitEthernet0/0.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
end
copy running-config startup-config''')],
    ["show ip interface brief", "show interfaces trunk", "show vlan brief", "show ip route connected"],
    [("Gateway", "PC10", "192.168.10.1", "Success"),
     ("Inter-VLAN", "PC10", "192.168.20.10", "Success"),
     ("Inter-VLAN", "PC30", "192.168.10.10", "Success")],
    [("One VLAN fails", "Missing subinterface or VLAN omitted from trunk", "Compare encapsulation VLAN IDs with show interfaces trunk"),
     ("All VLANs fail", "Physical router interface shut or switch port not trunking", "Use no shutdown on G0/0 and verify trunk state")],
    gui_steps=[("Configure all PCs", "Enter the IP address, `/24` mask, and matching `.1` gateway from the addressing table.")]
)

add(
    "08", "02", "Multilayer Switch Inter-VLAN Routing", "Layer 3 switch inter-VLAN routing",
    "Intermediate", "Yes",
    "Use switched virtual interfaces on a multilayer switch to route traffic among three VLANs.",
    'flowchart LR\n    PC10["PC10 VLAN 10"] --- ASW1["Access SW1"] ==>|"Trunk"| MLS1["MLS1 SVIs"]\n    PC20["PC20 VLAN 20"] --- ASW1\n    PC30["PC30 VLAN 30"] --- ASW1',
    [("PC10", "ASW1 F0/1", "Copper straight-through"),
     ("PC20", "ASW1 F0/2", "Copper straight-through"),
     ("PC30", "ASW1 F0/3", "Copper straight-through"),
     ("ASW1 G0/1", "MLS1 G0/1", "Copper crossover or Automatic trunk")],
    [("MLS1", "VLAN 10", "192.168.10.1 /24", "—"),
     ("MLS1", "VLAN 20", "192.168.20.1 /24", "—"),
     ("MLS1", "VLAN 30", "192.168.30.1 /24", "—"),
     ("PC10", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC20", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1"),
     ("PC30", "FastEthernet0", "192.168.30.10 /24", "192.168.30.1")],
    [("MLS1", '''enable
configure terminal
hostname MLS1
ip routing
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
exit
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface vlan 30
 ip address 192.168.30.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
end
copy running-config startup-config'''),
     ("ASW1", '''enable
configure terminal
hostname ASW1
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
interface fastEthernet0/2
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
interface fastEthernet0/3
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
end
copy running-config startup-config''')],
    ["show ip interface brief", "show ip route connected", "show interfaces trunk", "show vlan brief"],
    [("SVI gateway", "PC20", "192.168.20.1", "Success"),
     ("Inter-VLAN", "PC10", "192.168.30.10", "Success")],
    [("SVI protocol is down", "VLAN missing or no active member/trunk port", "Create the VLAN and verify an active Layer 2 path"),
     ("Gateways reply but inter-VLAN fails", "ip routing missing", "Enable ip routing on MLS1")],
    gui_steps=[("Configure PCs", "Enter each PC address and its matching SVI address as the default gateway.")]
)

add(
    "09", "02", "STP - Spanning Tree Protocol Root Bridge Configuration", "STP root bridge configuration",
    "Intermediate", "Yes",
    "Build a redundant triangle and deliberately select the primary and secondary Spanning Tree Protocol (STP) root bridges for VLAN 10.",
    'flowchart TD\n    SW1["SW1 Root Primary"] --- SW2["SW2 Root Secondary"]\n    SW1 --- SW3["SW3 Access"]\n    SW2 --- SW3',
    [("SW1 G0/1", "SW2 G0/1", "Copper crossover or Automatic trunk"),
     ("SW1 G0/2", "SW3 G0/1", "Copper crossover or Automatic trunk"),
     ("SW2 G0/2", "SW3 G0/2", "Copper crossover or Automatic trunk")],
    [("SW1", "VLAN 10", "Layer 2 only", "—"),
     ("SW2", "VLAN 10", "Layer 2 only", "—"),
     ("SW3", "VLAN 10", "Layer 2 only", "—")],
    [("SW1", '''enable
configure terminal
hostname SW1
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
spanning-tree vlan 10 root primary
end
copy running-config startup-config'''),
     ("SW2", '''enable
configure terminal
hostname SW2
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
spanning-tree vlan 10 root secondary
end
copy running-config startup-config'''),
     ("SW3", '''enable
configure terminal
hostname SW3
vlan 10
 name USERS
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree mode pvst
end
copy running-config startup-config''')],
    ["show spanning-tree vlan 10", "show spanning-tree root", "show interfaces trunk"],
    [("Root election", "SW1", "show spanning-tree vlan 10", "This bridge is the root"),
     ("Loop prevention", "SW3", "show spanning-tree vlan 10", "One redundant path is alternate/blocking")],
    [("Wrong root elected", "Priority command missing or applied to wrong VLAN", "Compare bridge IDs and configure root primary for VLAN 10"),
     ("No port blocks", "Triangle is not physically complete or VLAN 10 is absent", "Verify all three trunks and allowed VLANs")],
    notes=["A blocked redundant port is normal STP operation, not a failure."]
)

add(
    "10", "02", "RSTP - Rapid Spanning Tree Protocol with PortFast and BPDU Guard", "RSTP PortFast BPDU Guard configuration",
    "Intermediate", "Yes",
    "Enable Rapid Per-VLAN Spanning Tree, accelerate edge-port forwarding with PortFast, and protect an edge port with Bridge Protocol Data Unit (BPDU) Guard.",
    'flowchart LR\n    PC1["PC1"] --- SW1["SW1 rapid-pvst"] ==>|"Trunk"| SW2["SW2 rapid-pvst"]',
    [("PC1", "SW1 F0/1", "Copper straight-through edge link"),
     ("SW1 G0/1", "SW2 G0/1", "Copper crossover or Automatic trunk")],
    [("PC1", "FastEthernet0", "192.168.10.10 /24", "—"),
     ("SW1/SW2", "VLAN 10", "Layer 2 only", "—")],
    [("SW1", '''enable
configure terminal
hostname SW1
spanning-tree mode rapid-pvst
vlan 10
 name USERS
exit
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
exit
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree vlan 10 root primary
end
copy running-config startup-config'''),
     ("SW2", '''enable
configure terminal
hostname SW2
spanning-tree mode rapid-pvst
vlan 10
 name USERS
exit
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10
exit
spanning-tree vlan 10 root secondary
end
copy running-config startup-config''')],
    ["show spanning-tree summary", "show spanning-tree vlan 10", "show spanning-tree interface fastEthernet0/1 detail", "show interfaces status err-disabled"],
    [("RSTP mode", "SW1", "show spanning-tree summary", "Rapid PVST mode"),
     ("Edge port", "SW1", "F0/1 detail", "PortFast and BPDU Guard enabled")],
    [("F0/1 becomes err-disabled", "A switch sent a BPDU into the edge port", "Remove the switch, then shut/no shut the port after correcting the design"),
     ("Slow convergence", "Switches use different STP modes", "Configure rapid-pvst consistently")],
    gui_steps=[("Configure PC1", "Assign `192.168.10.10/24`. No gateway is required for this Layer 2 control-plane demonstration.")],
    notes=["Use PortFast only toward end devices. Never enable it casually on a switch-to-switch link."]
)

add(
    "11", "02", "EtherChannel with LACP and PAgP", "EtherChannel LACP PAgP configuration",
    "Intermediate", "Yes",
    "Bundle two physical links into one logical trunk using Link Aggregation Control Protocol (LACP), and show the equivalent Port Aggregation Protocol (PAgP) modes.",
    'flowchart LR\n    SW1["SW1"] ==>|"G0/1 + G0/2, Port-channel 1"| SW2["SW2"]',
    [("SW1 G0/1", "SW2 G0/1", "Copper crossover or Automatic"),
     ("SW1 G0/2", "SW2 G0/2", "Copper crossover or Automatic")],
    [("SW1", "Port-channel1", "Layer 2 trunk", "—"),
     ("SW2", "Port-channel1", "Layer 2 trunk", "—")],
    [("SW1 — LACP Active", '''enable
configure terminal
hostname SW1
vlan 10
vlan 20
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 channel-group 1 mode active
 no shutdown
exit
interface port-channel1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
end
copy running-config startup-config'''),
     ("SW2 — LACP Passive", '''enable
configure terminal
hostname SW2
vlan 10
vlan 20
exit
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 channel-group 1 mode passive
 no shutdown
exit
interface port-channel1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
end
copy running-config startup-config'''),
     ("PAgP Alternative — Use on Both Switches Instead of LACP", '''enable
configure terminal
default interface range gigabitEthernet0/1-2
interface range gigabitEthernet0/1-2
 switchport mode trunk
 channel-group 1 mode desirable
 no shutdown
exit
interface port-channel1
 switchport mode trunk
end
copy running-config startup-config''')],
    ["show etherchannel summary", "show etherchannel port-channel", "show interfaces port-channel1", "show interfaces trunk"],
    [("Bundle state", "SW1 and SW2", "show etherchannel summary", "Po1(SU), member ports marked P"),
     ("Resilience", "Either switch", "Disconnect one member link", "Port-channel stays up")],
    [("Ports show suspended", "Speed, duplex, VLAN, trunk, or protocol mismatch", "Make every member configuration identical on both ends"),
     ("LACP does not form", "Both ends passive", "Use active on at least one endpoint")],
    notes=["Do not configure LACP and PAgP simultaneously. The PAgP block is a separate alternative exercise."]
)

add(
    "12", "02", "Switch Port Security", "Port security configuration",
    "Beginner", "Yes",
    "Limit an access port to learned Media Access Control (MAC) addresses and compare protect, restrict, and shutdown violation behaviour.",
    'flowchart LR\n    PC1["Approved PC"] --- SW1["SW1 F0/1 secured"]',
    [("PC1 FastEthernet0", "SW1 F0/1", "Copper straight-through")],
    [("PC1", "FastEthernet0", "192.168.10.10 /24", "—"),
     ("SW1", "F0/1", "Access VLAN 10", "—")],
    [("SW1", '''enable
configure terminal
hostname SW1
vlan 10
 name USERS
exit
interface fastEthernet0/1
 description SECURED_USER_PORT
 switchport mode access
 switchport access vlan 10
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 switchport port-security violation restrict
 spanning-tree portfast
end
copy running-config startup-config''')],
    ["show port-security", "show port-security interface fastEthernet0/1", "show mac address-table interface fastEthernet0/1"],
    [("Sticky learning", "SW1", "F0/1 secure addresses", "One secure MAC appears after PC1 sends traffic"),
     ("Violation", "Replacement PC", "Send traffic through F0/1", "Violation counter increases in restrict mode")],
    [("Port-security command rejected", "Port is dynamic or trunk mode", "Set switchport mode access first"),
     ("Port is secure-shutdown", "Violation mode shutdown triggered", "Remove cause, then shutdown/no shutdown; clear secure MAC if needed")],
    gui_steps=[("Generate traffic from PC1", "Assign `192.168.10.10/24`, then send a ping so SW1 learns the sticky MAC address.")]
)

add(
    "13", "02", "DHCP Snooping, Dynamic ARP Inspection, and IP Source Guard", "DHCP snooping DAI IP Source Guard",
    "Advanced", "Partial",
    "Protect a user VLAN from rogue Dynamic Host Configuration Protocol (DHCP) replies, forged Address Resolution Protocol (ARP) messages, and source-address spoofing.",
    'flowchart LR\n    DHCP["Trusted DHCP Server"] --- SW1["SW1"] --- PC1["Untrusted Client"]',
    [("DHCP Server", "SW1 F0/24", "Copper straight-through trusted port"),
     ("PC1", "SW1 F0/1", "Copper straight-through untrusted port")],
    [("DHCP Server", "FastEthernet0", "192.168.10.5 /24", "192.168.10.1"),
     ("PC1", "FastEthernet0", "DHCP", "192.168.10.1"),
     ("Gateway", "VLAN 10", "192.168.10.1 /24", "—")],
    [("SW1", '''enable
configure terminal
hostname SW1
vlan 10
 name USERS
exit
ip dhcp snooping
ip dhcp snooping vlan 10
ip arp inspection vlan 10
interface fastEthernet0/24
 description TRUSTED_DHCP_SERVER
 switchport mode access
 switchport access vlan 10
 ip dhcp snooping trust
 ip arp inspection trust
exit
interface fastEthernet0/1
 description USER_EDGE_PORT
 switchport mode access
 switchport access vlan 10
 ip dhcp snooping limit rate 15
 ip verify source
 spanning-tree portfast
 spanning-tree bpduguard enable
end
copy running-config startup-config''')],
    ["show ip dhcp snooping", "show ip dhcp snooping binding", "show ip arp inspection", "show ip verify source"],
    [("DHCP lease", "PC1", "Trusted DHCP server", "Client receives a valid VLAN 10 lease"),
     ("Binding", "SW1", "show ip dhcp snooping binding", "PC1 MAC, IP, VLAN, and port appear")],
    [("Client cannot obtain a lease", "Server-facing port not trusted", "Trust only the actual server/uplink port"),
     ("DAI drops legitimate static host", "No DHCP snooping binding", "Use an ARP ACL or supported static binding design")],
    gui_steps=[("Configure the DHCP server", "Set the server to `192.168.10.5/24`, enable DHCP, and create a pool for `192.168.10.0/24` with gateway `192.168.10.1`."),
               ("Configure PC1", "Choose **DHCP** in **Desktop → IP Configuration** and verify the assigned address.")],
    notes=["Packet Tracer support varies by switch image for Dynamic ARP Inspection and IP Source Guard. Use Cisco Modeling Labs, EVE-NG, GNS3, or real switches if a command is unavailable."]
)

add(
    "14", "03", "IPv4 - Internet Protocol Version 4 Static, Default, and Floating Static Routing", "Static routing configuration",
    "Intermediate", "Yes",
    "Connect three IPv4 networks with static routes, add an edge default route, and configure a higher-distance floating backup route.",
    'flowchart LR\n    LAN1["192.168.10.0/24"] --- R1["R1"] ---|"10.0.12.0/30"| R2["R2"] --- LAN2["192.168.20.0/24"]',
    [("LAN1 PC", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic"),
     ("R2 G0/0", "LAN2 PC through switch", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "10.0.12.1 /30", "—"),
     ("R2", "G0/1", "10.0.12.2 /30", "—"),
     ("R2", "G0/0", "192.168.20.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.1 255.255.255.252
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.0.12.2
ip route 0.0.0.0 0.0.0.0 10.0.12.2
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.2 255.255.255.252
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.12.1
ip route 192.168.10.0 255.255.255.0 gigabitEthernet0/0 200
end
copy running-config startup-config''')],
    ["show ip interface brief", "show ip route", "show ip route static", "ping", "traceroute"],
    [("Next-hop", "R1", "10.0.12.2", "Success"),
     ("Remote LAN", "PC1", "192.168.20.10", "Success"),
     ("Route source", "R1", "show ip route 192.168.20.0", "Static route via 10.0.12.2")],
    [("Route absent", "Wrong network/mask or next hop unreachable", "Check connected routes and re-enter the exact destination prefix"),
     ("One-way ping", "Return route missing on R2", "Every router must know the return path"),
     ("Floating route active too early", "Administrative distance not higher than primary", "Use a distance such as 200")],
    gui_steps=[("Configure end devices", "Set PC1 and PC2 from the addressing table, including the local router interface as each default gateway.")],
    notes=["The floating-route exit interface shown is a teaching example. In a real redundant topology, point it toward a genuine alternate path."]
)

add(
    "15", "03", "RIPv2 - Routing Information Protocol Version 2", "RIPv2 configuration",
    "Intermediate", "Yes",
    "Exchange two LAN routes dynamically with Routing Information Protocol Version 2 (RIPv2), disable classful summarisation, and verify learned routes.",
    'flowchart LR\n    LAN1["192.168.10.0/24"] --- R1["R1"] ---|"10.0.12.0/30"| R2["R2"] --- LAN2["192.168.20.0/24"]',
    [("PC1", "R1 G0/0 through SW1", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic"),
     ("R2 G0/0", "PC2 through SW2", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "10.0.12.1 /30", "—"),
     ("R2", "G0/1", "10.0.12.2 /30", "—"),
     ("R2", "G0/0", "192.168.20.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.1 255.255.255.252
 no shutdown
exit
router rip
 version 2
 no auto-summary
 network 192.168.10.0
 network 10.0.0.0
 passive-interface gigabitEthernet0/0
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.2 255.255.255.252
 no shutdown
exit
router rip
 version 2
 no auto-summary
 network 192.168.20.0
 network 10.0.0.0
 passive-interface gigabitEthernet0/0
end
copy running-config startup-config''')],
    ["show ip protocols", "show ip route rip", "show ip route", "debug ip rip"],
    [("RIP route on R1", "R1", "192.168.20.0/24", "Route marked R via 10.0.12.2"),
     ("End-to-end", "PC1", "192.168.20.10", "Success")],
    [("No R routes", "Network statement missing or interface down", "Verify interface networks under show ip protocols"),
     ("Classful route appears", "no auto-summary missing", "Enable no auto-summary on both routers")],
    gui_steps=[("Configure PC1 and PC2", "Use the addresses and gateways in the table, then wait for RIP convergence before testing.")]
)

add(
    "16", "03", "OSPF - Open Shortest Path First Single-Area Configuration", "OSPF single-area configuration",
    "Intermediate", "Yes",
    "Form an Open Shortest Path First (OSPF) adjacency in area 0 and advertise both LANs with correct wildcard masks.",
    'flowchart LR\n    LAN1["192.168.10.0/24"] --- R1["R1 ID 1.1.1.1"] ---|"10.0.12.0/30 Area 0"| R2["R2 ID 2.2.2.2"] --- LAN2["192.168.20.0/24"]',
    [("PC1", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic"),
     ("R2 G0/0", "PC2 through switch", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "10.0.12.1 /30", "—"),
     ("R2", "G0/1", "10.0.12.2 /30", "—"),
     ("R2", "G0/0", "192.168.20.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.1 255.255.255.252
 no shutdown
exit
router ospf 1
 router-id 1.1.1.1
 network 192.168.10.0 0.0.0.255 area 0
 network 10.0.12.0 0.0.0.3 area 0
 passive-interface gigabitEthernet0/0
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.2 255.255.255.252
 no shutdown
exit
router ospf 1
 router-id 2.2.2.2
 network 192.168.20.0 0.0.0.255 area 0
 network 10.0.12.0 0.0.0.3 area 0
 passive-interface gigabitEthernet0/0
end
copy running-config startup-config''')],
    ["show ip ospf neighbor", "show ip ospf interface brief", "show ip route ospf", "show ip protocols"],
    [("Adjacency", "R1", "R2", "Neighbor state FULL"),
     ("Learned route", "R1", "192.168.20.0/24", "Route marked O"),
     ("End-to-end", "PC1", "192.168.20.10", "Success")],
    [("Neighbor absent", "Area, subnet, timers, or interface state mismatch", "Compare show ip ospf interface on both ends"),
     ("Neighbor FULL but route absent", "LAN network statement missing", "Advertise the LAN with the correct wildcard")],
    gui_steps=[("Configure the PCs", "Set both static addresses and local default gateways, then test only after the OSPF neighbor reaches FULL.")]
)

add(
    "17", "03", "OSPF - Open Shortest Path First Multi-Area Configuration", "OSPF multi-area configuration",
    "Advanced", "Yes",
    "Create a three-router OSPF design with backbone area 0 and two non-backbone areas connected through Area Border Routers (ABRs).",
    'flowchart LR\n    LAN10["Area 10 LAN"] --- R1["R1 ABR"] ---|"Area 0"| R2["R2 Backbone"] ---|"Area 0"| R3["R3 ABR"] --- LAN20["Area 20 LAN"]',
    [("LAN10 PC", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/0", "Copper crossover or Automatic"),
     ("R2 G0/1", "R3 G0/1", "Copper crossover or Automatic"),
     ("R3 G0/0", "LAN20 PC through switch", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24 Area 10", "—"),
     ("R1", "G0/1", "10.0.12.1 /30 Area 0", "—"),
     ("R2", "G0/0", "10.0.12.2 /30 Area 0", "—"),
     ("R2", "G0/1", "10.0.23.1 /30 Area 0", "—"),
     ("R3", "G0/1", "10.0.23.2 /30 Area 0", "—"),
     ("R3", "G0/0", "192.168.20.1 /24 Area 20", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.1 255.255.255.252
 no shutdown
router ospf 1
 router-id 1.1.1.1
 network 192.168.10.0 0.0.0.255 area 10
 network 10.0.12.0 0.0.0.3 area 0
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 10.0.12.2 255.255.255.252
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.23.1 255.255.255.252
 no shutdown
router ospf 1
 router-id 2.2.2.2
 network 10.0.12.0 0.0.0.3 area 0
 network 10.0.23.0 0.0.0.3 area 0
end
copy running-config startup-config'''),
     ("R3", '''enable
configure terminal
hostname R3
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.23.2 255.255.255.252
 no shutdown
router ospf 1
 router-id 3.3.3.3
 network 192.168.20.0 0.0.0.255 area 20
 network 10.0.23.0 0.0.0.3 area 0
end
copy running-config startup-config''')],
    ["show ip ospf neighbor", "show ip ospf", "show ip route ospf", "show ip ospf database"],
    [("Both adjacencies", "R2", "R1 and R3", "Two FULL neighbors"),
     ("Inter-area route", "R1", "192.168.20.0/24", "Route marked O IA"),
     ("End-to-end", "PC1", "192.168.20.10", "Success")],
    [("Area 20 unreachable", "R3 backbone link placed in wrong area", "Ensure every ABR connects its non-backbone area to area 0"),
     ("Adjacency stuck", "Address, mask, area, or timers mismatch", "Compare interface-level OSPF parameters")],
    gui_steps=[("Configure the two PCs", "Use `192.168.10.10/24` and `192.168.20.10/24` with their local `.1` gateways.")]
)

add(
    "18", "03", "EIGRP - Enhanced Interior Gateway Routing Protocol", "EIGRP configuration",
    "Intermediate", "Yes",
    "Form an Enhanced Interior Gateway Routing Protocol (EIGRP) adjacency in autonomous system 100 and advertise two LANs without automatic summarisation.",
    'flowchart LR\n    LAN1["192.168.10.0/24"] --- R1["R1"] ---|"10.0.12.0/30"| R2["R2"] --- LAN2["192.168.20.0/24"]',
    [("PC1", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic"),
     ("R2 G0/0", "PC2 through switch", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "10.0.12.1 /30", "—"),
     ("R2", "G0/1", "10.0.12.2 /30", "—"),
     ("R2", "G0/0", "192.168.20.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.1 255.255.255.252
 no shutdown
router eigrp 100
 network 192.168.10.0 0.0.0.255
 network 10.0.12.0 0.0.0.3
 passive-interface gigabitEthernet0/0
 no auto-summary
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.12.2 255.255.255.252
 no shutdown
router eigrp 100
 network 192.168.20.0 0.0.0.255
 network 10.0.12.0 0.0.0.3
 passive-interface gigabitEthernet0/0
 no auto-summary
end
copy running-config startup-config''')],
    ["show ip eigrp neighbors", "show ip eigrp topology", "show ip route eigrp", "show ip protocols"],
    [("Adjacency", "R1", "R2", "Neighbor 10.0.12.2 appears"),
     ("Learned route", "R1", "192.168.20.0/24", "Route marked D"),
     ("End-to-end", "PC1", "192.168.20.10", "Success")],
    [("No neighbor", "Autonomous system mismatch or subnet issue", "Use AS 100 and matching /30 addresses on both routers"),
     ("Neighbor present, route missing", "LAN omitted or passive setting applied to transit link", "Check show ip protocols and network statements")],
    gui_steps=[("Configure the PCs", "Set the two static host addresses and local `.1` default gateways.")]
)

add(
    "19", "04", "DHCP - Dynamic Host Configuration Protocol on a Cisco Router", "Router DHCP configuration",
    "Beginner", "Yes",
    "Configure a Cisco router as a Dynamic Host Configuration Protocol (DHCP) server for VLANs 10 and 20, including excluded addresses and Domain Name System (DNS) settings.",
    'flowchart LR\n    PC10["DHCP Client VLAN 10"] --- SW1["SW1"] ==>|"Trunk"| R1["R1 DHCP Server"]\n    PC20["DHCP Client VLAN 20"] --- SW1',
    [("PC10", "SW1 F0/1", "Copper straight-through"),
     ("PC20", "SW1 F0/2", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through trunk")],
    [("R1", "G0/0.10", "192.168.10.1 /24", "—"),
     ("R1", "G0/0.20", "192.168.20.1 /24", "—"),
     ("PC10", "FastEthernet0", "DHCP from VLAN10 pool", "192.168.10.1"),
     ("PC20", "FastEthernet0", "DHCP from VLAN20 pool", "192.168.20.1")],
    [("SW1", '''enable
configure terminal
hostname SW1
vlan 10
vlan 20
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
interface fastEthernet0/2
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
end
copy running-config startup-config'''),
     ("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 no ip address
 no shutdown
interface gigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
interface gigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
exit
ip dhcp excluded-address 192.168.10.1 192.168.10.20
ip dhcp excluded-address 192.168.20.1 192.168.20.20
ip dhcp pool VLAN10
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 192.168.50.10
 domain-name campus.lab
exit
ip dhcp pool VLAN20
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 192.168.50.10
 domain-name campus.lab
end
copy running-config startup-config''')],
    ["show ip dhcp pool", "show ip dhcp binding", "show ip dhcp conflict", "show interfaces trunk"],
    [("VLAN 10 lease", "PC10", "DHCP", "Receives 192.168.10.21 or later"),
     ("VLAN 20 lease", "PC20", "DHCP", "Receives 192.168.20.21 or later"),
     ("Gateway", "Each PC", "Assigned default gateway", "Matches the local .1 address")],
    [("APIPA address", "No DHCP offer reaches client", "Check VLAN, trunk, subinterface, pool network, and service state"),
     ("Wrong gateway", "Pool default-router value is incorrect", "Match it to the appropriate router subinterface")],
    gui_steps=[("Request DHCP on both PCs", "Open **Desktop → IP Configuration** and select **DHCP**. Use **Command Prompt → ipconfig /all** to confirm the lease.")]
)

add(
    "20", "04", "Central DHCP Server with DHCP Relay", "Dedicated DHCP server and relay configuration",
    "Intermediate", "Yes",
    "Serve clients in multiple VLANs from a dedicated Packet Tracer DHCP server at 200.100.10.5 by using DHCP relay on each gateway.",
    'flowchart LR\n    PC10["VLAN 10 Client"] --- ASW1["ASW1"] ==>|"Trunk"| MLS1["MLS1 helper addresses"] --- DHCP["DHCP Server 200.100.10.5"]\n    PC20["VLAN 20 Client"] --- ASW1',
    [("PC10", "ASW1 F0/1", "Copper straight-through"),
     ("PC20", "ASW1 F0/2", "Copper straight-through"),
     ("ASW1 G0/1", "MLS1 G0/1", "Trunk"),
     ("DHCP Server", "MLS1 F0/24", "Copper straight-through server VLAN")],
    [("MLS1", "VLAN 10", "192.168.10.1 /24", "—"),
     ("MLS1", "VLAN 20", "192.168.20.1 /24", "—"),
     ("MLS1", "VLAN 50", "200.100.10.1 /24", "—"),
     ("DHCP Server", "FastEthernet0", "200.100.10.5 /24", "200.100.10.1"),
     ("PC10/PC20", "FastEthernet0", "DHCP", "From matching pool")],
    [("MLS1", '''enable
configure terminal
hostname MLS1
ip routing
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 50
 name SERVERS
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 ip helper-address 200.100.10.5
 no shutdown
interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 ip helper-address 200.100.10.5
 no shutdown
interface vlan 50
 ip address 200.100.10.1 255.255.255.0
 no shutdown
interface fastEthernet0/24
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,50
end
copy running-config startup-config'''),
     ("ASW1", '''enable
configure terminal
hostname ASW1
vlan 10
vlan 20
vlan 50
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
interface fastEthernet0/2
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,50
end
copy running-config startup-config''')],
    ["show ip interface brief", "show running-config interface vlan 10", "show interfaces trunk", "ipconfig /all"],
    [("Server reachability", "MLS1", "200.100.10.5", "Success"),
     ("VLAN 10 lease", "PC10", "DHCP", "192.168.10.100+ and gateway 192.168.10.1"),
     ("VLAN 20 lease", "PC20", "DHCP", "192.168.20.100+ and gateway 192.168.20.1")],
    [("Only local server VLAN works", "Helper address missing", "Add ip helper-address to every remote client SVI"),
     ("No pools selected", "Server pool gateway/network does not match relay interface", "Match each pool to its client subnet and default gateway")],
    gui_steps=[("Configure the dedicated server", "Set `200.100.10.5/24`, gateway `200.100.10.1`. In **Services → DHCP**, create pool `VLAN10` with gateway `192.168.10.1`, start IP `192.168.10.100`, mask `255.255.255.0`, DNS `200.100.10.5`; add `VLAN20` with gateway `192.168.20.1` and start IP `192.168.20.100`. Turn DHCP **On**."),
               ("Request client leases", "Select **DHCP** on PC10 and PC20, then verify the correct subnet, gateway, and DNS address.")]
)

add(
    "21", "04", "DNS - Domain Name System Server", "DNS server configuration",
    "Beginner", "Yes",
    "Configure a Packet Tracer Domain Name System (DNS) server and resolve a web-server name from a client.",
    'flowchart LR\n    PC1["PC1"] --- SW1["SW1"] --- R1["R1"] --- SW2["Server Switch"]\n    SW2 --- DNS["DNS Server"]\n    SW2 --- WEB["Web Server"]',
    [("PC1", "SW1 F0/1", "Copper straight-through"),
     ("SW1", "R1 G0/0", "Copper straight-through"),
     ("R1 G0/1", "SW2", "Copper straight-through"),
     ("DNS and Web servers", "SW2 access ports", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "192.168.50.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("DNS Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1"),
     ("Web Server", "FastEthernet0", "192.168.50.20 /24", "192.168.50.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 192.168.50.1 255.255.255.0
 no shutdown
end
copy running-config startup-config''')],
    ["show ip interface brief", "ping 192.168.50.10", "nslookup www.campus.lab"],
    [("DNS reachability", "PC1", "192.168.50.10", "Success"),
     ("Name resolution", "PC1", "www.campus.lab", "Resolves to 192.168.50.20"),
     ("Web by name", "PC1 browser", "http://www.campus.lab", "Page opens")],
    [("IP works but name fails", "Wrong PC DNS setting or missing A record", "Set DNS to 192.168.50.10 and add the exact record"),
     ("Name resolves but page fails", "HTTP service off", "Enable HTTP on the web server")],
    gui_steps=[("Configure the DNS server", "Set `192.168.50.10/24`, gateway `192.168.50.1`. Open **Services → DNS**, turn it **On**, and add A record `www.campus.lab` → `192.168.50.20`."),
               ("Configure the web server", "Set `192.168.50.20/24`, gateway `192.168.50.1`, then enable **Services → HTTP**."),
               ("Configure PC1", "Set `192.168.10.10/24`, gateway `192.168.10.1`, and DNS server `192.168.50.10`.")]
)

add(
    "22", "04", "NTP - Network Time Protocol", "NTP configuration",
    "Beginner", "Yes",
    "Synchronise Cisco routers and switches to a Packet Tracer Network Time Protocol (NTP) server and verify clock state.",
    'flowchart LR\n    R1["R1"] --- SW1["SW1"] --- NTP["NTP Server 192.168.50.10"]\n    R2["R2"] --- SW1',
    [("R1 G0/0", "SW1 G0/1", "Copper straight-through"),
     ("R2 G0/0", "SW1 G0/2", "Copper straight-through"),
     ("NTP Server", "SW1 F0/1", "Copper straight-through")],
    [("R1", "G0/0", "192.168.50.1 /24", "—"),
     ("R2", "G0/0", "192.168.50.2 /24", "—"),
     ("NTP Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
clock timezone LKT 5 30
ntp server 192.168.50.10
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.50.2 255.255.255.0
 no shutdown
exit
clock timezone LKT 5 30
ntp server 192.168.50.10
end
copy running-config startup-config''')],
    ["show clock detail", "show ntp associations", "show ntp status", "ping 192.168.50.10"],
    [("Server reachability", "R1 and R2", "192.168.50.10", "Success"),
     ("Association", "R1 and R2", "show ntp associations", "Server appears; selected server may show *"),
     ("Time", "R1 and R2", "show clock detail", "Clocks agree after convergence")],
    [("Unsynchronised", "Insufficient wait time or unreachable server", "Ping the server and allow simulation time to advance"),
     ("Wrong displayed local time", "Timezone missing or incorrect", "Set clock timezone without changing the NTP source")],
    gui_steps=[("Configure the NTP server", "Set `192.168.50.10/24`, gateway `192.168.50.1`. Open **Services → NTP**, turn it **On**, and set the displayed date/time if the activity requires it.")],
    notes=["Packet Tracer NTP convergence and output are simplified compared with a real IOS device."]
)

add(
    "23", "04", "FTP and TFTP File Services", "FTP TFTP server configuration",
    "Beginner", "Yes",
    "Configure Packet Tracer File Transfer Protocol (FTP) and Trivial File Transfer Protocol (TFTP) services, test user authentication, and transfer router files.",
    'flowchart LR\n    R1["R1"] --- SW1["SW1"] --- FILE["FTP/TFTP Server"]\n    PC1["PC1"] --- SW1',
    [("R1 G0/0", "SW1 G0/1", "Copper straight-through"),
     ("PC1", "SW1 F0/1", "Copper straight-through"),
     ("File Server", "SW1 F0/2", "Copper straight-through")],
    [("R1", "G0/0", "192.168.50.1 /24", "—"),
     ("File Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1"),
     ("PC1", "FastEthernet0", "192.168.50.20 /24", "192.168.50.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
end
ping 192.168.50.10
copy running-config startup-config
copy running-config tftp:
192.168.50.10
R1-backup.cfg
copy running-config ftp:
192.168.50.10
netadmin
FilePass!23
R1-ftp-backup.cfg''')],
    ["ping 192.168.50.10", "dir flash:", "show running-config"],
    [("TFTP backup", "R1", "File Server", "R1-backup.cfg appears"),
     ("FTP login", "PC1", "ftp 192.168.50.10", "netadmin authenticates"),
     ("FTP backup", "R1", "File Server", "R1-ftp-backup.cfg appears")],
    [("FTP authentication fails", "Username/password mismatch or service off", "Check the FTP user account and permissions"),
     ("TFTP timeout", "No reachability or TFTP disabled", "Ping server, then enable TFTP")],
    gui_steps=[("Configure file services", "Set the server to `192.168.50.10/24`, gateway `192.168.50.1`. Enable **Services → TFTP**. Under **Services → FTP**, turn FTP on and add user `netadmin` with password `FilePass!23` and full permissions."),
               ("Configure PC1 and test FTP", "Set `192.168.50.20/24`; in Command Prompt run `ftp 192.168.50.10`, log in as `netadmin`, then use `dir`, `get`, or `put` as required.")]
)

add(
    "24", "04", "HTTP, HTTPS, SMTP, POP3, and IMAP Services", "Web and email server configuration",
    "Intermediate", "Partial",
    "Configure Packet Tracer web and email services, publish a web page, create user mailboxes, and test name-based client access.",
    'flowchart LR\n    PC1["PC1"] --- SW1["SW1"] --- SRV["Web DNS Email Server"]\n    PC2["PC2"] --- SW1',
    [("PC1", "SW1 F0/1", "Copper straight-through"),
     ("PC2", "SW1 F0/2", "Copper straight-through"),
     ("Server", "SW1 F0/24", "Copper straight-through")],
    [("Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1"),
     ("PC1", "FastEthernet0", "192.168.50.20 /24", "192.168.50.1"),
     ("PC2", "FastEthernet0", "192.168.50.30 /24", "192.168.50.1")],
    [("Gateway R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
end
copy running-config startup-config''')],
    ["ping 192.168.50.10", "nslookup www.campus.lab", "Browser: http://www.campus.lab", "PC email Send/Receive"],
    [("Web by IP", "PC1", "http://192.168.50.10", "Page opens"),
     ("Web by name", "PC1", "http://www.campus.lab", "DNS resolves and page opens"),
     ("Email", "alice@campus.lab", "bob@campus.lab", "Message is received")],
    [("Web name fails", "DNS record or client DNS address wrong", "Point both clients to 192.168.50.10 and verify A record"),
     ("Mail fails", "Domain, account, or incoming/outgoing server mismatch", "Use campus.lab and server 192.168.50.10 consistently")],
    gui_steps=[("Configure server addressing", "Set `192.168.50.10/24`, gateway `192.168.50.1`, DNS `192.168.50.10`."),
               ("Enable DNS and web", "Under **Services**, enable DNS and add `www.campus.lab` → `192.168.50.10`. Enable HTTP and HTTPS; edit `index.html` with a classroom test page."),
               ("Enable email", "Open **Services → EMAIL**, enable SMTP and POP3, set domain `campus.lab`, then add users `alice` and `bob` with classroom passwords."),
               ("Configure clients", "Give PC1 and PC2 their table addresses and DNS `192.168.50.10`. In **Desktop → Email**, configure Alice and Bob with incoming and outgoing server `192.168.50.10`.")],
    notes=["Packet Tracer commonly simulates SMTP and POP3 but does not fully model modern TLS, certificate validation, or IMAP behaviour. Use a real mail lab for those features."]
)

add(
    "25", "05", "SSH - Secure Shell Remote Management", "SSH configuration",
    "Beginner", "Yes",
    "Secure remote Cisco IOS management with Secure Shell (SSH) version 2, a local privileged user, RSA keys, and SSH-only virtual terminal lines.",
    'flowchart LR\n    ADMIN["Admin PC 192.168.99.10"] --- SW1["SW1"] --- R1["R1 192.168.99.1"]',
    [("Admin PC", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through")],
    [("R1", "G0/0", "192.168.99.1 /24", "—"),
     ("Admin PC", "FastEthernet0", "192.168.99.10 /24", "192.168.99.1")],
    [("R1", '''enable
configure terminal
hostname R1
ip domain-name campus.lab
username netadmin privilege 15 secret SSHpass!23
enable secret Enable!23
interface gigabitEthernet0/0
 ip address 192.168.99.1 255.255.255.0
 no shutdown
exit
crypto key generate rsa modulus 1024
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 10 0
end
copy running-config startup-config''')],
    ["show ip ssh", "show ssh", "show running-config | section line vty", "show users"],
    [("Reachability", "Admin PC", "192.168.99.1", "Success"),
     ("SSH", "Admin PC", "ssh -l netadmin 192.168.99.1", "Encrypted R1 session"),
     ("Telnet rejection", "Admin PC", "telnet 192.168.99.1", "Rejected")],
    [("Invalid input generating keys", "Hostname or domain missing", "Configure both before crypto key generate rsa"),
     ("Login rejected", "VTY not using login local or credentials differ", "Check the username and line vty configuration")],
    gui_steps=[("Configure the Admin PC", "Set `192.168.99.10/24`, gateway `192.168.99.1`. In Command Prompt enter `ssh -l netadmin 192.168.99.1`.")],
    notes=["Use a 2048-bit or stronger key and central identity management on production equipment when supported."]
)

add(
    "26", "05", "AAA - Authentication, Authorization, and Accounting with Local Users", "Local AAA configuration",
    "Intermediate", "Yes",
    "Enable Authentication, Authorization, and Accounting (AAA), apply a local login method list to SSH, and preserve console recovery access.",
    'flowchart LR\n    ADMIN["Admin PC"] --- SW1["SW1"] --- R1["R1 Local AAA"]',
    [("Admin PC", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through")],
    [("R1", "G0/0", "192.168.99.1 /24", "—"),
     ("Admin PC", "FastEthernet0", "192.168.99.10 /24", "192.168.99.1")],
    [("R1", '''enable
configure terminal
hostname R1
ip domain-name campus.lab
username netadmin privilege 15 secret LocalAAA!23
aaa new-model
aaa authentication login VTY-LOCAL local
aaa authorization exec VTY-AUTHZ local
interface gigabitEthernet0/0
 ip address 192.168.99.1 255.255.255.0
 no shutdown
exit
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
 login authentication VTY-LOCAL
 authorization exec VTY-AUTHZ
 transport input ssh
exit
line console 0
 login local
end
copy running-config startup-config''')],
    ["show running-config | section aaa", "show running-config | section line vty", "show users", "debug aaa authentication"],
    [("AAA login", "Admin PC", "SSH as netadmin", "Login succeeds and privileged EXEC is available"),
     ("Invalid login", "Admin PC", "Wrong password", "Access denied")],
    [("All logins fail", "Method list references no valid database", "Use console recovery and verify local user before applying the VTY list"),
     ("User lands without expected rights", "Authorization or privilege not configured", "Check username privilege 15 and exec authorization")],
    gui_steps=[("Test from the Admin PC", "Configure `192.168.99.10/24`, then use `ssh -l netadmin 192.168.99.1`.")],
    notes=["Configure and test the local user before enabling AAA so you do not lock yourself out."]
)

add(
    "27", "05", "RADIUS and TACACS+ Central AAA", "RADIUS TACACS+ AAA configuration",
    "Advanced", "Partial",
    "Authenticate SSH administrators against a central Remote Authentication Dial-In User Service (RADIUS) or Terminal Access Controller Access-Control System Plus (TACACS+) server with a local fallback.",
    'flowchart LR\n    ADMIN["Admin PC"] --- SW1["SW1"] --- R1["R1 AAA Client"]\n    AAA["AAA Server 192.168.50.10"] --- SW1',
    [("Admin PC", "SW1 F0/1", "Copper straight-through"),
     ("AAA Server", "SW1 F0/2", "Copper straight-through"),
     ("R1 G0/0", "SW1 G0/1", "Copper straight-through")],
    [("R1", "G0/0", "192.168.50.1 /24", "—"),
     ("AAA Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1"),
     ("Admin PC", "FastEthernet0", "192.168.50.20 /24", "192.168.50.1")],
    [("R1 — RADIUS Example", '''enable
configure terminal
hostname R1
ip domain-name campus.lab
username emergency privilege 15 secret LocalFallback!23
aaa new-model
radius-server host 192.168.50.10 auth-port 1812 acct-port 1813 key RadiusKey123
aaa authentication login VTY-AUTH group radius local
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
 login authentication VTY-AUTH
 transport input ssh
end
copy running-config startup-config'''),
     ("R1 — TACACS+ Alternative", '''enable
configure terminal
tacacs-server host 192.168.50.10 key TacacsKey123
aaa authentication login VTY-AUTH group tacacs+ local
aaa authorization exec default group tacacs+ local
aaa accounting exec default start-stop group tacacs+
end
copy running-config startup-config''')],
    ["show running-config | section aaa", "show radius statistics", "debug radius authentication", "debug tacacs authentication"],
    [("Central login", "Admin PC", "SSH with server account", "Login accepted by chosen AAA protocol"),
     ("Fallback", "Admin PC", "SSH as emergency while server is unavailable", "Local fallback succeeds")],
    [("Server rejects client", "Router client entry, shared secret, or protocol differs", "Match the router IP and shared secret on both sides"),
     ("No response", "Routing, firewall, or Packet Tracer service limitation", "Ping server and verify the selected AAA service is enabled")],
    gui_steps=[("Configure the AAA server", "Set `192.168.50.10/24`, gateway `192.168.50.1`. Open **Services → AAA**, enable the service, add R1 as a network client with the same shared secret, and create an administrator account."),
               ("Test centrally and locally", "From Admin PC, test the central account first. Then temporarily disable the AAA service and verify the `emergency` local fallback.")],
    notes=["Packet Tracer command syntax and TACACS+ feature depth vary by IOS image. Modern IOS XE commonly uses named `radius server` and `tacacs server` objects; validate against the target platform."]
)

add(
    "28", "05", "Standard IPv4 ACL - Access Control List", "Standard ACL configuration",
    "Intermediate", "Yes",
    "Use a standard IPv4 Access Control List (ACL) near the destination to block one source subnet while permitting all other sources.",
    'flowchart LR\n    LAN10["Blocked 192.168.10.0/24"] --- R1["R1"] --- R2["R2 ACL outbound"] --- SERVER["Server 192.168.30.10"]\n    LAN20["Allowed 192.168.20.0/24"] --- R1',
    [("LAN10 and LAN20 PCs", "R1 access interfaces through switches", "Copper straight-through"),
     ("R1 G0/2", "R2 G0/1", "Copper crossover or Automatic"),
     ("R2 G0/0", "Server switch", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "192.168.20.1 /24", "—"),
     ("R1", "G0/2", "10.0.12.1 /30", "—"),
     ("R2", "G0/1", "10.0.12.2 /30", "—"),
     ("R2", "G0/0", "192.168.30.1 /24", "—"),
     ("Server", "FastEthernet0", "192.168.30.10 /24", "192.168.30.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/2
 ip address 10.0.12.1 255.255.255.252
 no shutdown
exit
ip route 192.168.30.0 255.255.255.0 10.0.12.2
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/1
 ip address 10.0.12.2 255.255.255.252
 no shutdown
interface gigabitEthernet0/0
 ip address 192.168.30.1 255.255.255.0
 ip access-group BLOCK-LAN10 out
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.12.1
ip route 192.168.20.0 255.255.255.0 10.0.12.1
ip access-list standard BLOCK-LAN10
 deny 192.168.10.0 0.0.0.255
 permit any
end
copy running-config startup-config''')],
    ["show access-lists", "show ip interface gigabitEthernet0/0", "show ip route", "ping"],
    [("Blocked source", "LAN10 PC", "192.168.30.10", "Fails"),
     ("Allowed source", "LAN20 PC", "192.168.30.10", "Succeeds"),
     ("Counters", "R2", "show access-lists", "Deny and permit counters increase")],
    [("Everyone blocked", "permit any missing", "Add explicit permit any before the implicit deny"),
     ("ACL has no effect", "Applied to wrong interface/direction", "Use show ip interface and place standard ACL near destination")],
    notes=["Configure and verify routing before applying the ACL; otherwise a routing failure can look like an ACL failure."]
)

add(
    "29", "05", "Extended and Named IPv4 ACL - Access Control List", "Extended named ACL configuration",
    "Intermediate", "Yes",
    "Permit web and Domain Name System (DNS) traffic from a user subnet to a server while denying other traffic, using a named extended IPv4 ACL near the source.",
    'flowchart LR\n    USER["User PC 192.168.10.10"] --- R1["R1 ACL inbound"] --- SERVER["Server 192.168.50.10"]',
    [("User PC", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "Server through switch", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "192.168.50.1 /24", "—"),
     ("User PC", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip access-group USER-TO-SERVER in
 no shutdown
interface gigabitEthernet0/1
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
ip access-list extended USER-TO-SERVER
 remark Permit DNS, HTTP, and HTTPS to the server
 permit udp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 53
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 80
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 443
 deny ip 192.168.10.0 0.0.0.255 host 192.168.50.10
 permit ip any any
end
copy running-config startup-config''')],
    ["show access-lists USER-TO-SERVER", "show ip interface gigabitEthernet0/0", "show running-config | section ip access-list"],
    [("HTTP", "User PC", "http://192.168.50.10", "Allowed"),
     ("HTTPS", "User PC", "https://192.168.50.10", "Allowed if service supported"),
     ("ICMP", "User PC", "192.168.50.10", "Denied"),
     ("Other destinations", "User PC", "Unrelated routed host", "Allowed by final permit")],
    [("DNS still fails", "Only UDP or wrong server address permitted", "Confirm DNS server IP and add TCP 53 if the lesson requires it"),
     ("All later traffic denied", "Final permit ip any any missing", "Account for the implicit deny at the end")],
    gui_steps=[("Configure and enable server services", "Set `192.168.50.10/24`, gateway `192.168.50.1`; enable DNS, HTTP, and HTTPS where available."),
               ("Configure User PC", "Set `192.168.10.10/24`, gateway `192.168.10.1`, and DNS `192.168.50.10`.")]
)

add(
    "30", "05", "NAT and PAT - Network and Port Address Translation", "Static dynamic NAT PAT configuration",
    "Advanced", "Yes",
    "Configure inside/outside roles and demonstrate static Network Address Translation (NAT), dynamic pooled NAT, and Port Address Translation (PAT) as separate alternatives.",
    'flowchart LR\n    PC1["Inside PC 192.168.10.10"] --- R1["R1 NAT"] --- ISP["ISP 203.0.113.1"] --- WEB["Public Server 198.51.100.10"]',
    [("PC1", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "ISP G0/0", "Copper crossover or Automatic"),
     ("ISP G0/1", "Public Server through switch", "Copper straight-through")],
    [("R1", "G0/0 inside", "192.168.10.1 /24", "—"),
     ("R1", "G0/1 outside", "203.0.113.2 /29", "—"),
     ("ISP", "G0/0", "203.0.113.1 /29", "—"),
     ("ISP", "G0/1", "198.51.100.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("Public Server", "FastEthernet0", "198.51.100.10 /24", "198.51.100.1")],
    [("ISP", '''enable
configure terminal
hostname ISP
interface gigabitEthernet0/0
 ip address 203.0.113.1 255.255.255.248
 no shutdown
interface gigabitEthernet0/1
 ip address 198.51.100.1 255.255.255.0
 no shutdown
end
copy running-config startup-config'''),
     ("R1 — PAT Recommended Exercise", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 ip nat inside
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.248
 ip nat outside
 no shutdown
exit
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface gigabitEthernet0/1 overload
ip route 0.0.0.0 0.0.0.0 203.0.113.1
end
copy running-config startup-config'''),
     ("R1 — Static NAT Alternative", '''enable
configure terminal
no ip nat inside source list 1 interface gigabitEthernet0/1 overload
ip nat inside source static 192.168.10.10 203.0.113.3
end
copy running-config startup-config'''),
     ("R1 — Dynamic NAT Alternative", '''enable
configure terminal
no ip nat inside source static 192.168.10.10 203.0.113.3
ip nat pool PUBLIC-POOL 203.0.113.4 203.0.113.6 netmask 255.255.255.248
ip nat inside source list 1 pool PUBLIC-POOL
end
copy running-config startup-config''')],
    ["show ip nat translations", "show ip nat statistics", "show access-lists", "clear ip nat translation *", "show ip route"],
    [("Outside ping", "PC1", "198.51.100.10", "Success with PAT exercise"),
     ("Translation", "R1", "show ip nat translations", "Inside local 192.168.10.10 is translated"),
     ("Statistics", "R1", "show ip nat statistics", "G0/0 inside and G0/1 outside")],
    [("No translations", "NAT roles, ACL, or traffic missing", "Generate traffic and verify inside/outside plus ACL match"),
     ("Route works only from router", "PC gateway missing", "Set PC1 gateway to 192.168.10.1"),
     ("Alternative conflicts", "More than one example enabled", "Remove the prior translation rule before testing another method")],
    gui_steps=[("Configure the inside PC and public server", "Set the static IP addresses and gateways in the table; enable HTTP on the public server for a browser test.")],
    notes=["The documentation ranges 203.0.113.0/24 and 198.51.100.0/24 are used intentionally. In production, use only public addresses assigned and routed by the service provider."]
)

add(
    "30A", "05", "Telnet Legacy Remote Management", "Telnet legacy configuration",
    "Beginner", "Yes",
    "Configure Telnet only for a controlled legacy-protocol demonstration, observe that it lacks strong encryption, and then replace it with Secure Shell (SSH).",
    'flowchart LR\n    PC1["Admin PC"] --- SW1["SW1"] --- R1["R1 Telnet Lab"]',
    [("Admin PC", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through")],
    [("R1", "G0/0", "192.168.99.1 /24", "—"),
     ("Admin PC", "FastEthernet0", "192.168.99.10 /24", "192.168.99.1")],
    [("R1 — Legacy Demonstration Only", '''enable
configure terminal
hostname R1
username legacyadmin privilege 15 secret LegacyOnly!23
interface gigabitEthernet0/0
 ip address 192.168.99.1 255.255.255.0
 no shutdown
exit
line vty 0 4
 login local
 transport input telnet
 exec-timeout 5 0
end
copy running-config startup-config'''),
     ("R1 — Replace Telnet with SSH", '''enable
configure terminal
ip domain-name campus.lab
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
 transport input ssh
end
copy running-config startup-config''')],
    ["show users", "show line vty 0", "show running-config | section line vty", "show ip ssh"],
    [("Legacy access", "Admin PC", "telnet 192.168.99.1", "Works only during the demonstration"),
     ("Migration", "Admin PC", "ssh -l legacyadmin 192.168.99.1", "SSH works after replacement"),
     ("Telnet removal", "Admin PC", "telnet 192.168.99.1", "Rejected after SSH-only transport")],
    [("Telnet login rejected", "No local user or login local missing", "Verify the VTY authentication method"),
     ("Unsafe configuration left enabled", "Migration step skipped", "Change transport input to ssh immediately after the demonstration")],
    gui_steps=[("Configure the Admin PC", "Set `192.168.99.10/24`, gateway `192.168.99.1`. Test Telnet, complete the SSH replacement, and prove Telnet is then rejected.")],
    notes=["Telnet traffic is not strongly encrypted. Never use this configuration for production administration or across an untrusted network."]
)

add(
    "31", "06", "HSRP - Hot Standby Router Protocol with Tracking", "HSRP configuration and tracking",
    "Advanced", "Yes",
    "Provide a resilient virtual default gateway with Hot Standby Router Protocol (HSRP), deterministic active/standby roles, preemption, and uplink tracking.",
    'flowchart TD\n    PC1["PC1 Gateway 192.168.10.1"] --- SW1["Access SW1"]\n    SW1 --- R1["R1 Active 192.168.10.2"]\n    SW1 --- R2["R2 Standby 192.168.10.3"]\n    R1 --- ISP["Upstream"]\n    R2 --- ISP',
    [("PC1", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through"),
     ("SW1 G0/2", "R2 G0/0", "Copper straight-through"),
     ("R1/R2 G0/1", "Upstream switch/router", "Copper straight-through")],
    [("Virtual Gateway", "HSRP group 10", "192.168.10.1 /24", "—"),
     ("R1", "G0/0", "192.168.10.2 /24", "—"),
     ("R2", "G0/0", "192.168.10.3 /24", "—"),
     ("R1", "G0/1", "10.0.1.1 /30", "—"),
     ("R2", "G0/1", "10.0.2.1 /30", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.2 255.255.255.0
 standby 10 ip 192.168.10.1
 standby 10 priority 110
 standby 10 preempt
 standby 10 track gigabitEthernet0/1 20
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.1.1 255.255.255.252
 no shutdown
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.10.3 255.255.255.0
 standby 10 ip 192.168.10.1
 standby 10 priority 100
 standby 10 preempt
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.2.1 255.255.255.252
 no shutdown
end
copy running-config startup-config''')],
    ["show standby brief", "show standby", "show ip interface brief", "ping 192.168.10.1"],
    [("Initial roles", "R1/R2", "show standby brief", "R1 active; R2 standby"),
     ("Virtual gateway", "PC1", "192.168.10.1", "Success"),
     ("Tracked failure", "R1", "Shutdown G0/1", "R1 priority falls and R2 becomes active")],
    [("Both routers active", "Group, subnet, virtual IP, or Layer 2 segment differs", "Make both gateway interfaces share the same LAN and HSRP group"),
     ("R1 does not resume", "Preempt missing", "Configure standby 10 preempt"),
     ("Tracking has no effect", "Tracked interface already down or decrement too small", "Verify interface and effective priority")],
    gui_steps=[("Configure PC1", "Set `192.168.10.10/24` with the **virtual IP** `192.168.10.1` as gateway, never either physical router address.")]
)

add(
    "32", "06", "VRRP - Virtual Router Redundancy Protocol", "VRRP configuration",
    "Advanced", "Partial",
    "Configure Virtual Router Redundancy Protocol (VRRP) with a master, backup, virtual address, and preemption where the selected IOS image supports it.",
    'flowchart TD\n    PC1["PC1 Gateway 192.168.10.1"] --- SW1["Access SW1"]\n    SW1 --- R1["R1 Master"]\n    SW1 --- R2["R2 Backup"]',
    [("PC1", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through"),
     ("SW1 G0/2", "R2 G0/0", "Copper straight-through")],
    [("Virtual Router", "VRRP group 10", "192.168.10.1 /24", "—"),
     ("R1", "G0/0", "192.168.10.2 /24", "—"),
     ("R2", "G0/0", "192.168.10.3 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.2 255.255.255.0
 vrrp 10 ip 192.168.10.1
 vrrp 10 priority 110
 vrrp 10 preempt
 no shutdown
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.10.3 255.255.255.0
 vrrp 10 ip 192.168.10.1
 vrrp 10 priority 100
 vrrp 10 preempt
 no shutdown
end
copy running-config startup-config''')],
    ["show vrrp brief", "show vrrp", "show ip interface brief", "ping 192.168.10.1"],
    [("Initial roles", "R1/R2", "show vrrp brief", "R1 master; R2 backup"),
     ("Gateway", "PC1", "192.168.10.1", "Success"),
     ("Failover", "R1", "Shutdown G0/0", "R2 becomes master")],
    [("vrrp command unavailable", "Packet Tracer IOS image lacks support", "Use HSRP in Packet Tracer or test VRRP in CML/GNS3/EVE-NG"),
     ("No shared state", "Different group or virtual IP", "Match group 10 and 192.168.10.1")],
    gui_steps=[("Configure PC1", "Use `192.168.10.10/24` and virtual gateway `192.168.10.1`.")],
    notes=["Packet Tracer VRRP support is image-dependent. This note remains useful for IOS labs in Cisco Modeling Labs, GNS3, EVE-NG, or real equipment."]
)

add(
    "32A", "06", "GLBP - Gateway Load Balancing Protocol", "GLBP configuration",
    "Advanced", "Partial",
    "Configure Gateway Load Balancing Protocol (GLBP) so two routers provide one resilient virtual gateway while sharing client forwarding responsibility.",
    'flowchart TD\n    PC1["PC1 Gateway 192.168.10.1"] --- SW1["Access SW1"]\n    PC2["PC2 Gateway 192.168.10.1"] --- SW1\n    SW1 --- R1["R1 Active Virtual Gateway"]\n    SW1 --- R2["R2 Active Virtual Forwarder"]',
    [("PC1/PC2", "SW1 access ports", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through"),
     ("SW1 G0/2", "R2 G0/0", "Copper straight-through")],
    [("GLBP Virtual Gateway", "Group 10", "192.168.10.1 /24", "—"),
     ("R1", "G0/0", "192.168.10.2 /24", "—"),
     ("R2", "G0/0", "192.168.10.3 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.10.20 /24", "192.168.10.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.2 255.255.255.0
 glbp 10 ip 192.168.10.1
 glbp 10 priority 110
 glbp 10 preempt
 glbp 10 load-balancing round-robin
 no shutdown
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.10.3 255.255.255.0
 glbp 10 ip 192.168.10.1
 glbp 10 priority 100
 glbp 10 preempt
 glbp 10 load-balancing round-robin
 no shutdown
end
copy running-config startup-config''')],
    ["show glbp brief", "show glbp", "show arp"],
    [("Virtual gateway", "PC1 and PC2", "192.168.10.1", "Success"),
     ("Gateway role", "R1/R2", "show glbp brief", "One active virtual gateway and multiple forwarders"),
     ("Failover", "PC continuous ping", "Shut R1 G0/0", "R2 maintains the virtual gateway")],
    [("glbp command unavailable", "Packet Tracer IOS image lacks GLBP", "Use CML, GNS3, EVE-NG, or real IOS"),
     ("Only one router participates", "Group, subnet, or virtual IP mismatch", "Match group 10 and the virtual address on both routers")],
    gui_steps=[("Configure both PCs", "Assign the table addresses and use the GLBP virtual gateway `192.168.10.1`.")],
    notes=["Unlike HSRP or VRRP, GLBP can distribute host forwarding across multiple active virtual forwarders. Simulator support is image-dependent."]
)

add(
    "33", "07", "SNMPv2c - Simple Network Management Protocol Version 2c", "SNMPv2c configuration",
    "Intermediate", "Partial",
    "Configure read-only Simple Network Management Protocol Version 2c (SNMPv2c), device metadata, and traps toward a management server.",
    'flowchart LR\n    NMS["NMS 192.168.50.10"] --- SW1["SW1"] --- R1["R1 SNMP Agent"]',
    [("NMS Server", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through")],
    [("R1", "G0/0", "192.168.50.1 /24", "—"),
     ("NMS", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
access-list 10 permit host 192.168.50.10
snmp-server community CLASSROOM-RO ro 10
snmp-server location Main-Campus-Room-201
snmp-server contact network-admin@campus.lab
snmp-server host 192.168.50.10 version 2c CLASSROOM-RO
snmp-server enable traps
end
copy running-config startup-config''')],
    ["show running-config | include snmp", "show snmp", "show snmp community", "ping 192.168.50.10"],
    [("Agent reachability", "NMS", "192.168.50.1", "Success"),
     ("Polling", "NMS", "R1 with CLASSROOM-RO", "System description/location returned"),
     ("Trap destination", "R1", "Running configuration", "192.168.50.10 configured")],
    [("Polling times out", "Community, ACL, or reachability mismatch", "Match exact case and permit only the NMS address"),
     ("No traps", "Trap receiver or enable command missing", "Configure host and enable required trap categories")],
    gui_steps=[("Prepare the management server", "Set `192.168.50.10/24`, gateway `192.168.50.1`. Use the available Packet Tracer SNMP/NMS application to add R1 at `192.168.50.1` with community `CLASSROOM-RO`.")],
    notes=["SNMPv2c community strings are clear-text shared secrets. Use SNMPv3 in production."]
)

add(
    "34", "07", "SNMPv3 - Simple Network Management Protocol Version 3", "SNMPv3 configuration",
    "Advanced", "Partial",
    "Configure authenticated and encrypted Simple Network Management Protocol Version 3 (SNMPv3) access with a restricted management source.",
    'flowchart LR\n    NMS["Secure NMS 192.168.50.10"] --- SW1["SW1"] --- R1["R1 SNMPv3 Agent"]',
    [("NMS", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through")],
    [("R1", "G0/0", "192.168.50.1 /24", "—"),
     ("NMS", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
access-list 10 permit host 192.168.50.10
snmp-server view CAMPUS-VIEW iso included
snmp-server group CAMPUS-GROUP v3 priv read CAMPUS-VIEW access 10
snmp-server user snmpadmin CAMPUS-GROUP v3 auth sha AuthPass123 priv aes 128 PrivPass123
snmp-server location Main-Campus-Room-201
snmp-server contact network-admin@campus.lab
end
copy running-config startup-config''')],
    ["show snmp user", "show snmp group", "show snmp view", "show access-lists 10"],
    [("User", "R1", "show snmp user", "snmpadmin uses authentication and privacy"),
     ("Secure poll", "NMS", "R1", "Authenticated encrypted response")],
    [("User not visible in running config", "IOS hides SNMPv3 secrets", "Use show snmp user rather than expecting plaintext"),
     ("Authentication failure", "User/group/password/algorithm mismatch", "Match SHA, AES-128, and both passphrases exactly")],
    gui_steps=[("Configure the NMS", "If your simulator supports SNMPv3, add user `snmpadmin`, SHA authentication password `AuthPass123`, AES-128 privacy password `PrivPass123`, and target `192.168.50.1`.")],
    notes=["Packet Tracer may not provide a complete SNMPv3 manager or all IOS commands. Verify this configuration in CML, GNS3, EVE-NG, Linux net-snmp, or on real Cisco IOS."]
)

add(
    "35", "07", "Syslog Central Logging", "Syslog configuration",
    "Beginner", "Yes",
    "Send timestamped informational Cisco IOS messages to a central Syslog server and verify local and remote logging.",
    'flowchart LR\n    R1["R1"] --- SW1["SW1"] --- SYSLOG["Syslog Server 192.168.50.10"]',
    [("R1 G0/0", "SW1 G0/1", "Copper straight-through"),
     ("Syslog Server", "SW1 F0/1", "Copper straight-through")],
    [("R1", "G0/0", "192.168.50.1 /24", "—"),
     ("Syslog Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit
service timestamps log datetime msec
logging host 192.168.50.10
logging trap informational
logging source-interface gigabitEthernet0/0
logging buffered 16384 informational
end
copy running-config startup-config''')],
    ["show logging", "show clock", "ping 192.168.50.10", "show running-config | include logging"],
    [("Reachability", "R1", "192.168.50.10", "Success"),
     ("Test message", "R1", "Shutdown/no shutdown a spare interface", "Messages appear on server"),
     ("Timestamp", "Syslog Server", "Received entry", "Date/time included")],
    [("No remote logs", "Service off, wrong address, routing issue, or severity too restrictive", "Enable server, ping it, and inspect show logging"),
     ("Wrong source IP", "No source interface set", "Use a stable reachable management interface")],
    gui_steps=[("Configure the Syslog server", "Set `192.168.50.10/24`, gateway `192.168.50.1`. Open **Services → SYSLOG** and switch it **On**.")]
)

add(
    "36", "07", "CDP and LLDP - Cisco and Link Layer Discovery Protocols", "CDP LLDP configuration",
    "Beginner", "Partial",
    "Enable and verify Cisco Discovery Protocol (CDP) and Link Layer Discovery Protocol (LLDP), then disable discovery on an untrusted edge port.",
    'flowchart LR\n    R1["R1"] --- SW1["SW1"] --- SW2["SW2"]\n    PC1["Untrusted PC"] --- SW1',
    [("R1 G0/0", "SW1 G0/1", "Copper straight-through"),
     ("SW1 G0/2", "SW2 G0/1", "Copper crossover or Automatic"),
     ("PC1", "SW1 F0/1", "Copper straight-through")],
    [("R1", "G0/0", "192.168.99.1 /24", "—"),
     ("SW1", "VLAN 99", "192.168.99.2 /24", "192.168.99.1"),
     ("SW2", "VLAN 99", "192.168.99.3 /24", "192.168.99.1")],
    [("R1", '''enable
configure terminal
hostname R1
cdp run
lldp run
interface gigabitEthernet0/0
 ip address 192.168.99.1 255.255.255.0
 no shutdown
end
copy running-config startup-config'''),
     ("SW1", '''enable
configure terminal
hostname SW1
cdp run
lldp run
vlan 99
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 no shutdown
interface fastEthernet0/1
 no cdp enable
 no lldp transmit
 no lldp receive
end
copy running-config startup-config'''),
     ("SW2", '''enable
configure terminal
hostname SW2
cdp run
lldp run
vlan 99
interface vlan 99
 ip address 192.168.99.3 255.255.255.0
 no shutdown
end
copy running-config startup-config''')],
    ["show cdp neighbors", "show cdp neighbors detail", "show lldp neighbors", "show lldp neighbors detail"],
    [("Cisco discovery", "SW1", "R1 and SW2", "Neighbors appear in CDP table"),
     ("Open discovery", "SW1", "Connected LLDP-capable devices", "Neighbors appear where supported"),
     ("Edge privacy", "SW1", "F0/1", "No discovery advertisements sent or accepted")],
    [("No LLDP command", "Packet Tracer switch image limitation", "Use CDP in Packet Tracer or test LLDP on supported IOS"),
     ("Neighbor missing", "Protocol disabled or interface down", "Check global and per-interface discovery state")],
    notes=["CDP is Cisco proprietary; LLDP is the multi-vendor IEEE 802.1AB alternative."]
)

add(
    "37", "08", "GRE - Generic Routing Encapsulation Tunnel", "GRE tunnel configuration",
    "Advanced", "Partial",
    "Build a Generic Routing Encapsulation (GRE) tunnel between two routers, route private LAN traffic through it, and verify tunnel reachability.",
    'flowchart LR\n    LAN1["192.168.10.0/24"] --- R1["R1 Tunnel0"] ---|"203.0.113.0/30 underlay"| R2["R2 Tunnel0"] --- LAN2["192.168.20.0/24"]',
    [("LAN1 PC", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic underlay"),
     ("R2 G0/0", "LAN2 PC through switch", "Copper straight-through")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "203.0.113.1 /30", "—"),
     ("R1", "Tunnel0", "10.10.10.1 /30", "—"),
     ("R2", "G0/1", "203.0.113.2 /30", "—"),
     ("R2", "Tunnel0", "10.10.10.2 /30", "—"),
     ("R2", "G0/0", "192.168.20.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 no shutdown
interface tunnel0
 ip address 10.10.10.1 255.255.255.252
 tunnel source gigabitEthernet0/1
 tunnel destination 203.0.113.2
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.10.10.2
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.252
 no shutdown
interface tunnel0
 ip address 10.10.10.2 255.255.255.252
 tunnel source gigabitEthernet0/1
 tunnel destination 203.0.113.1
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.10.10.1
end
copy running-config startup-config''')],
    ["show interfaces tunnel0", "show ip interface brief", "show ip route", "ping 10.10.10.2 source 10.10.10.1"],
    [("Underlay", "R1", "203.0.113.2", "Success"),
     ("Tunnel", "R1", "10.10.10.2", "Success"),
     ("Private LAN", "PC1", "192.168.20.10", "Success through Tunnel0")],
    [("Tunnel up/down", "Destination route or far endpoint unavailable", "Verify underlay connectivity and tunnel destination"),
     ("Tunnel ping works but LAN fails", "Static LAN route or PC gateway missing", "Check routes and both host gateways")],
    gui_steps=[("Configure end PCs", "Set PC1 and PC2 from the table and use each local router LAN address as the gateway.")],
    notes=["GRE provides encapsulation but not encryption. Protect sensitive GRE traffic with IPsec on a capable platform."]
)

add(
    "38", "08", "PPP with PAP and CHAP - Point-to-Point Protocol Authentication", "PPP PAP CHAP configuration",
    "Advanced", "Partial",
    "Configure a serial Point-to-Point Protocol (PPP) link and test Password Authentication Protocol (PAP) and Challenge Handshake Authentication Protocol (CHAP) as separate authentication methods.",
    'flowchart LR\n    LAN1["192.168.10.0/24"] --- R1["R1 DCE"] ==>|"Serial PPP"| R2["R2 DTE"] --- LAN2["192.168.20.0/24"]',
    [("R1 S0/0/0", "R2 S0/0/0", "Serial DCE/DTE; add compatible serial modules first"),
     ("LAN PCs", "Router G0/0 through switches", "Copper straight-through")],
    [("R1", "S0/0/0", "10.0.12.1 /30", "—"),
     ("R2", "S0/0/0", "10.0.12.2 /30", "—"),
     ("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R2", "G0/0", "192.168.20.1 /24", "—")],
    [("R1 — CHAP Recommended", '''enable
configure terminal
hostname R1
username R2 password ChapSecret123
interface serial0/0/0
 ip address 10.0.12.1 255.255.255.252
 encapsulation ppp
 ppp authentication chap
 clock rate 64000
 no shutdown
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 10.0.12.2
end
copy running-config startup-config'''),
     ("R2 — CHAP Recommended", '''enable
configure terminal
hostname R2
username R1 password ChapSecret123
interface serial0/0/0
 ip address 10.0.12.2 255.255.255.252
 encapsulation ppp
 ppp authentication chap
 no shutdown
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 10.0.12.1
end
copy running-config startup-config'''),
     ("PAP Alternative — R1 Interface", '''enable
configure terminal
username R2 password PapSecret123
interface serial0/0/0
 ppp authentication pap
 ppp pap sent-username R1 password PapSecret123
end
copy running-config startup-config'''),
     ("PAP Alternative — R2 Interface", '''enable
configure terminal
username R1 password PapSecret123
interface serial0/0/0
 ppp authentication pap
 ppp pap sent-username R2 password PapSecret123
end
copy running-config startup-config''')],
    ["show interfaces serial0/0/0", "show controllers serial0/0/0", "show ip interface brief", "debug ppp authentication"],
    [("PPP state", "R1/R2", "show interfaces serial0/0/0", "Line and protocol are up; encapsulation PPP"),
     ("Neighbor ping", "R1", "10.0.12.2", "Success"),
     ("Authentication failure", "One router", "Temporarily change secret", "Line protocol fails")],
    [("Serial interface missing", "No serial module installed", "Power off router, install supported HWIC/WIC, then recable"),
     ("Line protocol down", "Encapsulation, username, hostname, or secret mismatch", "Match PPP mode and CHAP peer-hostname credentials"),
     ("Clock rate rejected", "Command entered on DTE side", "Apply clock rate only to the DCE endpoint")],
    notes=["PAP sends reusable credentials and is weaker than CHAP. Configure only one authentication alternative at a time."]
)

add(
    "39", "08", "IPsec - Internet Protocol Security Site-to-Site VPN", "IPsec site-to-site VPN configuration",
    "Advanced", "Partial",
    "Protect traffic between two private LANs with an Internet Protocol Security (IPsec) site-to-site virtual private network using an Internet Key Exchange policy, transform set, crypto ACL, and crypto map.",
    'flowchart LR\n    LAN1["192.168.10.0/24"] --- R1["R1 VPN Peer"] ---|"203.0.113.0/30"| R2["R2 VPN Peer"] --- LAN2["192.168.20.0/24"]',
    [("LAN PCs", "Router G0/0 through switches", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic WAN")],
    [("R1", "G0/0", "192.168.10.1 /24", "—"),
     ("R1", "G0/1", "203.0.113.1 /30", "—"),
     ("R2", "G0/1", "203.0.113.2 /30", "—"),
     ("R2", "G0/0", "192.168.20.1 /24", "—"),
     ("PC1", "FastEthernet0", "192.168.10.10 /24", "192.168.10.1"),
     ("PC2", "FastEthernet0", "192.168.20.10 /24", "192.168.20.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.252
 no shutdown
exit
ip route 192.168.20.0 255.255.255.0 203.0.113.2
access-list 110 permit ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
crypto isakmp policy 10
 encr aes
 hash sha
 authentication pre-share
 group 2
exit
crypto isakmp key VPNkey123 address 203.0.113.2
crypto ipsec transform-set CAMPUS-SET esp-aes esp-sha-hmac
crypto map CAMPUS-MAP 10 ipsec-isakmp
 set peer 203.0.113.2
 set transform-set CAMPUS-SET
 match address 110
exit
interface gigabitEthernet0/1
 crypto map CAMPUS-MAP
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface gigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.252
 no shutdown
exit
ip route 192.168.10.0 255.255.255.0 203.0.113.1
access-list 110 permit ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
crypto isakmp policy 10
 encr aes
 hash sha
 authentication pre-share
 group 2
exit
crypto isakmp key VPNkey123 address 203.0.113.1
crypto ipsec transform-set CAMPUS-SET esp-aes esp-sha-hmac
crypto map CAMPUS-MAP 10 ipsec-isakmp
 set peer 203.0.113.1
 set transform-set CAMPUS-SET
 match address 110
exit
interface gigabitEthernet0/1
 crypto map CAMPUS-MAP
end
copy running-config startup-config''')],
    ["show crypto isakmp sa", "show crypto ipsec sa", "show crypto map", "show access-lists 110"],
    [("Underlay", "R1", "203.0.113.2", "Success"),
     ("Interesting traffic", "PC1", "192.168.20.10", "Success and tunnel forms"),
     ("Encrypted counters", "R1/R2", "show crypto ipsec sa", "Encaps/decaps counters increase")],
    [("No ISAKMP security association", "Peer, key, policy, or reachability mismatch", "Compare both policies and ping public peer"),
     ("ISAKMP up but no IPsec packets", "Crypto ACLs are not mirrored or traffic does not match", "Verify source/destination networks in ACL 110"),
     ("Commands unavailable", "Packet Tracer image limitation", "Move the lab to Cisco Modeling Labs, GNS3, EVE-NG, or real IOS")],
    gui_steps=[("Configure both PCs", "Assign the private LAN addresses and local router gateways, then generate PC-to-PC traffic to bring up the tunnel.")],
    notes=["The algorithms are chosen for broad simulator compatibility, not as a modern production security recommendation. Use current platform-supported IKEv2 and strong cryptography in production."]
)

add(
    "40", "08", "WPA2 - Wi-Fi Protected Access 2 Wireless LAN", "WPA2 wireless configuration",
    "Beginner", "Yes",
    "Create a secured wireless local area network with a service set identifier (SSID), Wi-Fi Protected Access 2 (WPA2) pre-shared key, DHCP, and client association.",
    'flowchart LR\n    LAPTOP["Wireless Laptop"] -. "SSID CAMPUS-WIFI" .-> AP["Access Point"] --- SW1["SW1"] --- R1["R1 Gateway"]',
    [("Access Point Ethernet", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through"),
     ("Laptop", "Access Point", "802.11 wireless association")],
    [("R1", "G0/0", "192.168.40.1 /24", "—"),
     ("Access Point", "Management", "192.168.40.2 /24", "192.168.40.1"),
     ("Laptop", "Wireless0", "DHCP 192.168.40.100+", "192.168.40.1")],
    [("R1", '''enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.40.1 255.255.255.0
 no shutdown
exit
ip dhcp excluded-address 192.168.40.1 192.168.40.99
ip dhcp pool WIRELESS-USERS
 network 192.168.40.0 255.255.255.0
 default-router 192.168.40.1
 dns-server 192.168.40.1
end
copy running-config startup-config''')],
    ["show ip dhcp binding", "show ip dhcp pool", "Laptop: ipconfig /all", "Laptop: ping 192.168.40.1"],
    [("Association", "Laptop", "CAMPUS-WIFI", "Connected with WPA2"),
     ("DHCP", "Laptop", "WIRELESS-USERS pool", "Receives 192.168.40.100 or later"),
     ("Gateway", "Laptop", "192.168.40.1", "Success")],
    [("SSID not visible", "Radio off or SSID differs", "Enable AP radio and match the exact SSID"),
     ("Authentication fails", "Security mode or key mismatch", "Use WPA2-PSK/AES and the exact same key"),
     ("Associated but no address", "DHCP or wired uplink issue", "Check AP-to-switch link and router DHCP pool")],
    gui_steps=[("Configure the access point", "Set management IP `192.168.40.2/24` and gateway `192.168.40.1`. Set SSID `CAMPUS-WIFI`, security **WPA2-PSK**, encryption **AES**, and key `CampusWiFi!23`. Choose a non-overlapping channel appropriate to the classroom."),
               ("Configure the laptop", "Install/enable its wireless interface if required. Open **Desktop → PC Wireless**, select `CAMPUS-WIFI`, choose WPA2-PSK, enter `CampusWiFi!23`, then request DHCP.")],
    notes=["WPA3 and enterprise 802.1X support are limited in Packet Tracer. Use a wireless controller lab, real access point, or suitable emulator for production-grade demonstrations."]
)

add(
    "41", "09", "IPv6 - Internet Protocol Version 6 Addressing and Static Routing", "IPv6 static routing configuration",
    "Intermediate", "Yes",
    "Enable Internet Protocol Version 6 (IPv6) forwarding, configure global unicast and link-local addresses, and connect two IPv6 LANs with static routes.",
    'flowchart LR\n    LAN1["2001:DB8:10::/64"] --- R1["R1"] ---|"2001:DB8:12::/64"| R2["R2"] --- LAN2["2001:DB8:20::/64"]',
    [("PC1", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic"),
     ("R2 G0/0", "PC2 through switch", "Copper straight-through")],
    [("R1", "G0/0", "2001:DB8:10::1/64; FE80::1", "—"),
     ("R1", "G0/1", "2001:DB8:12::1/64; FE80::1", "—"),
     ("R2", "G0/1", "2001:DB8:12::2/64; FE80::2", "—"),
     ("R2", "G0/0", "2001:DB8:20::1/64; FE80::2", "—"),
     ("PC1", "FastEthernet0", "2001:DB8:10::10/64", "2001:DB8:10::1"),
     ("PC2", "FastEthernet0", "2001:DB8:20::10/64", "2001:DB8:20::1")],
    [("R1", '''enable
configure terminal
hostname R1
ipv6 unicast-routing
interface gigabitEthernet0/0
 ipv6 address 2001:DB8:10::1/64
 ipv6 address FE80::1 link-local
 no shutdown
interface gigabitEthernet0/1
 ipv6 address 2001:DB8:12::1/64
 ipv6 address FE80::1 link-local
 no shutdown
exit
ipv6 route 2001:DB8:20::/64 2001:DB8:12::2
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
ipv6 unicast-routing
interface gigabitEthernet0/0
 ipv6 address 2001:DB8:20::1/64
 ipv6 address FE80::2 link-local
 no shutdown
interface gigabitEthernet0/1
 ipv6 address 2001:DB8:12::2/64
 ipv6 address FE80::2 link-local
 no shutdown
exit
ipv6 route 2001:DB8:10::/64 2001:DB8:12::1
end
copy running-config startup-config''')],
    ["show ipv6 interface brief", "show ipv6 route", "show ipv6 neighbors", "ping 2001:DB8:12::2"],
    [("Transit", "R1", "2001:DB8:12::2", "Success"),
     ("Remote LAN", "PC1", "2001:DB8:20::10", "Success"),
     ("Neighbor discovery", "R1", "show ipv6 neighbors", "R2 transit address appears")],
    [("Local interface works, routing fails", "ipv6 unicast-routing missing", "Enable it globally on both routers"),
     ("Remote subnet absent", "Static route prefix or next hop wrong", "Use the exact /64 remote prefix and reachable next hop")],
    gui_steps=[("Configure both PCs", "Select **IPv6 Configuration → Static** and enter each global address, `/64` prefix, and local router global address as the gateway.")]
)

add(
    "42", "09", "SLAAC - Stateless Address Autoconfiguration with DHCPv6", "SLAAC DHCPv6 configuration",
    "Intermediate", "Partial",
    "Configure Stateless Address Autoconfiguration (SLAAC), stateless Dynamic Host Configuration Protocol for IPv6 (DHCPv6), and stateful DHCPv6 as clearly separated client-addressing alternatives.",
    'flowchart LR\n    PC1["IPv6 Client"] --- SW1["SW1"] --- R1["R1 Router Advertisement and DHCPv6"]',
    [("PC1", "SW1 F0/1", "Copper straight-through"),
     ("SW1 G0/1", "R1 G0/0", "Copper straight-through")],
    [("R1", "G0/0", "2001:DB8:10::1/64; FE80::1", "—"),
     ("PC1", "FastEthernet0", "SLAAC or DHCPv6", "FE80::1 learned from Router Advertisement")],
    [("R1 — SLAAC Only", '''enable
configure terminal
hostname R1
ipv6 unicast-routing
interface gigabitEthernet0/0
 ipv6 address 2001:DB8:10::1/64
 ipv6 address FE80::1 link-local
 no shutdown
end
copy running-config startup-config'''),
     ("R1 — Stateless DHCPv6 Alternative", '''enable
configure terminal
ipv6 dhcp pool STATELESS-V6
 dns-server 2001:DB8:50::53
 domain-name campus.lab
exit
interface gigabitEthernet0/0
 ipv6 nd other-config-flag
 ipv6 dhcp server STATELESS-V6
end
copy running-config startup-config'''),
     ("R1 — Stateful DHCPv6 Alternative", '''enable
configure terminal
ipv6 local pool V6-PREFIX 2001:DB8:10::/64 64
ipv6 dhcp pool STATEFUL-V6
 address prefix 2001:DB8:10::/64
 dns-server 2001:DB8:50::53
 domain-name campus.lab
exit
interface gigabitEthernet0/0
 ipv6 nd managed-config-flag
 ipv6 dhcp server STATEFUL-V6
end
copy running-config startup-config''')],
    ["show ipv6 interface gigabitEthernet0/0", "show ipv6 dhcp pool", "show ipv6 dhcp binding", "show ipv6 neighbors"],
    [("SLAAC", "PC1", "Automatic IPv6", "Global address in 2001:DB8:10::/64 and a link-local address"),
     ("Router Advertisement", "PC1", "Default route", "Learns router through ICMPv6 RA"),
     ("DHCPv6 option", "PC1", "Stateless/stateful exercise", "Receives supported DNS or address information")],
    [("No global address", "IPv6 routing/interface/RA unavailable", "Enable ipv6 unicast-routing and bring G0/0 up"),
     ("DHCPv6 pool unused", "Flag or interface pool binding missing", "Apply the correct ND flag and ipv6 dhcp server command")],
    gui_steps=[("Configure PC1", "Select **IPv6 Auto Config** for SLAAC. For DHCPv6 alternatives, select the simulator's DHCPv6 option and renew after changing the router configuration.")],
    notes=["Run one alternative at a time. Packet Tracer DHCPv6 client and server behaviour depends on the selected device image; use CML or real IOS if a command is missing."]
)

add(
    "43", "09", "OSPFv3 - Open Shortest Path First Version 3 for IPv6", "OSPFv3 IPv6 configuration",
    "Advanced", "Yes",
    "Form an Open Shortest Path First Version 3 (OSPFv3) adjacency and exchange IPv6 LAN prefixes through area 0.",
    'flowchart LR\n    LAN1["2001:DB8:10::/64"] --- R1["R1 ID 1.1.1.1"] ---|"2001:DB8:12::/64 Area 0"| R2["R2 ID 2.2.2.2"] --- LAN2["2001:DB8:20::/64"]',
    [("PC1", "R1 G0/0 through switch", "Copper straight-through"),
     ("R1 G0/1", "R2 G0/1", "Copper crossover or Automatic"),
     ("R2 G0/0", "PC2 through switch", "Copper straight-through")],
    [("R1", "G0/0", "2001:DB8:10::1/64", "—"),
     ("R1", "G0/1", "2001:DB8:12::1/64", "—"),
     ("R2", "G0/1", "2001:DB8:12::2/64", "—"),
     ("R2", "G0/0", "2001:DB8:20::1/64", "—"),
     ("PC1", "FastEthernet0", "2001:DB8:10::10/64", "2001:DB8:10::1"),
     ("PC2", "FastEthernet0", "2001:DB8:20::10/64", "2001:DB8:20::1")],
    [("R1", '''enable
configure terminal
hostname R1
ipv6 unicast-routing
ipv6 router ospf 10
 router-id 1.1.1.1
exit
interface gigabitEthernet0/0
 ipv6 address 2001:DB8:10::1/64
 ipv6 ospf 10 area 0
 no shutdown
interface gigabitEthernet0/1
 ipv6 address 2001:DB8:12::1/64
 ipv6 ospf 10 area 0
 no shutdown
end
copy running-config startup-config'''),
     ("R2", '''enable
configure terminal
hostname R2
ipv6 unicast-routing
ipv6 router ospf 10
 router-id 2.2.2.2
exit
interface gigabitEthernet0/0
 ipv6 address 2001:DB8:20::1/64
 ipv6 ospf 10 area 0
 no shutdown
interface gigabitEthernet0/1
 ipv6 address 2001:DB8:12::2/64
 ipv6 ospf 10 area 0
 no shutdown
end
copy running-config startup-config''')],
    ["show ipv6 ospf neighbor", "show ipv6 ospf interface brief", "show ipv6 route ospf", "show ipv6 protocols"],
    [("Adjacency", "R1", "R2", "Neighbor state FULL"),
     ("Learned prefix", "R1", "2001:DB8:20::/64", "Route marked O"),
     ("End-to-end", "PC1", "2001:DB8:20::10", "Success")],
    [("No neighbor", "OSPFv3 missing on transit interface or interface down", "Apply ipv6 ospf 10 area 0 to both transit interfaces"),
     ("Router ID error", "No IPv4 address and no manual router ID", "Configure router-id under ipv6 router ospf")],
    gui_steps=[("Configure IPv6 hosts", "Give each PC the static global address, `/64` prefix, and matching local router gateway from the table.")]
)

add(
    "44", "10", "Complete Enterprise Campus Configuration", "Enterprise campus configuration",
    "Advanced", "Yes",
    "Integrate VLANs, trunks, Rapid Spanning Tree, Hot Standby Router Protocol, inter-VLAN routing, Open Shortest Path First, central DHCP relay, Domain Name System, Network Time Protocol, Syslog, Simple Network Management Protocol, Secure Shell, and Port Address Translation in one campus example.",
    'flowchart TD\n    PC10["Admin PC VLAN 10"] --- ASW1["ASW1"]\n    PC20["Staff PC VLAN 20"] --- ASW1\n    PC30["Student PC VLAN 30"] --- ASW1\n    SRV["Services 192.168.50.10"] --- ASW1\n    ASW1 ==>|"Trunk"| MLS1["MLS1 HSRP Active"]\n    ASW1 ==>|"Trunk"| MLS2["MLS2 HSRP Standby"]\n    MLS1 --- EDGE["EDGE1 OSPF NAT"]\n    MLS2 --- EDGE\n    EDGE --- ISP["ISP"] --- WEB["Internet Server"]',
    [("PC10/PC20/PC30", "ASW1 F0/1-3", "Copper straight-through access links"),
     ("Services Server", "ASW1 F0/10", "Copper straight-through VLAN 50"),
     ("ASW1 G0/1", "MLS1 G0/1", "802.1Q trunk"),
     ("ASW1 G0/2", "MLS2 G0/1", "802.1Q trunk"),
     ("MLS1 G0/2", "EDGE1 G0/0", "Layer 3 routed link"),
     ("MLS2 G0/2", "EDGE1 G0/1", "Layer 3 routed link"),
     ("EDGE1 G0/2", "ISP G0/0", "WAN routed link"),
     ("ISP G0/1", "Internet Server", "Copper straight-through")],
    [("VLAN 10 virtual", "HSRP", "192.168.10.1 /24", "—"),
     ("VLAN 20 virtual", "HSRP", "192.168.20.1 /24", "—"),
     ("VLAN 30 virtual", "HSRP", "192.168.30.1 /24", "—"),
     ("VLAN 50 virtual", "HSRP", "192.168.50.1 /24", "—"),
     ("VLAN 99 virtual", "HSRP", "192.168.99.1 /24", "—"),
     ("MLS1", "G0/2", "10.0.1.1 /30", "—"),
     ("EDGE1", "G0/0", "10.0.1.2 /30", "—"),
     ("MLS2", "G0/2", "10.0.2.1 /30", "—"),
     ("EDGE1", "G0/1", "10.0.2.2 /30", "—"),
     ("EDGE1", "G0/2", "203.0.113.2 /30", "—"),
     ("ISP", "G0/0", "203.0.113.1 /30", "—"),
     ("Services Server", "FastEthernet0", "192.168.50.10 /24", "192.168.50.1"),
     ("Internet Server", "FastEthernet0", "198.51.100.10 /24", "198.51.100.1")],
    [("ASW1", '''enable
configure terminal
hostname ASW1
spanning-tree mode rapid-pvst
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 50
 name SERVERS
vlan 99
 name MANAGEMENT
interface fastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security mac-address sticky
interface fastEthernet0/2
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
interface fastEthernet0/3
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
interface fastEthernet0/10
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
interface range gigabitEthernet0/1-2
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,50,99
end
copy running-config startup-config'''),
     ("MLS1", '''enable
configure terminal
hostname MLS1
ip routing
spanning-tree mode rapid-pvst
vlan 10
vlan 20
vlan 30
vlan 50
vlan 99
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,50,99
interface gigabitEthernet0/2
 no switchport
 ip address 10.0.1.1 255.255.255.252
 no shutdown
interface vlan 10
 ip address 192.168.10.2 255.255.255.0
 standby 10 ip 192.168.10.1
 standby 10 priority 110
 standby 10 preempt
 ip helper-address 192.168.50.10
 no shutdown
interface vlan 20
 ip address 192.168.20.2 255.255.255.0
 standby 20 ip 192.168.20.1
 standby 20 priority 110
 standby 20 preempt
 ip helper-address 192.168.50.10
 no shutdown
interface vlan 30
 ip address 192.168.30.2 255.255.255.0
 standby 30 ip 192.168.30.1
 standby 30 priority 110
 standby 30 preempt
 ip helper-address 192.168.50.10
 no shutdown
interface vlan 50
 ip address 192.168.50.2 255.255.255.0
 standby 50 ip 192.168.50.1
 standby 50 priority 110
 standby 50 preempt
 no shutdown
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 standby 99 ip 192.168.99.1
 standby 99 priority 110
 standby 99 preempt
 no shutdown
spanning-tree vlan 10,20,30,50,99 root primary
router ospf 1
 router-id 1.1.1.1
 network 10.0.1.0 0.0.0.3 area 0
 network 192.168.10.0 0.0.0.255 area 0
 network 192.168.20.0 0.0.0.255 area 0
 network 192.168.30.0 0.0.0.255 area 0
 network 192.168.50.0 0.0.0.255 area 0
 network 192.168.99.0 0.0.0.255 area 0
 passive-interface default
 no passive-interface gigabitEthernet0/2
ntp server 192.168.50.10
logging host 192.168.50.10
snmp-server community CAMPUS-RO ro
username netadmin privilege 15 secret AdminSSH!23
ip domain-name campus.lab
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config'''),
     ("MLS2", '''enable
configure terminal
hostname MLS2
ip routing
spanning-tree mode rapid-pvst
vlan 10
vlan 20
vlan 30
vlan 50
vlan 99
interface gigabitEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,50,99
interface gigabitEthernet0/2
 no switchport
 ip address 10.0.2.1 255.255.255.252
 no shutdown
interface vlan 10
 ip address 192.168.10.3 255.255.255.0
 standby 10 ip 192.168.10.1
 standby 10 priority 100
 standby 10 preempt
 ip helper-address 192.168.50.10
 no shutdown
interface vlan 20
 ip address 192.168.20.3 255.255.255.0
 standby 20 ip 192.168.20.1
 standby 20 priority 100
 standby 20 preempt
 ip helper-address 192.168.50.10
 no shutdown
interface vlan 30
 ip address 192.168.30.3 255.255.255.0
 standby 30 ip 192.168.30.1
 standby 30 priority 100
 standby 30 preempt
 ip helper-address 192.168.50.10
 no shutdown
interface vlan 50
 ip address 192.168.50.3 255.255.255.0
 standby 50 ip 192.168.50.1
 standby 50 priority 100
 standby 50 preempt
 no shutdown
interface vlan 99
 ip address 192.168.99.3 255.255.255.0
 standby 99 ip 192.168.99.1
 standby 99 priority 100
 standby 99 preempt
 no shutdown
spanning-tree vlan 10,20,30,50,99 root secondary
router ospf 1
 router-id 2.2.2.2
 network 10.0.2.0 0.0.0.3 area 0
 network 192.168.10.0 0.0.0.255 area 0
 network 192.168.20.0 0.0.0.255 area 0
 network 192.168.30.0 0.0.0.255 area 0
 network 192.168.50.0 0.0.0.255 area 0
 network 192.168.99.0 0.0.0.255 area 0
 passive-interface default
 no passive-interface gigabitEthernet0/2
ntp server 192.168.50.10
logging host 192.168.50.10
snmp-server community CAMPUS-RO ro
username netadmin privilege 15 secret AdminSSH!23
ip domain-name campus.lab
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config'''),
     ("EDGE1", '''enable
configure terminal
hostname EDGE1
interface gigabitEthernet0/0
 ip address 10.0.1.2 255.255.255.252
 ip nat inside
 no shutdown
interface gigabitEthernet0/1
 ip address 10.0.2.2 255.255.255.252
 ip nat inside
 no shutdown
interface gigabitEthernet0/2
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
 no shutdown
router ospf 1
 router-id 3.3.3.3
 network 10.0.1.0 0.0.0.3 area 0
 network 10.0.2.0 0.0.0.3 area 0
 default-information originate
exit
access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface gigabitEthernet0/2 overload
ip route 0.0.0.0 0.0.0.0 203.0.113.1
username netadmin privilege 15 secret AdminSSH!23
ip domain-name campus.lab
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
end
copy running-config startup-config'''),
     ("ISP", '''enable
configure terminal
hostname ISP
interface gigabitEthernet0/0
 ip address 203.0.113.1 255.255.255.252
 no shutdown
interface gigabitEthernet0/1
 ip address 198.51.100.1 255.255.255.0
 no shutdown
end
copy running-config startup-config''')],
    ["show interfaces trunk", "show spanning-tree root", "show standby brief", "show ip ospf neighbor", "show ip route", "show ip dhcp binding", "show ip nat translations", "show ntp associations", "show logging"],
    [("DHCP", "Each user PC", "Services Server", "Receives address from its own VLAN pool"),
     ("Gateway", "Each user PC", "Local HSRP .1", "Success"),
     ("Inter-VLAN", "Admin PC", "Staff and Student PCs", "Success unless later restricted by policy"),
     ("DNS", "Any PC", "www.campus.lab", "Resolves to 192.168.50.10"),
     ("Internet", "Any PC", "198.51.100.10", "Success through PAT"),
     ("Failover", "Admin PC continuous ping", "Shut MLS1 trunk/uplink", "Brief loss, then service through MLS2")],
    [("Clients receive no DHCP", "Pool, helper, trunk, VLAN, or server gateway mismatch", "Trace from access VLAN to SVI to 192.168.50.10"),
     ("OSPF neighbors absent", "Routed port, address, passive interface, or area issue", "Verify G0/2 on each core and both EDGE links"),
     ("Internet fails but campus works", "Default route, default advertisement, NAT role, or ACL issue", "Verify EDGE default route and NAT translations"),
     ("HSRP failover fails", "Layer 2 path or group mismatch", "Compare virtual IP, group, VLAN, and trunk state")],
    gui_steps=[("Configure the Services Server", "Set `192.168.50.10/24`, gateway `192.168.50.1`, DNS `192.168.50.10`. Create DHCP pools for VLAN10 (`192.168.10.100`, gateway `.1`), VLAN20, and VLAN30. Enable DNS A record `www.campus.lab` → `192.168.50.10`, HTTP, NTP, and Syslog services."),
               ("Configure the Internet Server", "Set `198.51.100.10/24`, gateway `198.51.100.1`, and enable HTTP."),
               ("Configure user PCs", "Select DHCP on each PC, confirm the correct VLAN lease, then work through the testing matrix in order.")],
    notes=["The integrated configuration deliberately uses local SSH and SNMPv2c for Packet Tracer compatibility. Upgrade to central AAA and SNMPv3 in a production design."]
)

# TOPICS END


def render_category_guide(code, name, topics):
    guide_title = category_guide_title(name)
    links = "\n".join(
        f"{index}. [[{topic['number']} - {topic['title']} - Step by Step]] — {topic['objective']}"
        for index, topic in enumerate(topics, 1)
    )
    return f'''---
title: "{guide_title}"
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

# {guide_title}

Complete these notes in order. Each guide includes a topology, addressing plan, exact device configuration, verification, testing, and troubleshooting.

{links}

Return to [[Configuration Library Dashboard]].
'''


def render_dashboard():
    sections = []
    for code, name in CATEGORIES.items():
        topic_count = sum(topic["category"] == code for topic in TOPICS)
        sections.append(
            f"## {code} — {name}\n\n"
            f"Open [[{category_guide_title(name)}]] for {topic_count} complete walkthroughs."
        )
    return f'''---
title: "Configuration Library Dashboard"
aliases:
  - "Step-by-Step Configuration Hub"
  - "Cisco Configuration Library"
category: "Dashboard"
difficulty: "Mixed"
packet_tracer_supported: "Mixed"
related_protocols: []
tags:
  - networking
  - cisco
  - packet-tracer
  - configuration
  - dashboard
---

# Configuration Library Dashboard

This folder is the dedicated hands-on configuration library. The original teaching notes and their code remain unchanged.

> [!tip] Recommended use
> Open one configuration guide, build its topology from an empty Packet Tracer file, enter each device block, verify the result, and then introduce one fault for troubleshooting practice.

## Naming Standard

Protocol notes use the short name and full name together, such as **OSPF — Open Shortest Path First** and **NTP — Network Time Protocol**.

{chr(10).join(sections)}

## Configuration Workflow

```mermaid
flowchart LR
    A["Build topology"] --> B["Apply addressing"]
    B --> C["Configure each device"]
    C --> D["Run show commands"]
    D --> E["Test end-to-end"]
    E --> F["Troubleshoot and save"]
```

## Completion Checklist

- [ ] Topology matches the guide
- [ ] Interfaces and cables are correct
- [ ] Addressing table is complete
- [ ] Every device configuration is entered
- [ ] Verification output is checked
- [ ] Testing matrix passes
- [ ] Running configurations are saved
'''


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    expected = set()
    for topic in TOPICS:
        category_dir = ROOT / f"{topic['category']} - {CATEGORIES[topic['category']]}"
        category_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{topic['number']} - {topic['title']} - Step by Step.md"
        path = category_dir / filename
        path.write_text(render_note(topic), encoding="utf-8")
        expected.add(path.resolve())

    for code, name in CATEGORIES.items():
        category_dir = ROOT / f"{code} - {name}"
        category_dir.mkdir(parents=True, exist_ok=True)
        category_topics = [topic for topic in TOPICS if topic["category"] == code]
        guide = category_dir / f"{category_guide_title(name)}.md"
        guide.write_text(render_category_guide(code, name, category_topics), encoding="utf-8")
        expected.add(guide.resolve())

    dashboard = ROOT / "Configuration Library Dashboard.md"
    dashboard.write_text(render_dashboard(), encoding="utf-8")
    expected.add(dashboard.resolve())

    print(f"Created {len(TOPICS)} complete configuration notes and {len(CATEGORIES)} category guides.")


if __name__ == "__main__":
    main()
