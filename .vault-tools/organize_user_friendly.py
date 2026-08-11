from pathlib import Path
import re

from expand_protocol_names import NOTE_RENAMES


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "Newroking"
DATE = "2026-08-11"


def fm(title: str, category: str, note_type: str = "navigation") -> str:
    return f"""---
title: "{title}"
category: "{category}"
difficulty: "Mixed"
packet_tracer_supported: "Mixed"
related_protocols: []
tags:
  - networking
  - navigation
  - teaching
type: "{note_type}"
status: "active"
created: "{DATE}"
updated: "{DATE}"
---"""


def link_list(items: list[tuple[str, str] | str]) -> str:
    lines = []
    for item in items:
        if isinstance(item, tuple):
            target = NOTE_RENAMES.get(item[0], item[0])
            lines.append(f"- [[{target}|{item[1]}]]")
        else:
            target = NOTE_RENAMES.get(item, item)
            lines.append(f"- [[{target}]]")
    return "\n".join(lines)


def write(relative: str, title: str, category: str, body: str) -> None:
    path = VAULT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    content = fm(title, category) + "\n\n" + f"# {title}\n\n" + body.strip() + "\n"
    path.write_text(content, encoding="utf-8", newline="\n")


DASHBOARD = f"""
> [!abstract]
> A simple front door to the complete networking teaching vault. Choose what you want to do rather than searching through hundreds of files.

## Choose Your Path

| I want to... | Open this |
|---|---|
| Learn networking in order | [[Student Dashboard]] |
| Prepare or teach a class | [[Lecturer Dashboard]] |
| Find a subject directly | [[Learn Dashboard]] |
| Complete a practical lab | [[Lab Dashboard]] |
| Find templates, commands, or questions | [[Teaching Toolkit Dashboard]] |
| Work on enterprise and advanced material | [[Advanced Projects Dashboard]] |

## Recommended First Steps

1. New student: [[Student Dashboard]]
2. New lecturer: [[Lecturer Dashboard]]
3. Returning user: [[Network Protocol Master Index]] or [[Lab Dashboard]]

## Five Main Areas

```text
00 - Start Here          Navigation and learning paths
01 - Learn               Concepts, configurations, and troubleshooting
02 - Practice Labs       All 30 numbered Packet Tracer labs
03 - Teaching Toolkit    Templates, cheat sheets, viva, and lesson tools
04 - Advanced Projects   Enterprise design and platform guidance
```

## Fast Links

- [[Networking Learning Roadmap]]
- [[Network Protocol Master Index]]
- [[Cisco Troubleshooting Cheat Sheet]]
- [[Networking Port Numbers Cheat Sheet]]
- [[Subnetting Cheat Sheet]]
- [[Lab 29 - Complete Enterprise Network]]
- [[Lab 30 - Network Troubleshooting Challenge]]
"""


STUDENT = f"""
> [!abstract]
> Follow one clear cycle: learn the idea, observe it, configure it, verify it, break it safely, and revise it.

## Your Study Cycle

```mermaid
flowchart LR
A[Learn] --> B[Draw] --> C[Configure] --> D[Verify] --> E[Troubleshoot] --> F[Revise]
```

## Start by Experience

### New to networking

1. [[Fundamentals Guide]]
2. [[Addressing and Subnetting Guide]]
3. [[Switching and VLANs Guide]]
4. [[Routing Guide]]

### Know the basics

1. [[Network Services Guide]]
2. [[Security Guide]]
3. [[High Availability Guide]]
4. [[Monitoring and Management Guide]]

### Preparing for practical assessment

1. Choose a topic in [[Learn Dashboard]].
2. Complete its numbered exercise in [[Lab Dashboard]].
3. Use [[Viva Questions Guide]].
4. Finish with [[Lab 30 - Network Troubleshooting Challenge]].

## Progress Checklist

- [ ] I can explain the purpose without commands.
- [ ] I can draw the traffic or protocol sequence.
- [ ] I can configure each device separately.
- [ ] I can prove it works with show commands and endpoint tests.
- [ ] I can diagnose one realistic fault.
"""


LECTURER = f"""
> [!abstract]
> Prepare a lesson from existing concepts, demonstrations, labs, question banks, and marking tools without rebuilding material.

## Build a Lesson in Five Steps

1. Select the subject from [[Learn Dashboard]].
2. Copy [[Lesson Plan Template]].
3. Choose a demonstration from [[Lab Dashboard]].
4. Select questions from [[Viva Questions Guide]].
5. Mark practical evidence with [[Assessment Rubric]].

## Classroom Resources

- [[Packet Tracer Demonstration Guide]]
- [[Student Exercise Design Guide]]
- [[Practical Examination Template]]
- [[Viva Session Guide]]
- [[Configuration Templates Guide]]
- [[Cheat Sheets Guide]]

## Recommended Teaching Pattern

```text
Problem -> Concept -> Diagram -> Configuration -> Verification -> Fault -> Revision
```

> [!tip]
> Keep the lecturer solution hidden until students submit their topology, configuration, and verification evidence.
"""


VAULT_GUIDE = """
> [!abstract]
> The vault uses a task-first layout with only five top-level folders.

## How Notes Are Organized

- **Start Here:** dashboards and learning maps.
- **Learn:** all subject knowledge grouped by how networking is taught.
- **Practice Labs:** one numbered collection from Lab 01 to Lab 30.
- **Teaching Toolkit:** reusable classroom artifacts.
- **Advanced Projects:** integrated enterprise work and platform guidance.

## Note Pattern

Major notes answer WHAT, WHY, WHERE, HOW, CONFIGURE, VERIFY, FAIL, and TROUBLESHOOT.

## Finding Anything

1. Use Quick Switcher and type the technology name.
2. Use [[Network Protocol Master Index]] when you know the protocol.
3. Use [[Learn Dashboard]] when you know the subject area.
4. Use [[Lab Dashboard]] when you want practical work.

## Link Rule

Wikilinks use unique note names, so notes can move between folders without breaking relationships.
"""


LEARN_AREAS = {
    "01 - Learn/01 - Fundamentals/Fundamentals Guide.md": (
        "Fundamentals Guide", "Networking Fundamentals",
        "Build the mental model needed for every later subject.",
        ["OSI Model", "TCP-IP Model", "Ethernet", "Ethernet Frame", "MAC Addressing", "ARP", "ICMP", "TCP", "UDP", "Common Network Ports", "Cisco Router Basic Configuration", "Cisco Switch Basic Configuration"]),
    "01 - Learn/02 - Internet Protocol (IP) Addressing and Subnetting/Addressing and Subnetting Guide.md": (
        "Addressing and Subnetting Guide", "IP Addressing and Subnetting",
        "Learn to design and validate IPv4 networks before configuring devices.",
        ["IPv4 Addressing", "Subnet Mask", "Default Gateway", "Network Address", "Broadcast Address", "CIDR", "Subnetting Basics", "Subnetting Step by Step", "VLSM", "Subnetting Practice Questions"]),
    "01 - Learn/03 - Switching and Virtual Local Area Networks (VLANs)/Switching and VLANs Guide.md": (
        "Switching and VLANs Guide", "Switching and VLANs",
        "Move from Ethernet switching through VLANs, trunks, loop prevention, link aggregation, and inter-VLAN routing.",
        ["VLAN", "VLAN Configuration", "802.1Q Trunking", "Trunk Configuration", "STP", "RSTP", "PortFast", "BPDU Guard", "EtherChannel", "LACP", "Router on a Stick", "Layer 3 Switch Inter-VLAN Routing"]),
    "01 - Learn/04 - Routing/Routing Guide.md": (
        "Routing Guide", "Routing",
        "Learn route selection from static routes through RIP, OSPF, and EIGRP.",
        ["Static Routing", "Default Route", "Floating Static Route", "RIP", "RIPv2 Configuration", "OSPF", "OSPF Single Area", "OSPF Multi Area", "OSPF Troubleshooting", "EIGRP", "RIP vs OSPF vs EIGRP"]),
    "01 - Learn/05 - Network Services/Network Services Guide.md": (
        "Network Services Guide", "Network Services",
        "Configure the services that give clients addresses, names, time, files, web access, and email.",
        ["DHCP", "Dedicated DHCP Server", "DHCP Relay", "DNS", "Packet Tracer DNS Server", "NTP", "Cisco NTP Configuration", "FTP", "TFTP", "HTTP", "HTTPS", "SMTP", "POP3", "IMAP"]),
    "01 - Learn/06 - High Availability/High Availability Guide.md": (
        "High Availability Guide", "High Availability",
        "Protect default gateways and understand first-hop redundancy choices.",
        ["HSRP", "HSRP Configuration", "HSRP Tracking", "HSRP Troubleshooting", "VRRP", "VRRP Configuration", "HSRP vs VRRP", "GLBP"]),
    "01 - Learn/07 - Security/Security Guide.md": (
        "Security Guide", "Network Security",
        "Secure device access, control traffic, translate addresses, and protect the access layer.",
        ["SSH", "Cisco SSH Configuration", "AAA", "RADIUS", "TACACS+", "ACL", "Standard ACL", "Extended ACL", "NAT", "PAT", "Switch Port Security", "DHCP Snooping", "Dynamic ARP Inspection", "IP Source Guard"]),
    "01 - Learn/08 - Monitoring and Management/Monitoring and Management Guide.md": (
        "Monitoring and Management Guide", "Monitoring and Management",
        "Collect time, state, events, neighbors, and packet evidence for network operations.",
        ["Network Monitoring", "SNMP", "SNMPv2c", "SNMPv3", "Cisco SNMP Configuration", "Syslog", "Cisco Syslog Configuration", "Syslog Severity Levels", "Wireshark", "Packet Capture", "CDP", "LLDP"]),
    "01 - Learn/09 - Wide Area Networks (WAN), Virtual Private Networks (VPN), and Wireless/WAN VPN and Wireless Guide.md": (
        "WAN VPN and Wireless Guide", "WAN VPN and Wireless",
        "Connect remote networks and users across serial, tunnel, encrypted, and wireless links.",
        ["VPN", "Site-to-Site VPN", "Remote Access VPN", "IPsec", "GRE Tunnel", "GRE over IPsec", "PPP", "PPP CHAP", "HDLC", "Wireless Networking", "Wi-Fi Standards", "WPA2", "WPA3"]),
    "01 - Learn/10 - Internet Protocol Version 6 (IPv6)/IPv6 Guide.md": (
        "IPv6 Guide", "IPv6",
        "Learn IPv6 addressing, neighbor discovery, automatic configuration, routing, and troubleshooting.",
        ["IPv6", "IPv6 Address Types", "IPv6 Static Routing", "IPv6 SLAAC", "DHCPv6", "IPv6 OSPFv3", "IPv6 Troubleshooting"]),
    "01 - Learn/11 - Troubleshooting/Troubleshooting Guide.md": (
        "Troubleshooting Guide", "Troubleshooting",
        "Use a repeatable evidence-based method and targeted symptom guides.",
        ["Network Troubleshooting Methodology", "Cisco Troubleshooting Method", "OSI Troubleshooting", "Cisco Troubleshooting Commands", "PC Cannot Get DHCP Address", "PC Cannot Ping Gateway", "VLAN Communication Failure", "OSPF Neighbour Not Forming", "ACL Blocking Traffic", "NAT Not Working", "DNS Resolution Failure", "NTP Not Synchronising"]),
}


def guide_body(summary: str, items: list[str]) -> str:
    return f"""> [!abstract]
> {summary}

## Recommended Order

{link_list(items)}

## Study Pattern

1. Read the overview.
2. Draw the packet path or state transition.
3. Open the related configuration note.
4. Complete the matching lab from [[Lab Dashboard]].
5. Use [[Viva Questions Guide]] and a troubleshooting note for revision.

## Navigation

- [[Learn Dashboard]]
- [[Student Dashboard]]
- [[Networking Dashboard]]
"""


def lab_links(start: int, end: int) -> str:
    names = {}
    for path in (VAULT / "02 - Practice Labs").glob("Lab *.md"):
        match = re.match(r"Lab (\d+) - ", path.stem)
        if match:
            names[int(match.group(1))] = path.stem
    return "\n".join(f"{number}. [[{names[number]}]]" for number in range(start, end + 1) if number in names)


def main() -> None:
    write("00 - Start Here/Networking Dashboard.md", "Networking Dashboard", "Start Here", DASHBOARD)
    write("00 - Start Here/Student Dashboard.md", "Student Dashboard", "Start Here", STUDENT)
    write("00 - Start Here/Lecturer Dashboard.md", "Lecturer Dashboard", "Start Here", LECTURER)
    write("00 - Start Here/Vault Guide.md", "Vault Guide", "Start Here", VAULT_GUIDE)

    learn_sections = [(data[0], data[2]) for data in LEARN_AREAS.values()]
    learn_body = "> [!abstract]\n> Choose a subject area. Each guide gives a recommended order and connects theory to configuration, labs, viva, and troubleshooting.\n\n## Learning Areas\n\n" + "\n".join(f"- [[{title}]] - {summary}" for title, summary in learn_sections) + "\n\n## Full Sequence\n\n- [[Networking Learning Roadmap]]\n- [[Network Protocol Master Index]]\n"
    write("01 - Learn/Learn Dashboard.md", "Learn Dashboard", "Learn", learn_body)
    for relative, (title, category, summary, items) in LEARN_AREAS.items():
        write(relative, title, category, guide_body(summary, items))

    lab_body = f"""> [!abstract]
> All Packet Tracer work is kept in one numbered sequence. Use the first group for foundations, the middle groups for implementation, and the final group for integration.

## Foundation Labs

{lab_links(1, 10)}

## Services, Management, and Security

{lab_links(11, 19)}

## Switching, Redundancy, and Modern Networks

{lab_links(20, 28)}

## Capstone Labs

{lab_links(29, 30)}

## Before You Begin

- Read the matching subject note in [[Learn Dashboard]].
- Copy the relevant file from [[Configuration Templates Guide]].
- Record results with [[Testing Matrix Template]].
"""
    write("02 - Practice Labs/Lab Dashboard.md", "Lab Dashboard", "Practice Labs", lab_body)

    toolkit_body = """> [!abstract]
> Reusable material for faster lesson preparation, classroom delivery, revision, and assessment.

## Toolkit Areas

- [[Configuration Templates Guide]] - reusable Cisco IOS skeletons.
- [[Cheat Sheets Guide]] - compact classroom references.
- [[Viva Questions Guide]] - 23 question banks with three difficulty levels.
- [[Teaching Materials Guide]] - lesson, examination, demonstration, and marking tools.
"""
    write("03 - Teaching Toolkit/Teaching Toolkit Dashboard.md", "Teaching Toolkit Dashboard", "Teaching Toolkit", toolkit_body)

    config_items = sorted(path.stem for path in (VAULT / "03 - Teaching Toolkit/01 - Configuration Templates").glob("*.md") if path.stem != "Configuration Templates Guide")
    write("03 - Teaching Toolkit/01 - Configuration Templates/Configuration Templates Guide.md", "Configuration Templates Guide", "Configuration Templates", "> [!abstract]\n> Copy a template, replace every placeholder, validate interfaces and addressing, then verify before saving.\n\n## Templates\n\n" + link_list(config_items))
    cheat_items = sorted(path.stem for path in (VAULT / "03 - Teaching Toolkit/02 - Cheat Sheets").glob("*.md") if path.stem != "Cheat Sheets Guide")
    write("03 - Teaching Toolkit/02 - Cheat Sheets/Cheat Sheets Guide.md", "Cheat Sheets Guide", "Cheat Sheets", "> [!abstract]\n> Quick references for commands, ports, switching, routing, security, troubleshooting, and subnetting.\n\n## Cheat Sheets\n\n" + link_list(cheat_items))
    viva_items = sorted(path.stem for path in (VAULT / "03 - Teaching Toolkit/03 - Viva Questions").glob("*.md") if path.stem != "Viva Questions Guide")
    write("03 - Teaching Toolkit/03 - Viva Questions/Viva Questions Guide.md", "Viva Questions Guide", "Viva Questions", "> [!abstract]\n> Every bank contains 10 beginner, 10 intermediate, and 5 advanced questions with answers.\n\n## Question Banks\n\n" + link_list(viva_items))
    teaching_items = sorted(path.stem for path in (VAULT / "03 - Teaching Toolkit/04 - Teaching Materials").glob("*.md") if path.stem != "Teaching Materials Guide")
    write("03 - Teaching Toolkit/04 - Teaching Materials/Teaching Materials Guide.md", "Teaching Materials Guide", "Teaching Materials", "> [!abstract]\n> Tools for lesson planning, demonstrations, exercises, practical examinations, viva sessions, and assessment.\n\n## Teaching Tools\n\n" + link_list(teaching_items))

    advanced_items = sorted(path.stem for path in (VAULT / "04 - Advanced Projects").glob("*.md") if path.stem != "Advanced Projects Dashboard")
    advanced_body = "> [!abstract]\n> Integrated design, platform selection, and capstone work.\n\n## Advanced Notes\n\n" + link_list(advanced_items) + "\n\n## Capstones\n\n- [[Lab 29 - Complete Enterprise Network]]\n- [[Lab 30 - Network Troubleshooting Challenge]]\n"
    write("04 - Advanced Projects/Advanced Projects Dashboard.md", "Advanced Projects Dashboard", "Advanced Projects", advanced_body)

    replacements = {
        "Index - Viva and Revision Questions": "Viva Questions Guide",
        "Index - Packet Tracer Labs": "Lab Dashboard",
        "Index - Configuration Templates": "Configuration Templates Guide",
        "Index - Commands Cheat Sheets": "Cheat Sheets Guide",
        "Index - Teaching Materials": "Teaching Materials Guide",
    }
    for path in VAULT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            content = content.replace(f"[[{old}", f"[[{new}")
        path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")

    print("Created user-friendly dashboards and subject guides.")


if __name__ == "__main__":
    main()
