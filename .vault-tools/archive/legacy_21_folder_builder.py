from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
import textwrap


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "Newroking"
TODAY = "2026-08-11"

FOLDERS = [
    "00 - Dashboard",
    "01 - Networking Fundamentals",
    "02 - IP Addressing and Subnetting",
    "03 - Switching",
    "04 - VLAN and Trunking",
    "05 - Inter-VLAN Routing",
    "06 - Routing Protocols",
    "07 - DHCP and Network Services",
    "08 - Redundancy and High Availability",
    "09 - Network Security",
    "10 - Network Management and Monitoring",
    "11 - WAN and VPN",
    "12 - Wireless Networking",
    "13 - IPv6",
    "14 - Troubleshooting",
    "15 - Packet Tracer Labs",
    "16 - Configuration Templates",
    "17 - Commands Cheat Sheets",
    "18 - Viva and Revision Questions",
    "19 - Teaching Materials",
    "20 - Advanced Networking",
]


@dataclass
class Topic:
    folder: str
    title: str
    summary: str
    points: list[str] = field(default_factory=list)
    difficulty: str = "Beginner"
    support: str = "Yes"
    layer: str = "Varies"
    ports: str = "Not applicable"
    protocol_number: str = "Not applicable"
    related: list[str] = field(default_factory=list)
    commands: str = ""
    verify: list[str] = field(default_factory=list)
    diagram: str = ""


def clean(value: str) -> str:
    value = textwrap.dedent(value).strip()
    # Interpolated multiline values can prevent dedent from seeing the template's
    # common four-space source indentation. Remove that one template level while
    # preserving one- and two-space Cisco/YAML indentation.
    return re.sub(r"(?m)^ {4}", "", value)


def topic(folder: str, title: str, summary: str, points: str = "", **kwargs) -> Topic:
    parsed = [item.strip() for item in points.split("|") if item.strip()]
    return Topic(folder=folder, title=title, summary=summary, points=parsed, **kwargs)


def yaml_scalar(value: str) -> str:
    if not value:
        return '""'
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def frontmatter(title: str, category: str, difficulty: str, support: str,
                related: list[str], tags: list[str], note_type: str = "reference") -> str:
    lines = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"category: {yaml_scalar(category)}",
        f"difficulty: {yaml_scalar(difficulty)}",
        f"packet_tracer_supported: {yaml_scalar(support)}",
    ]
    if related:
        lines.append("related_protocols:")
        lines.extend(f'  - "[[{name}]]"' for name in related)
    else:
        lines.append("related_protocols: []")
    lines.append("tags:")
    lines.extend(f"  - {tag}" for tag in tags)
    lines.extend([
        f"type: {yaml_scalar(note_type)}",
        'status: "active"',
        f'created: "{TODAY}"',
        f'updated: "{TODAY}"',
        "---",
    ])
    return "\n".join(lines)


def tags_for(folder: str, title: str) -> list[str]:
    tags = ["networking", "teaching"]
    folder_tags = {
        "01": "fundamentals", "02": "subnetting", "03": "switching",
        "04": "switching", "05": "routing", "06": "routing",
        "07": "network-services", "08": "high-availability",
        "09": "security", "10": "monitoring", "11": "wan",
        "12": "wireless", "13": "ipv6", "14": "troubleshooting",
        "15": "lab", "16": "configuration-template",
        "17": "cheat-sheet", "18": "viva", "19": "teaching",
        "20": "advanced",
    }
    tags.append(folder_tags.get(folder[:2], "reference"))
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if slug in {"ospf", "dhcp", "stp", "hsrp", "snmp", "syslog", "ntp", "ipv6"}:
        tags.append(slug)
    return list(dict.fromkeys(tags))


def render_topic(spec: Topic) -> str:
    category = spec.folder.split(" - ", 1)[-1]
    points = spec.points or [
        f"Identify the devices and information involved in {spec.title}.",
        "Follow the traffic or control-message sequence from source to destination.",
        "Verify the result before adding complexity or security controls.",
    ]
    point_lines = "\n".join(f"{index}. {point}" for index, point in enumerate(points, 1))
    terms = "\n".join(f"- **Key idea {index}:** {point}" for index, point in enumerate(points[:5], 1))
    related_links = "\n".join(f"- [[{name}]]" for name in spec.related) or "- [[Networking Dashboard]]"
    verify = "\n".join(f"- `{command}`" for command in spec.verify) or "- Confirm the expected state at every participating device."
    config_section = ""
    if spec.commands:
        config_section = clean(f"""
        ## 12. Step-by-Step Configuration

        > [!note]
        > Interface names are examples. Confirm the actual Packet Tracer device interfaces before applying the configuration.

        ```cisco
        {clean(spec.commands)}
        ```

        Save IOS configurations with:

        ```cisco
        end
        copy running-config startup-config
        ```
        """)
    else:
        config_section = clean(f"""
        ## 12. Configuration or Demonstration

        This focused note explains one part of the subject. Use the related configuration note or Packet Tracer lab for device-by-device commands. For a theory-only topic, demonstrate the behavior with Packet Tracer Simulation Mode or Wireshark rather than inventing an IOS configuration.
        """)
    diagram = ""
    if spec.diagram:
        diagram = clean(f"""
        ## 7. Process Diagram

        ```mermaid
        {clean(spec.diagram)}
        ```
        """)
    support_note = {
        "Yes": "Packet Tracer can demonstrate the essential behavior in this note.",
        "Partial": "Packet Tracer demonstrates only part of this technology. Use Wireshark, GNS3, EVE-NG, Cisco CML, Linux, or real hardware for missing behavior.",
        "No": "Packet Tracer is not an adequate implementation environment. Use GNS3, EVE-NG, Cisco CML, Linux, Wireshark, or real hardware.",
    }.get(spec.support, "Confirm support in the selected platform and image.")
    return frontmatter(spec.title, category, spec.difficulty, spec.support, spec.related,
                       tags_for(spec.folder, spec.title)) + "\n\n" + clean(f"""
    # {spec.title}

    > [!abstract]
    > {spec.summary}

    > [!info] Packet Tracer Support: {spec.support}
    > {support_note}

    ## 1. What Is It?

    {spec.summary}

    ## 2. Why Do We Use It?

    It gives engineers a defined method to build, operate, verify, or troubleshoot this part of a network. Students should connect the concept to observable frames, packets, device state, and user impact.

    ## 3. Where Is It Used?

    It is used in {category.lower()} designs, Cisco IOS teaching labs, operational verification, and fault isolation. The exact platform support depends on the selected switch, router, server, or endpoint.

    ## 4. How It Works

    {point_lines}

    ## 5. Important Terminology

    {terms}

    ## 6. Technical Classification

    | Item | Value |
    |---|---|
    | OSI layer | {spec.layer} |
    | Port numbers | {spec.ports} |
    | IP protocol number | {spec.protocol_number} |
    | Packet Tracer support | {spec.support} |

    {diagram}

    ## 8. Advantages

    - Provides a standard and repeatable operational method.
    - Improves visibility, interoperability, availability, or control when designed correctly.
    - Can be verified with explicit state, counters, messages, or packet captures.

    ## 9. Limitations and Risks

    - Incorrect addressing, interface state, VLAN membership, timers, or policy can prevent operation.
    - Packet Tracer may omit advanced features or detailed debug output.
    - Security and scale requirements are greater in production than in a classroom lab.

    ## 10. Requirements

    - A documented topology and addressing plan.
    - Correct device and interface capabilities.
    - Baseline connectivity before advanced configuration.
    - A verification and rollback plan.

    ## 11. Practical Topology

    ```text
    Source/Client ---- Network Device(s) ---- Destination/Service
            |                 |
            +------ verification points -----+
    ```

    {config_section}

    ## 13. Verification Commands

    {verify}

    ## 14. Expected Result

    The intended adjacency, route, service, security policy, or forwarding state should be visible in verification output and confirmed with an end-to-end test.

    ## 15. Testing Procedure

    1. Verify cabling and interface state.
    2. Verify Layer 2 membership and forwarding where applicable.
    3. Verify IP addressing and routing.
    4. Verify the technology-specific state or service.
    5. Test from an endpoint.
    6. Introduce one controlled failure and confirm the expected response.

    ## 16. Troubleshooting

    | Check | Expected | Typical fix |
    |---|---|---|
    | Physical/interface state | Required interfaces are up | Correct cable, module, interface, or `no shutdown` |
    | Addressing or VLAN | Matches the design table | Correct address, mask, gateway, VLAN, or trunk list |
    | Protocol/service state | Required relationship is established | Correct peer, timer, process, server, or policy |
    | End-to-end test | Expected traffic succeeds | Follow the path and isolate the first failing hop |

    ## 17. Common Errors

    - Applying a correct command to the wrong device or interface.
    - Using an address, mask, wildcard, VLAN, or next hop that does not match the plan.
    - Testing an advanced feature before baseline connectivity works.
    - Assuming Packet Tracer supports every production IOS command.

    ## 18. Security Considerations

    Use least privilege, authenticated management, trusted peers, restricted infrastructure access, and logging. Replace classroom passwords, community strings, and shared keys before production use.

    ## 19. Student Exercise

    ### Beginner

    Draw the message or forwarding path and identify every device, address, interface, and verification point.

    ### Intermediate

    Build a small Packet Tracer topology and prove the expected behavior with at least two verification commands.

    ### Advanced

    Introduce one realistic fault, diagnose it without deleting the configuration, repair it, and document the evidence.

    ## 20. Viva Questions

    1. What problem does {spec.title} solve?
    2. Which device state or packet exchange proves it is working?
    3. What is the most likely configuration error in a Packet Tracer lab?
    4. What additional control would be required in production?

    ## 21. Quick Revision

    - **What:** {spec.summary}
    - **Why:** To produce predictable, verifiable network behavior.
    - **Verify:** Inspect the relevant interface, table, adjacency, service, or policy and then run an end-to-end test.
    - **Troubleshoot:** Start with physical state and follow the path upward through the OSI model.

    ## 22. Lecturer Notes

    - Start with the user-visible problem before introducing commands.
    - Draw the packet or control-message path and ask students to predict the next step.
    - Demonstrate one correct build and one deliberately broken build.
    - Common Packet Tracer mistakes are wrong interfaces, missing `no shutdown`, mismatched VLANs, and premature testing.

    ## 23. Related Notes

    {related_links}
    """) + "\n"


def write(path: Path, content: str, overwrite: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


TOPICS: list[Topic] = []


def add(folder: str, title: str, summary: str, points: str = "", **kwargs) -> None:
    TOPICS.append(topic(folder, title, summary, points, **kwargs))


# Networking fundamentals
F = "01 - Networking Fundamentals"
add(F, "OSI Model", "The OSI model divides network communication into seven layers so functions and faults can be discussed consistently.", "Physical transmits bits through media|Data Link frames local traffic and uses MAC addresses|Network routes packets with logical addresses|Transport provides end-to-end delivery|Session manages conversations|Presentation transforms and protects data|Application provides user-facing network services", related=["TCP-IP Model", "OSI Troubleshooting Method"], diagram="flowchart TB\nL7[Application] --> L6[Presentation] --> L5[Session] --> L4[Transport] --> L3[Network] --> L2[Data Link] --> L1[Physical]")
add(F, "OSI Troubleshooting Method", "The OSI troubleshooting method isolates faults by testing one layer at a time instead of changing unrelated settings.", "Check power cable and link at Layer 1|Check VLAN MAC and framing at Layer 2|Check IP gateway and routing at Layer 3|Check ports and sessions at Layer 4|Check applications and names at upper layers", related=["OSI Model", "Network Troubleshooting Methodology"])
add(F, "TCP-IP Model", "The TCP/IP model groups real-world networking functions into Network Access, Internet, Transport, and Application layers.", "Network Access moves frames on the local medium|Internet uses IP to deliver packets between networks|Transport uses TCP or UDP between applications|Application contains user and infrastructure services", related=["OSI Model", "OSI vs TCP-IP"])
add(F, "OSI vs TCP-IP", "OSI is a seven-layer reference model while TCP/IP is the practical four-layer architecture used by Internet protocols.", "OSI separates Session and Presentation functions|TCP-IP combines upper-layer functions into Application|Both provide a layered troubleshooting vocabulary", related=["OSI Model", "TCP-IP Model"])
add(F, "Ethernet", "Ethernet defines common wired LAN framing, MAC addressing, link operation, and media behavior.", "Endpoints and switches exchange Ethernet frames|Switches learn source MAC addresses|Destination MAC addresses control local forwarding", layer="Layer 1 and Layer 2", related=["Ethernet Frame", "MAC Addressing"])
add(F, "Ethernet Frame", "An Ethernet frame carries a Layer 3 packet across one local Layer 2 segment.", "Preamble and SFD synchronize reception|Destination and source MAC addresses identify the local hop|EtherType identifies the payload|FCS detects corruption", layer="Layer 2", related=["Ethernet", "MAC Addressing"])
add(F, "MAC Addressing", "A MAC address identifies a network interface for local Ethernet delivery.", "A 48-bit address is written in hexadecimal|The first portion identifies the vendor assignment|Switches build MAC tables from source addresses", layer="Layer 2", related=["Ethernet Frame", "ARP"])
add(F, "Unicast", "Unicast communication sends a frame or packet from one source to one destination.", "The destination identifies one receiver|Switches forward known unicast frames toward one port|Routers forward unicast packets using route tables", related=["Broadcast", "Multicast"])
add(F, "Broadcast", "Broadcast communication targets every host in one broadcast domain.", "Ethernet broadcast uses FF:FF:FF:FF:FF:FF|Routers do not normally forward Layer 2 broadcasts|ARP and DHCP use broadcasts during discovery", related=["Broadcast Domain", "ARP", "DHCP DORA Process"])
add(F, "Multicast", "Multicast delivers one stream to a selected group of interested receivers.", "Senders address a group rather than each receiver|Network devices replicate traffic only where required|Control protocols also use reserved multicast groups", related=["Unicast", "Broadcast"])
add(F, "Collision Domain", "A collision domain is a shared Ethernet region where simultaneous half-duplex transmissions can interfere.", "A switch creates one collision domain per port|Hubs place all ports in one collision domain|Full-duplex switched Ethernet removes collisions", related=["CSMA-CD", "Full Duplex"])
add(F, "Broadcast Domain", "A broadcast domain is the set of devices that receive the same Layer 2 broadcast.", "One VLAN normally equals one broadcast domain|Routers and Layer 3 interfaces separate domains|Large domains increase broadcast scope", related=["VLAN", "Broadcast"])
add(F, "CSMA-CD", "CSMA/CD is the legacy half-duplex Ethernet method for detecting and recovering from collisions.", "Listen before transmitting|Detect a collision while sending|Send a jam signal and back off randomly|Retry after the timer", layer="Layer 2", related=["Half Duplex", "Collision Domain"])
add(F, "Full Duplex", "Full duplex allows simultaneous transmission and reception on a point-to-point Ethernet link.", "Separate transmit and receive paths operate concurrently|Collisions do not occur|Both ends must negotiate or be configured compatibly", related=["Half Duplex", "Auto Negotiation"])
add(F, "Half Duplex", "Half duplex allows transmission in only one direction at a time and uses collision handling on shared Ethernet.", "Only one station transmits at a time|Collisions reduce performance|Modern switched networks normally use full duplex", related=["Full Duplex", "CSMA-CD"])
add(F, "Auto Negotiation", "Ethernet auto-negotiation lets link partners select compatible speed and duplex settings.", "Partners advertise capabilities|The highest common mode is selected|A mismatch can cause errors and poor performance", related=["Full Duplex", "Cisco Troubleshooting Commands"])
add(F, "ARP", "ARP resolves an IPv4 address to a local Ethernet MAC address.", "The sender checks its ARP cache|An ARP request is broadcast|The owner sends a unicast ARP reply|The mapping is cached temporarily", layer="Layer 2/Layer 3 boundary", related=["MAC Addressing", "IPv4 Addressing", "Dynamic ARP Inspection"], verify=["arp -a", "show arp", "show ip arp"], diagram="sequenceDiagram\nPC1->>LAN: Broadcast ARP request\nLAN->>PC2: Who has the target IPv4 address?\nPC2-->>PC1: Unicast ARP reply with MAC address")
add(F, "ICMP", "ICMP reports IP-layer status and errors and supports tools such as ping and traceroute.", "Echo request tests reachability|Echo reply confirms a response|Destination unreachable reports a delivery problem|Time exceeded supports hop discovery", layer="Layer 3", protocol_number="1 for IPv4", related=["IPv4 Addressing", "Cisco Troubleshooting Commands"], verify=["ping <destination>", "traceroute <destination>", "tracert <destination>"])
add(F, "TCP", "TCP provides reliable, ordered, connection-oriented transport between applications.", "SYN starts a connection|SYN-ACK acknowledges and synchronizes|ACK completes the three-way handshake|Sequence numbers acknowledgements and windows manage delivery", layer="Layer 4", protocol_number="6", related=["UDP", "TCP vs UDP"], diagram="sequenceDiagram\nClient->>Server: SYN\nServer-->>Client: SYN-ACK\nClient->>Server: ACK")
add(F, "UDP", "UDP provides connectionless transport with low overhead and no built-in delivery guarantee.", "No handshake is required|Datagrams are independent|Applications add reliability when needed|Useful for real-time and simple request-response services", layer="Layer 4", protocol_number="17", related=["TCP", "TCP vs UDP"])
add(F, "TCP vs UDP", "TCP prioritizes reliable ordered delivery while UDP prioritizes simplicity and low overhead.", "TCP establishes a session and retransmits loss|UDP sends independent datagrams|The application requirement determines the transport", layer="Layer 4", related=["TCP", "UDP", "Common Network Ports"])
add(F, "Common Network Ports", "Well-known port numbers identify common application and infrastructure services.", "Servers listen on known destination ports|Clients normally use temporary source ports|TCP and UDP port spaces are separate", layer="Layer 4", related=["TCP", "UDP", "Networking Port Numbers Cheat Sheet"])
add(F, "CDP", "Cisco Discovery Protocol advertises Cisco device identity, platform, port, and addressing information to directly connected neighbors.", "CDP operates only on the local link|Cisco devices periodically advertise information|Neighbor tables assist topology discovery", layer="Layer 2", support="Yes", related=["LLDP", "CDP vs LLDP"], verify=["show cdp neighbors", "show cdp neighbors detail"])
add(F, "LLDP", "Link Layer Discovery Protocol is a vendor-neutral method for discovering directly connected network devices.", "Enable LLDP globally where required|Devices advertise chassis port and capability data|Neighbor information stays on the local link", layer="Layer 2", support="Partial", related=["CDP", "CDP vs LLDP"], commands="enable\nconfigure terminal\nlldp run", verify=["show lldp neighbors", "show lldp neighbors detail"])
add(F, "CDP vs LLDP", "CDP is Cisco proprietary while LLDP is the IEEE vendor-neutral discovery protocol.", "Both discover directly connected neighbors|CDP is common in Cisco-only labs|LLDP improves multi-vendor interoperability", layer="Layer 2", related=["CDP", "LLDP"])
add(F, "Cisco Router Basic Configuration", "A baseline router configuration establishes identity, secure administration, interface state, and saved startup configuration.", "Set hostname and protected secrets|Configure management access|Address required interfaces|Verify and save", related=["Cisco SSH Configuration", "Cisco Troubleshooting Commands"], commands="enable\nconfigure terminal\nhostname R1\nenable secret <ENABLE-SECRET>\nservice password-encryption\nbanner motd #Authorized Access Only#\nusername admin privilege 15 secret <ADMIN-SECRET>\nline console 0\n login local\nexit\nline vty 0 4\n login local\n transport input ssh\nexit", verify=["show running-config", "show ip interface brief"])
add(F, "Cisco Switch Basic Configuration", "A baseline switch configuration establishes device identity, secure management, access ports, and saved configuration.", "Set hostname and credentials|Create a management VLAN and SVI|Configure the default gateway on Layer 2 switches|Verify ports and save", related=["VLAN Configuration", "Cisco SSH Configuration"], commands="enable\nconfigure terminal\nhostname SW1\nenable secret <ENABLE-SECRET>\nservice password-encryption\nusername admin privilege 15 secret <ADMIN-SECRET>\ninterface vlan <MANAGEMENT-VLAN>\n ip address <SWITCH-IP> <SUBNET-MASK>\n no shutdown\nexit\nip default-gateway <GATEWAY>", verify=["show ip interface brief", "show vlan brief"])
add(F, "Cisco Multilayer Switch Configuration", "A multilayer switch combines VLAN switching with routed SVIs or routed physical ports.", "Create VLANs|Configure SVIs or routed ports|Enable IP routing|Verify routes and reachability", difficulty="Intermediate", related=["Multilayer Switch Routing", "SVI Routing"], commands="enable\nconfigure terminal\nhostname MLS1\nip routing\nvlan <VLAN-ID>\n name <VLAN-NAME>\ninterface vlan <VLAN-ID>\n ip address <GATEWAY> <SUBNET-MASK>\n no shutdown", verify=["show ip interface brief", "show ip route"])


# IPv4 addressing and subnetting
F = "02 - IP Addressing and Subnetting"
add(F, "IPv4 Addressing", "IPv4 uses 32-bit logical addresses and prefix lengths to identify networks and hosts.", "Separate network and host portions with the mask|Use unique host addresses in each subnet|Route packets between different subnets", layer="Layer 3", related=["Subnet Mask", "CIDR", "Default Gateway"])
add(F, "Public vs Private IP", "Public IPv4 addresses are globally routable while RFC 1918 private addresses require translation for public Internet access.", "Private ranges are 10/8 172.16/12 and 192.168/16|Public addresses require allocation|NAT commonly translates private clients", related=["IPv4 Addressing", "NAT"])
add(F, "Classful Addressing", "Classful addressing is the historical A, B, and C network model that was replaced by classless CIDR.", "Class A used default /8|Class B used /16|Class C used /24|Modern routing carries explicit prefix lengths", related=["CIDR", "IPv4 Addressing"])
add(F, "CIDR", "CIDR uses variable prefix lengths such as /24 or /27 instead of fixed address classes.", "The prefix counts network bits|Shorter prefixes contain more addresses|CIDR enables aggregation and efficient allocation", related=["Subnet Mask", "VLSM"])
add(F, "Subnet Mask", "A subnet mask marks the network bits and host bits of an IPv4 address.", "Binary 1 bits identify the network portion|Binary 0 bits identify the host portion|The mask determines local versus remote delivery", related=["CIDR", "Network Address"])
add(F, "Default Gateway", "A default gateway is the local router address an endpoint uses for destinations outside its subnet.", "The endpoint compares the destination with its mask|Local traffic is sent directly|Remote traffic is framed toward the gateway MAC", related=["ARP", "PC Cannot Ping Gateway"])
add(F, "Network Address", "The network address identifies an IPv4 subnet and has every host bit set to zero.", "Apply a bitwise AND between address and mask|Do not assign the network address to a host|Routes normally reference network prefixes", related=["Broadcast Address", "Subnetting Step by Step"])
add(F, "Broadcast Address", "The directed broadcast address is the last address in an IPv4 subnet with every host bit set to one.", "It targets all hosts in the subnet|It is not assigned to an endpoint|Routers normally restrict directed broadcasts", related=["Network Address", "Broadcast"])
add(F, "Subnetting Basics", "Subnetting borrows host bits to create smaller IPv4 networks with controlled size and broadcast scope.", "Choose the required number of subnets or hosts|Select a prefix length|Find the block size|Calculate network broadcast and usable range", related=["Subnetting Step by Step", "Subnetting Cheat Sheet"])
add(F, "Subnetting Step by Step", "A repeatable subnetting method calculates network, broadcast, first host, last host, and capacity from an address and prefix.", "Convert the prefix to a mask|Identify the interesting octet|Calculate block size as 256 minus the mask value|Locate the address inside its block|Derive usable boundaries", related=["Subnetting Basics", "VLSM"])
add(F, "VLSM", "Variable Length Subnet Masking assigns different prefix lengths to subnets according to their host requirements.", "Sort requirements from largest to smallest|Allocate the largest block first|Continue from the next unused network boundary|Document unused space", difficulty="Intermediate", related=["CIDR", "Subnetting Practice Questions"])
add(F, "Subnetting Practice Questions", "This exercise bank practices /23, /24, /27, /28, /30, and VLSM calculations.", "Calculate 192.168.1.0/27 ranges|Find the subnet containing 172.16.20.140/23|Divide 200.100.10.0/24 into /28 blocks|Design VLSM for 100 50 25 and 10 hosts", related=["Subnetting Step by Step", "Subnetting Cheat Sheet"])


# VLAN and switching topics
F = "04 - VLAN and Trunking"
add(F, "VLAN", "A VLAN creates a logical Layer 2 broadcast domain on a switch infrastructure.", "Assign a VLAN ID and name|Place access ports into one VLAN|Carry multiple VLANs across trunks|Route between VLANs with Layer 3 interfaces", layer="Layer 2", related=["VLAN Configuration", "802.1Q Trunking"])
add(F, "VLAN Configuration", "Cisco IOS VLAN configuration creates broadcast domains and assigns endpoint access ports.", "Create VLANs before assigning ports|Set endpoint ports to static access mode|Match the access VLAN to the addressing plan", layer="Layer 2", related=["VLAN", "VLAN Troubleshooting"], commands="enable\nconfigure terminal\nvlan 10\n name ADMIN\nvlan 20\n name STAFF\nvlan 30\n name STUDENTS\ninterface fastEthernet 0/1\n switchport mode access\n switchport access vlan 10\n no shutdown", verify=["show vlan brief", "show interfaces switchport"])
add(F, "VLAN Troubleshooting", "VLAN troubleshooting checks whether the VLAN exists, the port mode is correct, and every link carries the intended VLAN.", "Check interface status|Check access VLAN membership|Check trunk allowed lists|Check Layer 3 gateway and addressing", related=["VLAN Configuration", "VLAN Communication Failure"], verify=["show vlan brief", "show interfaces switchport", "show interfaces trunk"])
add(F, "802.1Q Trunking", "IEEE 802.1Q adds VLAN identification to Ethernet frames so one link can carry multiple VLANs.", "Tagged frames identify their VLAN|Native VLAN traffic is normally untagged|Allowed lists control which VLANs cross the trunk", layer="Layer 2", related=["Trunk Configuration", "Native VLAN Mismatch"])
add(F, "Trunk Configuration", "A Cisco trunk carries selected VLANs between switches or between a switch and a router-on-a-stick interface.", "Configure both endpoints consistently|Allow only required VLANs|Match the native VLAN if changed", layer="Layer 2", related=["802.1Q Trunking", "Trunk Troubleshooting"], commands="enable\nconfigure terminal\ninterface gigabitEthernet 0/1\n switchport mode trunk\n switchport trunk allowed vlan 10,20,30\n no shutdown", verify=["show interfaces trunk", "show interfaces switchport"])
add(F, "Trunk Troubleshooting", "Trunk troubleshooting isolates mode, encapsulation, allowed-VLAN, native-VLAN, and physical-link mismatches.", "Verify the operational trunk state|Compare both ends|Confirm the VLAN exists locally|Inspect native VLAN warnings", related=["Trunk Configuration", "Native VLAN Mismatch"], verify=["show interfaces trunk", "show vlan brief", "show logging"])


# Inter-VLAN routing
F = "05 - Inter-VLAN Routing"
add(F, "Router on a Stick", "Router-on-a-stick uses one physical router interface with 802.1Q subinterfaces to route between VLANs.", "The switch link is a trunk|Each subinterface maps to one VLAN|Each subinterface address is that VLAN's gateway", layer="Layer 3 over 802.1Q", related=["802.1Q Trunking", "SVI"], commands="enable\nconfigure terminal\ninterface gigabitEthernet 0/0\n no shutdown\ninterface gigabitEthernet 0/0.10\n encapsulation dot1Q 10\n ip address 192.168.10.1 255.255.255.0\ninterface gigabitEthernet 0/0.20\n encapsulation dot1Q 20\n ip address 192.168.20.1 255.255.255.0", verify=["show ip interface brief", "show interfaces trunk", "show ip route"])
add(F, "Layer 3 Switch Inter-VLAN Routing", "A multilayer switch routes between VLANs using switched virtual interfaces at wire speed.", "Create VLANs and access ports|Create an SVI gateway for each VLAN|Enable ip routing|Verify connected routes", difficulty="Intermediate", related=["SVI", "Multilayer Switch Routing"], commands="enable\nconfigure terminal\nip routing\nvlan 10\nvlan 20\ninterface vlan 10\n ip address 192.168.10.1 255.255.255.0\n no shutdown\ninterface vlan 20\n ip address 192.168.20.1 255.255.255.0\n no shutdown", verify=["show ip interface brief", "show ip route"])
add(F, "SVI", "A switched virtual interface is a logical Layer 3 interface associated with a VLAN.", "The VLAN must exist|At least one member path normally must be active|An SVI can provide management or routed-gateway service", layer="Layer 3", related=["SVI Routing", "VLAN"])
add(F, "Multilayer Switch Routing", "Multilayer switch routing combines Layer 2 VLAN forwarding with Layer 3 route decisions.", "Enable ip routing|Use SVIs for VLAN gateways|Use no switchport for routed links|Add static or dynamic routes as required", difficulty="Intermediate", related=["Routed Port", "SVI Routing"])
add(F, "Routed Port", "A routed switch port behaves as a Layer 3 interface instead of a VLAN switchport.", "Remove Layer 2 mode with no switchport|Assign an IP address and mask|Enable routing and the interface", difficulty="Intermediate", related=["Multilayer Switch Routing"], commands="enable\nconfigure terminal\nip routing\ninterface gigabitEthernet 0/1\n no switchport\n ip address 10.0.0.1 255.255.255.252\n no shutdown", verify=["show ip interface brief", "show ip route"])
add(F, "SVI Routing", "SVI routing uses one logical VLAN interface per subnet to provide inter-VLAN default gateways.", "Create the VLAN|Configure the SVI address|Ensure the SVI line protocol is up|Enable ip routing", difficulty="Intermediate", related=["SVI", "Layer 3 Switch Inter-VLAN Routing"])


# Routing protocols
F = "06 - Routing Protocols"
add(F, "Static Routing", "A static route is manually configured reachability for a destination prefix.", "Match the destination prefix|Point to a reachable next hop or exit interface|Use route tables and pings to verify", layer="Layer 3", related=["Default Route", "Floating Static Route"], commands="enable\nconfigure terminal\nip route 192.168.20.0 255.255.255.0 10.0.0.2", verify=["show ip route", "show ip route static", "ping <destination>"])
add(F, "Default Route", "A default route matches destinations that have no more-specific route.", "Use 0.0.0.0/0 in IPv4|Point toward an upstream router|Confirm a recursive next hop is reachable", layer="Layer 3", related=["Static Routing"], commands="enable\nconfigure terminal\nip route 0.0.0.0 0.0.0.0 10.0.0.1", verify=["show ip route", "show ip route 0.0.0.0"])
add(F, "Floating Static Route", "A floating static route uses a higher administrative distance so it activates only when a preferred route disappears.", "Configure the same destination as the primary path|Set a worse administrative distance|Test primary failure and recovery", difficulty="Intermediate", related=["Static Routing"], commands="enable\nconfigure terminal\nip route 192.168.20.0 255.255.255.0 10.0.1.2 200", verify=["show ip route", "show running-config | include ip route"])
add(F, "RIP", "RIP is a distance-vector routing protocol that uses hop count and permits at most 15 routed hops.", "Routers periodically advertise route vectors|Lowest hop count wins|Split horizon and route poisoning reduce loops|RIPv2 carries masks and multicast updates", layer="Layer 3", ports="UDP 520", related=["RIPv2 Configuration", "RIP Troubleshooting"])
add(F, "RIPv2 Configuration", "RIPv2 configuration enables classless route exchange with masks and multicast updates.", "Enable version 2|Disable automatic summarization|Add connected major networks|Verify learned R routes", layer="Layer 3", ports="UDP 520", related=["RIP", "RIP Troubleshooting"], commands="enable\nconfigure terminal\nrouter rip\n version 2\n no auto-summary\n network 192.168.1.0\n network 10.0.0.0", verify=["show ip route", "show ip protocols"])
add(F, "RIP Troubleshooting", "RIP troubleshooting checks interface networks, version, auto-summary, passive interfaces, and route-table installation.", "Verify connected networks|Compare RIP versions|Check advertised network statements|Inspect administrative distance and better routes", related=["RIP", "RIPv2 Configuration"], verify=["show ip protocols", "show ip route rip", "show running-config | section router rip"])
add(F, "OSPF", "OSPF is a link-state interior gateway protocol that builds a topology database and calculates shortest paths with SPF.", "Discover neighbors with Hello packets|Synchronize link-state databases|Flood LSAs within defined scope|Run SPF and install best routes", difficulty="Intermediate", layer="Layer 3", protocol_number="89", related=["OSPF Single Area", "OSPF Neighbourship", "OSPF Troubleshooting"])
add(F, "OSPF Single Area", "Single-area OSPF places every participating interface in one area, commonly area 0.", "Assign a unique router ID|Match interfaces with network and wildcard statements|Use the same area on shared links|Verify Full neighbors", difficulty="Intermediate", layer="Layer 3", protocol_number="89", related=["OSPF", "OSPF Router ID"], commands="enable\nconfigure terminal\nrouter ospf 1\n router-id 1.1.1.1\n network 192.168.1.0 0.0.0.255 area 0\n network 10.0.0.0 0.0.0.3 area 0", verify=["show ip ospf neighbor", "show ip ospf interface", "show ip route ospf", "show ip protocols"])
add(F, "OSPF Multi Area", "Multi-area OSPF limits link-state flooding and SPF scope by connecting non-backbone areas to area 0 through ABRs.", "Area 0 is the backbone|ABRs maintain databases for attached areas|Summarization can occur at boundaries|Area design affects scale and recovery", difficulty="Advanced", layer="Layer 3", protocol_number="89", support="Partial", related=["OSPF", "OSPF Single Area"])
add(F, "OSPF Neighbourship", "OSPF neighbors progress through defined states before becoming fully adjacent.", "Down and Init establish Hello visibility|2-Way confirms bidirectional communication|ExStart and Exchange negotiate database transfer|Loading requests missing LSAs|Full means databases are synchronized", difficulty="Intermediate", related=["OSPF", "OSPF Troubleshooting"], diagram="flowchart LR\nDown --> Init --> TwoWay[2-Way] --> ExStart --> Exchange --> Loading --> Full")
add(F, "OSPF Router ID", "The OSPF router ID is a 32-bit identifier used in adjacencies and link-state advertisements.", "Manual router-id is most predictable|Otherwise IOS selects a loopback or active interface address|Changing it can require process restart", difficulty="Intermediate", related=["OSPF Single Area"])
add(F, "OSPF Cost", "OSPF cost is an interface metric commonly derived from reference bandwidth divided by interface bandwidth.", "Lower total cost is preferred|Reference bandwidth should be consistent|Manual cost can influence path selection", difficulty="Intermediate", related=["OSPF", "OSPF DR and BDR"])
add(F, "OSPF DR and BDR", "OSPF elects a designated router and backup designated router on multiaccess segments to reduce adjacency and flooding overhead.", "Interface priority influences election|Router ID breaks priority ties|Priority zero prevents candidacy|Elections are non-preemptive", difficulty="Advanced", related=["OSPF Neighbourship"])
add(F, "OSPF Troubleshooting", "OSPF troubleshooting compares interface, area, timer, network type, authentication, MTU, and router-ID parameters.", "Start with IP reachability|Compare Hello-visible parameters|Inspect neighbor state|Check LSDB and route-table results", difficulty="Intermediate", related=["OSPF", "OSPF Neighbour Not Forming"], verify=["show ip ospf neighbor", "show ip ospf interface", "show ip ospf database", "show ip route ospf"])
add(F, "EIGRP", "EIGRP is an advanced distance-vector protocol that uses DUAL to select loop-free successor and feasible-successor paths.", "Neighbors exchange topology information|DUAL selects the successor|Feasibility condition identifies safe backups|Composite metrics compare paths", difficulty="Intermediate", layer="Layer 3", protocol_number="88", related=["EIGRP Configuration", "EIGRP Troubleshooting"])
add(F, "EIGRP Configuration", "Classic EIGRP configuration enables one autonomous-system process and selects participating interfaces with network statements.", "Use the same AS number between neighbors|Match the intended interfaces|Disable classful auto-summary in legacy IOS|Verify neighbors and D routes", difficulty="Intermediate", layer="Layer 3", protocol_number="88", related=["EIGRP", "EIGRP Troubleshooting"], commands="enable\nconfigure terminal\nrouter eigrp 100\n network 192.168.1.0 0.0.0.255\n network 10.0.0.0 0.0.0.3\n no auto-summary", verify=["show ip eigrp neighbors", "show ip eigrp topology", "show ip route eigrp", "show ip protocols"])
add(F, "EIGRP Troubleshooting", "EIGRP troubleshooting checks autonomous-system, K values, address families, passive interfaces, network statements, and reachability.", "Compare neighbor-facing configuration|Verify EIGRP is active on the interface|Inspect neighbor and topology tables|Check route selection", difficulty="Intermediate", related=["EIGRP", "EIGRP Configuration"], verify=["show ip eigrp neighbors", "show ip protocols", "show ip route eigrp"])
add(F, "RIP vs OSPF vs EIGRP", "RIP, OSPF, and EIGRP differ in algorithm, metric, convergence, scale, complexity, and operational visibility.", "RIP uses hop count and scales poorly|OSPF uses link state and open standards|EIGRP uses DUAL and Cisco-oriented operation|Administrative distances affect route selection", difficulty="Intermediate", related=["RIP", "OSPF", "EIGRP"])


# DHCP, DNS, time, and application services
F = "07 - DHCP and Network Services"
add(F, "DHCP", "DHCP automatically leases IPv4 addressing information such as address, mask, gateway, DNS server, and lease time.", "A client broadcasts discovery|A server offers a lease|The client requests one offer|The server acknowledges the binding", layer="Layer 7", ports="UDP 67 server, UDP 68 client", related=["DHCP DORA Process", "Cisco Router DHCP", "Dedicated DHCP Server", "DHCP Relay"], diagram="sequenceDiagram\nClient->>Network: DHCP Discover\nServer-->>Client: DHCP Offer\nClient->>Network: DHCP Request\nServer-->>Client: DHCP Acknowledge")
add(F, "DHCP DORA Process", "DORA describes DHCP Discover, Offer, Request, and Acknowledge messages used to obtain an IPv4 lease.", "Discover locates servers|Offer proposes addressing|Request identifies the chosen offer|Acknowledge confirms the lease", layer="Layer 7", ports="UDP 67/68", related=["DHCP", "DHCP Relay"])
add(F, "Cisco Router DHCP", "Cisco IOS can act as a DHCP server by excluding infrastructure addresses and defining one pool per client subnet.", "Exclude static addresses|Create a pool matching the subnet|Provide the correct default gateway|Verify bindings and conflicts", layer="Layer 7", ports="UDP 67/68", related=["DHCP", "Dedicated DHCP Server"], commands="enable\nconfigure terminal\nip dhcp excluded-address 192.168.10.1 192.168.10.20\nip dhcp pool VLAN10\n network 192.168.10.0 255.255.255.0\n default-router 192.168.10.1\n dns-server 8.8.8.8", verify=["show ip dhcp pool", "show ip dhcp binding", "show ip dhcp conflict"])
add(F, "Dedicated DHCP Server", "A dedicated DHCP server centralizes address pools for multiple VLANs and is the preferred design for the enterprise Packet Tracer labs.", "Give the server a static address|Create one correctly scoped pool per VLAN|Configure each pool gateway and DNS values|Use relay on remote client gateways", layer="Layer 7", ports="UDP 67/68", related=["DHCP Relay", "Packet Tracer DNS Server"], diagram="flowchart LR\nPC[Client VLAN] --> GW[Gateway with helper] --> S[DHCP Server 200.100.10.5]")
add(F, "DHCP Relay", "DHCP relay converts local client broadcasts into routed unicast messages sent to a central DHCP server.", "Configure helper on the client-facing Layer 3 interface|Point to the server IP|Ensure routing works both directions|Match the server pool to the client subnet", layer="Layer 3/Layer 7", ports="UDP 67/68", related=["Dedicated DHCP Server", "DHCP Relay Not Working"], commands="enable\nconfigure terminal\ninterface vlan 10\n ip helper-address 200.100.10.5", verify=["show running-config interface vlan 10", "show ip route", "show ip dhcp binding"])
add(F, "DHCP Troubleshooting", "DHCP troubleshooting follows DORA and checks client VLAN, relay address, server pool, routing, exclusions, and lease availability.", "Capture or simulate DORA|Confirm helper is on the client gateway|Confirm the pool network and gateway|Verify return routing", related=["DHCP", "PC Cannot Get DHCP Address"], verify=["show running-config | include helper-address", "show ip dhcp binding", "show ip route"])
add(F, "DNS", "DNS resolves names into addresses and stores other domain information in distributed records.", "A resolver sends a query|Recursive servers follow referrals or use cache|Authoritative servers answer for their zones|The result is cached for its TTL", layer="Layer 7", ports="UDP/TCP 53", related=["Packet Tracer DNS Server", "DNS Troubleshooting"], diagram="sequenceDiagram\nClient->>Resolver: Query name\nResolver->>Authoritative: Resolve record\nAuthoritative-->>Resolver: A or AAAA answer\nResolver-->>Client: Address")
add(F, "Packet Tracer DNS Server", "Packet Tracer Server-PT can provide basic DNS records for classroom name-resolution labs.", "Configure a static server address|Enable DNS under Services|Create A records mapping names to IPv4 addresses|Point clients to the server", layer="Layer 7", ports="UDP 53", related=["DNS", "Packet Tracer Web Server"], verify=["nslookup <name>", "ping <name>"])
add(F, "DNS Troubleshooting", "DNS troubleshooting separates name-resolution failure from basic IP reachability and application failure.", "Ping the DNS server by address|Check the client DNS setting|Query the exact record|Verify server service and record spelling", related=["DNS", "DNS Resolution Failure"], verify=["nslookup <name>", "ping <dns-server-ip>"])
add(F, "Cisco NTP Configuration", "Cisco IOS NTP configuration points a device at a trusted time source and verifies synchronization state.", "Verify reachability to the server|Configure the NTP server address|Allow polling time|Check association and clock source", layer="Layer 7", ports="UDP 123", related=["NTP", "Lab 13 - NTP Server", "NTP Troubleshooting"], commands="enable\nconfigure terminal\nntp server 200.100.100.15", verify=["show clock", "show ntp associations", "show ntp status"])
add(F, "NTP Troubleshooting", "NTP troubleshooting checks server reachability, UDP 123, configured peers, stratum, authentication, and elapsed polling time.", "Confirm IP reachability|Confirm the server service is active|Inspect association symbols and reach|Wait through polling intervals", related=["NTP", "NTP Not Synchronising"], verify=["show clock detail", "show ntp associations", "show ntp status"])
add(F, "FTP", "FTP transfers files with authentication using a control connection and a separate data connection.", "TCP 21 carries control commands|TCP 20 is associated with active-mode data|Credentials are not strongly protected by basic FTP", layer="Layer 7", ports="TCP 20/21", related=["Packet Tracer FTP Server", "TFTP"])
add(F, "Packet Tracer FTP Server", "Packet Tracer Server-PT can provide accounts and file transfer for basic FTP demonstrations.", "Set a static server address|Enable FTP in Services|Create a user and permissions|Connect from a PC FTP client", layer="Layer 7", ports="TCP 20/21", related=["FTP", "Lab 26 - FTP and TFTP"])
add(F, "TFTP", "TFTP is a simple unauthenticated file-transfer protocol commonly used for network-device images and configuration copies in trusted labs.", "Uses UDP with a simple request-response exchange|Provides no login or encryption|Requires IP reachability and correct server path", layer="Layer 7", ports="UDP 69", related=["Cisco Configuration Backup Using TFTP", "FTP"])
add(F, "Cisco Configuration Backup Using TFTP", "Cisco IOS can copy running or startup configurations to and from a reachable TFTP server.", "Verify server reachability|Supply the server address|Use a distinct filename|Review configuration before restoring", layer="Layer 7", ports="UDP 69", related=["TFTP", "Lab 26 - FTP and TFTP"], commands="enable\ncopy running-config tftp:\ncopy tftp: running-config", verify=["show running-config", "dir flash:"])
add(F, "HTTP", "HTTP transfers web resources without transport encryption.", "A client sends a request method and path|The server returns a status and content|Proxies and caches can participate", layer="Layer 7", ports="TCP 80", related=["HTTPS", "HTTP vs HTTPS"])
add(F, "HTTPS", "HTTPS protects HTTP with TLS authentication, integrity, and encryption.", "A TLS handshake negotiates security|Certificates identify the server|Encrypted HTTP data follows", layer="Layer 7", ports="TCP 443", support="Partial", related=["HTTP", "HTTP vs HTTPS"])
add(F, "HTTP vs HTTPS", "HTTP sends web traffic without TLS while HTTPS adds certificate-based authentication and encryption.", "HTTP commonly uses TCP 80|HTTPS commonly uses TCP 443|HTTPS protects credentials and content in transit", layer="Layer 7", ports="TCP 80 and 443", related=["HTTP", "HTTPS"])
add(F, "Packet Tracer Web Server", "Packet Tracer Server-PT can host simple HTTP and HTTPS pages for DNS and application-layer labs.", "Set a static address and gateway|Enable HTTP or HTTPS service|Edit the index page|Browse by address and DNS name", layer="Layer 7", ports="TCP 80/443", support="Yes", related=["Packet Tracer DNS Server", "HTTP vs HTTPS"])
add(F, "SMTP", "SMTP transfers outgoing email between clients and mail servers or between mail servers.", "Clients submit mail|Servers relay it toward the destination domain|Recipients retrieve it with POP3 or IMAP", layer="Layer 7", ports="TCP 25; submission commonly 587", related=["POP3", "IMAP", "Email Protocols Comparison"])
add(F, "POP3", "POP3 retrieves mail with a download-oriented mailbox model.", "A client authenticates|Messages are listed and retrieved|Clients may delete server copies", layer="Layer 7", ports="TCP 110; secure 995", related=["SMTP", "IMAP"])
add(F, "IMAP", "IMAP synchronizes server-hosted mailboxes, folders, flags, and messages across clients.", "Mail remains organized on the server|Multiple clients share state|Only required content needs to be downloaded", layer="Layer 7", ports="TCP 143; secure 993", support="Partial", related=["SMTP", "POP3"])
add(F, "Email Protocols Comparison", "SMTP sends mail, while POP3 and IMAP retrieve or synchronize received mail.", "SMTP handles submission and relay|POP3 favors simple download|IMAP favors synchronized server mailboxes", layer="Layer 7", ports="SMTP 25/587, POP3 110, IMAP 143", related=["SMTP", "POP3", "IMAP"])


# High availability
F = "08 - Redundancy and High Availability"
add(F, "HSRP Configuration", "HSRP configuration gives two Cisco gateways one virtual IP with active and standby roles.", "Use unique physical addresses|Configure the same group and virtual IP|Set intentional priorities|Enable preemption where required", difficulty="Intermediate", layer="Layer 3", ports="UDP 1985", related=["HSRP", "HSRP Tracking", "Lab 23 - HSRP"], commands="enable\nconfigure terminal\ninterface vlan 10\n ip address 192.168.10.2 255.255.255.0\n standby 10 ip 192.168.10.1\n standby 10 priority 110\n standby 10 preempt", verify=["show standby brief", "show standby"])
add(F, "HSRP Tracking", "HSRP tracking lowers gateway priority when an upstream interface or tracked object fails.", "Choose a failure that affects real reachability|Set a decrement large enough to change preference|Use preemption to move roles|Test failure and recovery", difficulty="Intermediate", related=["HSRP", "HSRP Configuration"], commands="enable\nconfigure terminal\ninterface vlan 10\n standby 10 track gigabitEthernet 0/1 20", verify=["show standby", "show track"])
add(F, "HSRP Troubleshooting", "HSRP troubleshooting checks shared Layer 2 reachability, group, virtual IP, version, priority, preemption, authentication, and tracking.", "Confirm peers hear hello messages|Compare group and VIP|Inspect active and standby roles|Test the virtual gateway", difficulty="Intermediate", related=["HSRP", "Lab 23 - HSRP"], verify=["show standby brief", "show standby", "show ip interface brief"])
add(F, "VRRP", "VRRP is a standards-based first-hop redundancy protocol with master and backup routers sharing a virtual router.", "Elect a master using priority|Backups monitor advertisements|A backup takes over after master failure|The virtual IP remains the endpoint gateway", difficulty="Intermediate", layer="Layer 3", protocol_number="112", support="Partial", related=["VRRP Configuration", "HSRP vs VRRP"])
add(F, "VRRP Configuration", "VRRP configuration creates a shared virtual router on platforms that support the required IOS feature set.", "Use unique physical addresses|Match group and virtual IP|Set priority and preemption intentionally|Verify master and backup", difficulty="Intermediate", support="Partial", related=["VRRP", "HSRP vs VRRP"], commands="enable\nconfigure terminal\ninterface gigabitEthernet 0/0\n ip address 192.168.10.2 255.255.255.0\n vrrp 10 ip 192.168.10.1\n vrrp 10 priority 110\n vrrp 10 preempt", verify=["show vrrp", "show vrrp brief"])
add(F, "HSRP vs VRRP", "HSRP is Cisco-oriented and uses active/standby terminology, while VRRP is standards-based and uses master/backup terminology.", "Both provide a virtual gateway|Both use priority and preemption|Packet Tracer support is stronger for HSRP than VRRP", difficulty="Intermediate", related=["HSRP", "VRRP"])
add(F, "GLBP", "GLBP provides first-hop redundancy and distributes hosts across multiple active virtual forwarders.", "One active virtual gateway coordinates the group|Multiple active virtual forwarders own virtual MAC addresses|Clients can be balanced while redundancy remains", difficulty="Advanced", layer="Layer 3", ports="UDP 3222", support="No", related=["HSRP", "VRRP"])


# Security
F = "09 - Network Security"
add(F, "AAA", "AAA separates authentication, authorization, and accounting for controlled device access.", "Authentication verifies identity|Authorization decides permitted actions|Accounting records activity", difficulty="Intermediate", related=["Local AAA", "RADIUS", "TACACS+"])
add(F, "Local AAA", "Local AAA authenticates users against the device's own username database.", "Enable the AAA model|Create a local privileged user|Define a local login method list|Apply it to console or VTY lines", difficulty="Intermediate", related=["AAA", "Cisco SSH Configuration"], commands="enable\nconfigure terminal\naaa new-model\nusername admin privilege 15 secret <STRONG-PASSWORD>\naaa authentication login default local", verify=["show running-config | section aaa", "show users"])
add(F, "RADIUS", "RADIUS centralizes access authentication and accounting, commonly for network access and administrative login.", "The client sends credentials to a server|The server returns accept reject or challenge|Authorization attributes can accompany the response", difficulty="Intermediate", layer="Layer 7", ports="UDP 1812/1813", support="Partial", related=["AAA", "RADIUS vs TACACS+"])
add(F, "TACACS+", "TACACS+ centralizes Cisco-oriented device administration and separates authentication, authorization, and accounting exchanges.", "The device contacts a TACACS+ server|Authorization can control individual commands|Most packet content is protected", difficulty="Intermediate", layer="Layer 7", ports="TCP 49", support="Partial", related=["AAA", "RADIUS vs TACACS+"])
add(F, "AAA Troubleshooting", "AAA troubleshooting protects recovery access while checking method lists, server reachability, shared secrets, user databases, and line application.", "Keep a local recovery account|Verify IP and time first|Compare shared secrets|Test method order before closing the session", difficulty="Advanced", related=["AAA", "SSH Login Failure"], verify=["show running-config | section aaa", "show aaa servers", "show users"])
add(F, "RADIUS vs TACACS+", "RADIUS commonly supports network access with UDP, while TACACS+ commonly supports device administration with TCP and granular command authorization.", "RADIUS combines authentication and authorization|TACACS+ separates AAA functions|Transport and encryption coverage differ", difficulty="Intermediate", related=["RADIUS", "TACACS+"])
add(F, "SSH", "SSH provides encrypted remote terminal access and should replace Telnet for device administration.", "The server has identity keys|The client verifies and negotiates encryption|User authentication opens a protected channel", layer="Layer 7", ports="TCP 22", related=["Cisco SSH Configuration", "SSH vs Telnet"])
add(F, "Cisco SSH Configuration", "Cisco IOS SSH configuration requires hostname, domain name, RSA keys, local users, and SSH-only VTY transport.", "Set device identity|Create a privileged local user|Generate RSA keys|Restrict VTY transport to SSH", layer="Layer 7", ports="TCP 22", related=["SSH", "SSH Troubleshooting"], commands="enable\nconfigure terminal\nhostname R1\nip domain-name network.lab\nusername admin privilege 15 secret <STRONG-PASSWORD>\ncrypto key generate rsa modulus 2048\nip ssh version 2\nline vty 0 4\n login local\n transport input ssh", verify=["show ip ssh", "show ssh"])
add(F, "SSH Troubleshooting", "SSH troubleshooting checks management IP reachability, keys, domain name, version, local users, VTY authentication, and access controls.", "Ping the device management address|Verify RSA keys and SSH version|Check line vty login and transport|Inspect ACL restrictions", related=["Cisco SSH Configuration", "SSH Login Failure"], verify=["show ip ssh", "show running-config | section line vty", "show users"])
add(F, "Telnet", "Telnet provides legacy remote terminal access without strong encryption and should be limited to isolated teaching demonstrations.", "A TCP session opens to port 23|Credentials and commands can be observed|SSH should replace it in production", layer="Layer 7", ports="TCP 23", related=["SSH", "SSH vs Telnet"], commands="enable\nconfigure terminal\nusername student secret <PASSWORD>\nline vty 0 4\n login local\n transport input telnet")
add(F, "SSH vs Telnet", "SSH encrypts management traffic and authenticates the server, while Telnet exposes session content in clear text.", "SSH uses TCP 22|Telnet uses TCP 23|Only SSH is appropriate for normal production administration", related=["SSH", "Telnet"])
add(F, "ACL", "An access control list evaluates traffic against ordered permit and deny entries, ending with an implicit deny.", "Entries are processed top to bottom|First match decides the action|Direction is relative to the interface|Placement depends on ACL type", layer="Layer 3/Layer 4", related=["Standard ACL", "Extended ACL", "Named ACL"])
add(F, "Standard ACL", "A standard IPv4 ACL filters primarily by source address and is normally placed near the destination.", "Match source networks with wildcard masks|Remember implicit deny|Apply in the correct direction", related=["ACL", "ACL Troubleshooting"], commands="enable\nconfigure terminal\naccess-list 10 permit 192.168.10.0 0.0.0.255\ninterface gigabitEthernet 0/0\n ip access-group 10 out", verify=["show access-lists", "show ip interface"])
add(F, "Extended ACL", "An extended IPv4 ACL can match source, destination, protocol, and transport ports and is normally placed near the source.", "Select protocol|Match source and destination|Match ports where relevant|Apply once in the correct direction", difficulty="Intermediate", related=["ACL", "Named ACL"], commands="enable\nconfigure terminal\naccess-list 100 permit tcp 192.168.10.0 0.0.0.255 any eq 80\ninterface gigabitEthernet 0/0\n ip access-group 100 in", verify=["show access-lists", "show ip interface"])
add(F, "Named ACL", "A named ACL uses a descriptive identifier and supports sequence-based editing on suitable IOS images.", "Choose standard or extended|Add specific permits and denies|Review order and implicit deny|Apply to an interface", difficulty="Intermediate", related=["ACL", "Extended ACL"], commands="enable\nconfigure terminal\nip access-list extended WEB-FILTER\n permit tcp 192.168.10.0 0.0.0.255 any eq 80\n deny ip any any log\nexit", verify=["show ip access-lists"])
add(F, "ACL Troubleshooting", "ACL troubleshooting checks hit counts, entry order, wildcard masks, protocol and port direction, interface placement, and implicit deny.", "Reproduce one flow|Identify its ingress and egress path|Read the ACL top to bottom|Inspect counters and interface direction", difficulty="Intermediate", related=["ACL", "ACL Blocking Traffic"], verify=["show access-lists", "show ip interface", "show running-config | include access-group"])
add(F, "NAT", "NAT translates addresses between inside and outside domains, commonly allowing private IPv4 networks to use public connectivity.", "Classify inside and outside interfaces|Match inside local addresses|Select static dynamic or overload translation|Verify return traffic", layer="Layer 3/Layer 4", related=["Static NAT", "Dynamic NAT", "PAT"])
add(F, "Static NAT", "Static NAT creates a permanent one-to-one mapping between an inside local and inside global address.", "Choose one internal host|Reserve one translated address|Configure inside and outside roles|Verify the fixed translation", difficulty="Intermediate", related=["NAT", "NAT Troubleshooting"], commands="enable\nconfigure terminal\nip nat inside source static 192.168.10.10 203.0.113.10", verify=["show ip nat translations", "show ip nat statistics"])
add(F, "Dynamic NAT", "Dynamic NAT allocates one address from a public pool for each matching inside host while translations are active.", "Define a pool|Match inside sources with an ACL|Connect the ACL to the pool|Mark inside and outside interfaces", difficulty="Intermediate", related=["NAT", "PAT"])
add(F, "PAT", "PAT overloads many inside hosts onto one outside address by tracking transport identifiers.", "Match inside sources|Mark inside and outside interfaces|Translate through the outside interface address|Inspect translation entries", difficulty="Intermediate", related=["NAT", "NAT Troubleshooting"], commands="enable\nconfigure terminal\naccess-list 1 permit 192.168.10.0 0.0.0.255\ninterface gigabitEthernet 0/0\n ip nat inside\ninterface gigabitEthernet 0/1\n ip nat outside\nip nat inside source list 1 interface gigabitEthernet 0/1 overload", verify=["show ip nat translations", "show ip nat statistics"])
add(F, "NAT Troubleshooting", "NAT troubleshooting checks routing first, then inside/outside roles, source ACL matching, pool or interface selection, and translation counters.", "Verify un-translated reachability|Check interface roles|Compare traffic against the NAT ACL|Inspect translations while generating traffic", difficulty="Intermediate", related=["NAT", "NAT Not Working"], verify=["show ip nat translations", "show ip nat statistics", "show access-lists", "show ip route"])
add(F, "Switch Port Security", "Switch port security restricts which source MAC addresses may use an access port.", "Enable on a static access port|Set maximum secure addresses|Learn sticky addresses or configure them|Choose protect restrict or shutdown violation mode", layer="Layer 2", related=["Port Security Troubleshooting"], commands="enable\nconfigure terminal\ninterface fastEthernet 0/1\n switchport mode access\n switchport port-security\n switchport port-security maximum 2\n switchport port-security mac-address sticky\n switchport port-security violation restrict", verify=["show port-security", "show port-security interface fastEthernet 0/1"])
add(F, "Port Security Troubleshooting", "Port security troubleshooting checks port mode, secure MAC learning, maximum count, violation mode, and error-disabled state.", "Inspect port-security status|Compare learned and connected MAC addresses|Remove the cause before recovery|Shut and reopen a shutdown port", related=["Switch Port Security", "Lab 24 - Port Security"], verify=["show port-security interface fastEthernet 0/1", "show interfaces status"])
add(F, "DHCP Snooping", "DHCP snooping blocks rogue DHCP server messages on untrusted ports and builds a trusted binding database.", "Enable globally and per VLAN|Trust only legitimate server-facing paths|Rate-limit untrusted access ports|Use bindings for DAI and IP Source Guard", layer="Layer 2", related=["Dynamic ARP Inspection", "IP Source Guard"], commands="enable\nconfigure terminal\nip dhcp snooping\nip dhcp snooping vlan 10,20\ninterface gigabitEthernet 0/1\n ip dhcp snooping trust", verify=["show ip dhcp snooping", "show ip dhcp snooping binding"])
add(F, "Dynamic ARP Inspection", "Dynamic ARP Inspection validates ARP messages against trusted bindings to reduce ARP spoofing.", "Enable DHCP snooping first|Enable DAI per VLAN|Trust only infrastructure links|Validate untrusted ARP against bindings", layer="Layer 2", related=["DHCP Snooping", "ARP"], commands="enable\nconfigure terminal\nip arp inspection vlan 10,20\ninterface gigabitEthernet 0/1\n ip arp inspection trust", verify=["show ip arp inspection", "show ip arp inspection statistics"])
add(F, "IP Source Guard", "IP Source Guard filters access-port traffic that does not match an approved IP and MAC binding.", "Build DHCP snooping bindings|Enable source verification on untrusted access ports|Handle static hosts with explicit bindings where supported", layer="Layer 2", support="Partial", related=["DHCP Snooping", "Dynamic ARP Inspection"], commands="enable\nconfigure terminal\ninterface fastEthernet 0/1\n ip verify source", verify=["show ip verify source", "show ip dhcp snooping binding"])


# Network management and monitoring
F = "10 - Network Management and Monitoring"
add(F, "Wireshark", "Wireshark captures and decodes network traffic so engineers can inspect protocol behavior and faults packet by packet.", "Select the correct capture interface|Apply a capture or display filter|Follow the packet sequence|Compare fields with the expected design", support="No", related=["Packet Capture", "Network Monitoring"], verify=["icmp", "arp", "dns", "dhcp", "tcp", "udp", "ospf"])
add(F, "Packet Capture", "Packet capture records traffic at an observation point for protocol analysis and evidence-based troubleshooting.", "Choose an observation point|Capture a controlled test|Filter to the relevant conversation|Correlate packets with device state and time", support="Partial", related=["Wireshark", "Network Troubleshooting Methodology"])
add(F, "SNMPv2c", "SNMPv2c provides efficient polling and notifications but relies on unencrypted community strings.", "The manager sends Get or GetNext requests|The agent returns MIB object values|Traps notify the manager without polling", layer="Layer 7", ports="UDP 161/162", related=["SNMP", "SNMPv3"])
add(F, "SNMPv3", "SNMPv3 adds user-based authentication, integrity, and optional privacy to network management.", "Create an SNMPv3 group and user|Choose authentication and privacy algorithms|Restrict views and manager access|Use credentials instead of community strings", difficulty="Advanced", layer="Layer 7", ports="UDP 161/162", support="Partial", related=["SNMP", "SNMPv2c"])
add(F, "Cisco SNMP Configuration", "Cisco IOS SNMP configuration defines read access, device identity, and optional trap destinations.", "Use a unique read-only community in labs|Set contact and location|Configure a manager for traps|Prefer SNMPv3 in production", layer="Layer 7", ports="UDP 161/162", related=["SNMP", "Lab 14 - SNMP Monitoring", "SNMP Troubleshooting"], commands="enable\nconfigure terminal\nsnmp-server community NETWORK-RO ro\nsnmp-server location Main-Office\nsnmp-server contact admin@example.com", verify=["show running-config | include snmp", "show snmp", "show snmp community"])
add(F, "SNMP Troubleshooting", "SNMP troubleshooting checks IP reachability, version, credentials, UDP 161/162, views, ACLs, and requested OIDs.", "Ping the agent|Match manager and agent version|Check the exact community or user|Test a standard system OID", related=["SNMP", "Cisco SNMP Configuration"], verify=["show snmp", "show running-config | include snmp"])
add(F, "Cisco Syslog Configuration", "Cisco IOS Syslog configuration timestamps events and sends an intentional severity range to a central collector.", "Enable meaningful timestamps|Configure the server address|Choose a severity threshold|Generate and verify a test event", layer="Layer 7", ports="UDP 514 in Packet Tracer", related=["Syslog", "Syslog Severity Levels", "Lab 15 - Syslog Server"], commands="enable\nconfigure terminal\nservice timestamps log datetime msec\nlogging 200.100.100.20\nlogging trap informational", verify=["show logging", "show running-config | include logging"])
add(F, "Syslog Severity Levels", "Syslog severity ranges from 0 emergencies to 7 debugging; a threshold includes that level and every more serious level.", "0 Emergencies|1 Alerts|2 Critical|3 Errors|4 Warnings|5 Notifications|6 Informational|7 Debugging", layer="Layer 7", ports="UDP 514", related=["Syslog", "Cisco Syslog Configuration"])


# WAN and VPN
F = "11 - WAN and VPN"
add(F, "VPN", "A virtual private network protects traffic across an untrusted network by creating an authenticated encrypted tunnel.", "Peers authenticate|Security parameters are negotiated|Traffic is encapsulated and protected|Policies decide which traffic enters the tunnel", difficulty="Intermediate", support="Partial", related=["Site-to-Site VPN", "Remote Access VPN", "IPsec"])
add(F, "Site-to-Site VPN", "A site-to-site VPN connects entire networks through security gateways.", "Define interesting traffic|Authenticate the peer gateways|Negotiate IPsec security associations|Route matching traffic through the tunnel", difficulty="Advanced", support="Partial", related=["VPN", "IPsec"])
add(F, "Remote Access VPN", "A remote-access VPN securely connects an individual user device to an organizational network.", "The client reaches a VPN gateway|User and device authenticate|An encrypted tunnel is established|Access policy limits reachable resources", difficulty="Advanced", support="No", related=["VPN", "AAA"])
add(F, "IPsec", "IPsec protects IP traffic with authentication, integrity, anti-replay controls, and optional encryption.", "IKE negotiates keys and policies|ESP commonly protects payloads|Security associations are directional|Selectors identify protected traffic", difficulty="Advanced", layer="Layer 3", protocol_number="ESP 50, AH 51", support="Partial", related=["VPN", "GRE over IPsec"])
add(F, "GRE Tunnel", "GRE creates a logical point-to-point tunnel that can carry routed and multicast traffic but does not encrypt it.", "Encapsulate the original packet|Route the outer packet between tunnel endpoints|Assign tunnel addresses|Add IPsec when confidentiality is needed", difficulty="Advanced", layer="Layer 3", protocol_number="47", support="Partial", related=["GRE over IPsec", "IPsec"], commands="enable\nconfigure terminal\ninterface tunnel 0\n ip address 10.10.10.1 255.255.255.252\n tunnel source gigabitEthernet 0/0\n tunnel destination 200.100.100.2\n no shutdown", verify=["show interfaces tunnel 0", "show ip route", "ping 10.10.10.2"])
add(F, "GRE over IPsec", "GRE over IPsec combines flexible GRE encapsulation with IPsec encryption and authentication.", "GRE carries multicast or multiple protocols|IPsec protects the GRE outer flow|Routing and security dependencies must both work", difficulty="Advanced", support="No", related=["GRE Tunnel", "IPsec"])
add(F, "PPP", "PPP is a point-to-point WAN encapsulation that supports negotiation, authentication, and multiple Layer 3 protocols.", "LCP establishes and tests the link|Optional PAP or CHAP authenticates peers|NCP configures Layer 3 protocol use", difficulty="Intermediate", layer="Layer 2", related=["PPP PAP", "PPP CHAP", "HDLC"])
add(F, "PPP PAP", "PAP is a simple PPP authentication method that sends credentials without strong protection.", "The requester repeatedly sends a username and password|The peer accepts or rejects|CHAP is preferable where available", difficulty="Intermediate", related=["PPP", "PAP vs CHAP"])
add(F, "PPP CHAP", "CHAP authenticates PPP peers through a challenge-response exchange without sending the shared secret directly.", "The authenticator sends a random challenge|The peer hashes the challenge with the secret|The authenticator compares the result", difficulty="Intermediate", related=["PPP", "PAP vs CHAP"])
add(F, "PAP vs CHAP", "PAP sends reusable credentials with weak protection, while CHAP uses periodic challenge-response authentication.", "PAP is simple but weak|CHAP avoids transmitting the shared secret|Both require matching peer configuration", difficulty="Intermediate", related=["PPP PAP", "PPP CHAP"])
add(F, "HDLC", "Cisco HDLC is the default proprietary serial encapsulation on many Cisco router interfaces.", "Frames carry a Cisco type field|No authentication is provided|Both ends must use compatible encapsulation", layer="Layer 2", support="Partial", related=["HDLC vs PPP", "PPP"])
add(F, "HDLC vs PPP", "Cisco HDLC is simple and Cisco-oriented, while PPP adds standards-based negotiation and optional PAP or CHAP authentication.", "Both encapsulate point-to-point serial traffic|PPP provides more negotiation features|Interoperability and authentication often favor PPP", related=["HDLC", "PPP"])


# Wireless
F = "12 - Wireless Networking"
add(F, "Wireless Networking", "Wireless LANs use IEEE 802.11 radio links to connect clients through access points.", "Clients discover an SSID|Authentication and association establish access|Frames share radio airtime|The AP bridges traffic toward the wired LAN", layer="Layer 1 and Layer 2", related=["Wi-Fi Standards", "SSID", "Wireless Security"])
add(F, "Wi-Fi Standards", "IEEE 802.11 amendments define wireless bands, channel widths, modulation, spatial streams, and capabilities.", "2.4 GHz offers reach but limited non-overlapping channels|5 GHz offers more channels|6 GHz provides additional clean spectrum on supported devices", support="Partial", related=["Wireless Networking", "Wireless Security"])
add(F, "SSID", "An SSID is the human-readable identifier advertised or configured for a wireless LAN.", "An SSID identifies a service set|Multiple SSIDs can map to different VLANs|Hiding the SSID is not strong security", layer="Layer 2", related=["Wireless Networking", "WPA2"])
add(F, "WPA2", "WPA2 protects wireless access with AES-based CCMP in personal or enterprise authentication modes.", "Personal mode uses a shared passphrase|Enterprise mode uses 802.1X and AAA|Strong unique credentials remain necessary", support="Yes", related=["WPA3", "Wireless Security"])
add(F, "WPA3", "WPA3 improves wireless authentication and protection, including SAE for personal networks.", "SAE resists offline password guessing better than PSK exchange|Protected management features are strengthened|Legacy compatibility can affect deployment", support="No", related=["WPA2", "Wireless Security"])
add(F, "Wireless Security", "Wireless security combines strong authentication, encryption, segmentation, radio planning, and monitoring.", "Prefer WPA2-AES or WPA3|Separate guest and internal networks|Use enterprise authentication where appropriate|Monitor rogue access points", support="Partial", related=["WPA2", "WPA3", "AAA"])


# IPv6
F = "13 - IPv6"
add(F, "IPv6", "IPv6 uses 128-bit addressing, extension headers, multicast, neighbor discovery, and large hierarchical prefixes.", "Use hexadecimal colon notation|Enable IPv6 routing on routers|Assign /64 LAN prefixes|Use NDP instead of ARP", layer="Layer 3", protocol_number="41", related=["IPv6 Address Types", "IPv6 SLAAC", "IPv6 Troubleshooting"], commands="enable\nconfigure terminal\nipv6 unicast-routing\ninterface gigabitEthernet 0/0\n ipv6 address 2001:DB8:10::1/64\n ipv6 enable\n no shutdown", verify=["show ipv6 interface brief", "show ipv6 route", "show ipv6 neighbors"])
add(F, "IPv6 Address Types", "IPv6 defines global unicast, unique local, link-local, multicast, anycast, loopback, and unspecified address uses.", "Global unicast is Internet-routable|Link-local FE80::/10 supports local control|Multicast replaces broadcast|::1 is loopback", layer="Layer 3", related=["IPv6", "IPv6 SLAAC"])
add(F, "IPv6 Static Routing", "IPv6 static routes manually define reachability for IPv6 prefixes.", "Enable ipv6 unicast-routing|Use an outgoing interface and/or next hop|Use ::/0 for a default route|Verify recursive reachability", difficulty="Intermediate", related=["IPv6", "IPv6 Troubleshooting"], commands="enable\nconfigure terminal\nipv6 unicast-routing\nipv6 route 2001:DB8:20::/64 2001:DB8:12::2", verify=["show ipv6 route", "ping ipv6 <destination>"])
add(F, "IPv6 SLAAC", "SLAAC lets hosts create IPv6 addresses from router advertisements without a stateful address server.", "Routers advertise a prefix and flags|Hosts create interface identifiers|Duplicate Address Detection checks uniqueness|A link-local router can become the default gateway", layer="Layer 3", related=["IPv6", "DHCPv6"])
add(F, "DHCPv6", "DHCPv6 supplies stateful addresses or additional parameters, depending on router-advertisement flags and design.", "Clients use multicast to discover servers or relays|Stateful mode leases addresses|Stateless mode supplies options such as DNS", layer="Layer 7", ports="UDP 546/547", support="Partial", related=["IPv6 SLAAC", "DHCP"])
add(F, "IPv6 OSPFv3", "OSPFv3 exchanges IPv6 routes with link-local neighbor relationships and interface-oriented configuration.", "Enable IPv6 routing|Assign router IDs|Activate OSPFv3 on intended interfaces|Verify IPv6 neighbors and routes", difficulty="Advanced", protocol_number="89", support="Partial", related=["OSPF", "IPv6"], verify=["show ipv6 ospf neighbor", "show ipv6 route ospf", "show ipv6 protocols"])
add(F, "IPv6 Troubleshooting", "IPv6 troubleshooting checks interface state, prefix length, link-local addresses, router advertisements, neighbor discovery, and routing.", "Inspect IPv6 interface state|Check neighbor cache|Verify RA and default route|Follow the IPv6 route table", difficulty="Intermediate", related=["IPv6", "IPv6 SLAAC"], verify=["show ipv6 interface brief", "show ipv6 neighbors", "show ipv6 route", "ping ipv6 <destination>"])


# Troubleshooting methodology and problem guides
F = "14 - Troubleshooting"
add(F, "Cisco Troubleshooting Commands", "Cisco show, ping, and traceroute commands reveal interface, switching, routing, service, security, and neighbor state without changing configuration.", "Capture a baseline|Use the most specific show command|Compare expected and actual state|Change one cause at a time", related=["Cisco Troubleshooting Cheat Sheet", "Network Troubleshooting Methodology"], verify=["show running-config", "show startup-config", "show ip interface brief", "show interfaces", "show interfaces status", "show vlan brief", "show interfaces trunk", "show spanning-tree", "show etherchannel summary", "show ip route", "show ip protocols", "show ip ospf neighbor", "show arp", "show mac address-table", "show access-lists", "show ip nat translations", "show cdp neighbors", "show lldp neighbors", "show clock", "show ntp associations", "show logging", "ping", "traceroute"])
add(F, "Network Troubleshooting Methodology", "A structured troubleshooting method identifies the problem, tests a theory, implements a controlled solution, verifies recovery, and documents evidence.", "Identify the problem|Establish a theory|Test the theory|Create an action plan|Implement the solution|Verify operation|Document findings", related=["Cisco Troubleshooting Method", "OSI Troubleshooting"])
add(F, "Cisco Troubleshooting Method", "Cisco troubleshooting combines layered reasoning with device state, path tracing, comparison, and controlled change.", "Bottom-up starts at media|Top-down starts at the application|Divide-and-conquer starts near Layer 3|Follow-the-path finds the first failed hop|Comparison finds configuration drift", related=["Network Troubleshooting Methodology", "Cisco Troubleshooting Commands"])
add(F, "OSI Troubleshooting", "OSI troubleshooting maps symptoms and tests to Physical, Data Link, Network, Transport, and application functions.", "Check link before VLAN|Check VLAN before IP|Check IP before ports|Check ports before application configuration", related=["OSI Model", "OSI Troubleshooting Method"])

PROBLEMS = {
    "PC Cannot Get DHCP Address": "No valid lease is received; check access VLAN, trunk path, helper address, server pool, routing, and available addresses.",
    "PC Cannot Ping Gateway": "The endpoint cannot reach its local Layer 3 gateway; check cable, VLAN, address, mask, ARP, gateway SVI, and port state.",
    "VLAN Communication Failure": "Hosts expected in the same VLAN cannot communicate; verify access membership, VLAN existence, trunks, STP, and host addressing.",
    "Trunk Failure": "A switch link is not carrying required VLANs; compare both ends for link, mode, allowed list, native VLAN, and VLAN existence.",
    "Native VLAN Mismatch": "The two ends of an 802.1Q trunk use different native VLANs, creating warnings and possible traffic leakage.",
    "OSPF Neighbour Not Forming": "OSPF does not reach Full; compare subnet, area, timers, network type, authentication, MTU, passive state, and router IDs.",
    "RIP Route Missing": "An expected RIP route is absent; check version, network statements, passive interfaces, auto-summary, hop count, and better routes.",
    "EtherChannel Failure": "Member links do not bundle; compare mode, protocol, speed, duplex, switchport mode, VLANs, and allowed lists on both sides.",
    "STP Blocking Problems": "A link blocks unexpectedly or the wrong root is selected; inspect bridge priorities, path costs, port roles, and topology.",
    "ACL Blocking Traffic": "Traffic is denied unexpectedly; follow the flow, inspect ACL order and counters, and confirm interface direction and wildcard masks.",
    "NAT Not Working": "Translations are absent or unusable; verify routing, inside/outside roles, source ACL matching, and return reachability.",
    "DHCP Relay Not Working": "Remote clients cannot reach the central DHCP server; check helper placement, server route, pool scope, and VLAN path.",
    "DNS Resolution Failure": "Names fail while IP connectivity may work; verify the client DNS address, server reachability, service state, and record spelling.",
    "SSH Login Failure": "SSH connection or authentication fails; check management reachability, RSA keys, SSH version, local user, VTY settings, and ACLs.",
    "NTP Not Synchronising": "The device remains unsynchronized; check reachability, server service, UDP 123, association state, authentication, and polling time.",
}
for problem_title, problem_summary in PROBLEMS.items():
    add(F, problem_title, problem_summary,
        "Record the exact symptom and scope|Check the relevant physical and logical path|Use show commands to compare expected state|Correct one verified cause|Repeat the original test",
        difficulty="Intermediate", related=["Network Troubleshooting Methodology", "Cisco Troubleshooting Commands"])


# Switching companion notes (the canonical STP overview is preserved from the existing vault)
F = "03 - Switching"
add(F, "STP Root Bridge", "The STP root bridge is the switch with the lowest bridge ID and acts as the path-cost reference for one spanning-tree instance.", "Compare bridge priorities first|Use MAC address only to break a priority tie|Configure the intended root deliberately|Verify the Root ID on every switch", layer="Layer 2", related=["STP", "STP Configuration"])
add(F, "STP Port Roles", "STP assigns root, designated, alternate, and backup roles so only a loop-free set of ports forwards.", "Each non-root switch chooses one root port|Each segment chooses one designated port|Alternate and backup roles remain non-forwarding", layer="Layer 2", related=["STP", "STP Port States"])
add(F, "STP Port States", "STP port states control whether a port receives BPDUs, learns MAC addresses, and forwards user traffic.", "Classic STP uses blocking listening learning forwarding|RSTP uses discarding learning forwarding|State transitions prevent temporary loops", layer="Layer 2", related=["STP", "RSTP"])
add(F, "PVST+", "Cisco PVST+ runs a separate classic spanning-tree instance for each VLAN.", "Each VLAN can have a different root|802.1Q trunks carry the instances|Per-VLAN tuning can distribute traffic", layer="Layer 2", related=["STP", "RSTP"])
add(F, "STP Configuration", "Cisco STP configuration selects planned primary and secondary roots and verifies port roles for each VLAN.", "Choose the intended root location|Set root primary and secondary|Verify roles on every redundant link|Test one link failure", layer="Layer 2", related=["STP", "STP Troubleshooting", "Lab 20 - STP"], commands="enable\nconfigure terminal\nspanning-tree vlan 10 root primary\nspanning-tree vlan 20 root secondary", verify=["show spanning-tree", "show spanning-tree vlan 10"])
add(F, "STP Troubleshooting", "STP troubleshooting checks root placement, bridge priority, path cost, VLAN presence, trunk state, port roles, and protection features.", "Identify the root seen by each switch|Trace the lowest-cost path|Inspect alternate ports|Check for BPDU Guard or inconsistent states", difficulty="Intermediate", related=["STP", "STP Blocking Problems"], verify=["show spanning-tree vlan 10", "show spanning-tree inconsistentports", "show interfaces status"])
add(F, "RSTP", "Rapid Spanning Tree Protocol accelerates convergence with proposal-agreement handshakes and alternate paths.", "Root and designated roles forward|Alternate ports provide rapid backup|Edge ports can transition immediately|Discarding combines legacy non-forwarding states", layer="Layer 2", related=["RSTP vs STP", "PortFast"], commands="enable\nconfigure terminal\nspanning-tree mode rapid-pvst", verify=["show spanning-tree summary", "show spanning-tree vlan 10"])
add(F, "RSTP vs STP", "RSTP preserves STP loop prevention while using fewer states and faster transition mechanisms.", "STP uses slower timer-driven convergence|RSTP uses rapid role negotiation|Both elect a root and block redundant paths", layer="Layer 2", related=["STP", "RSTP"])
add(F, "PortFast", "PortFast marks an endpoint-facing access port as an edge so it can enter forwarding without normal STP delay.", "Use only toward endpoints|It does not disable STP|Pair with BPDU Guard", layer="Layer 2", related=["BPDU Guard", "STP"], commands="enable\nconfigure terminal\ninterface fastEthernet 0/1\n spanning-tree portfast", verify=["show spanning-tree interface fastEthernet 0/1 detail"])
add(F, "BPDU Guard", "BPDU Guard error-disables a protected edge port that receives a BPDU.", "Enable on untrusted PortFast access ports|A detected switch causes shutdown|Remove the cause before recovering the port", layer="Layer 2", related=["PortFast", "STP"], commands="enable\nconfigure terminal\ninterface fastEthernet 0/1\n spanning-tree portfast\n spanning-tree bpduguard enable", verify=["show interfaces status", "show spanning-tree summary"])
add(F, "EtherChannel", "EtherChannel bundles compatible physical links into one logical port-channel for bandwidth and redundancy.", "Member settings must match|A negotiation protocol or static on mode forms the bundle|STP treats the port-channel as one link", layer="Layer 2 or Layer 3", related=["LACP", "PAgP", "EtherChannel Troubleshooting"])
add(F, "LACP", "LACP is the standards-based EtherChannel negotiation protocol using active and passive modes.", "Active initiates negotiation|Passive responds|At least one side must be active|Members must have consistent settings", layer="Layer 2", related=["EtherChannel", "PAgP"], commands="enable\nconfigure terminal\ninterface range gigabitEthernet 0/1 - 2\n channel-group 1 mode active\ninterface port-channel 1\n switchport mode trunk", verify=["show etherchannel summary", "show interfaces port-channel 1"])
add(F, "PAgP", "PAgP is Cisco's EtherChannel negotiation protocol using desirable and auto modes.", "Desirable initiates negotiation|Auto responds|At least one side must be desirable|Use only between compatible Cisco devices", layer="Layer 2", related=["EtherChannel", "LACP"], commands="enable\nconfigure terminal\ninterface range gigabitEthernet 0/1 - 2\n channel-group 1 mode desirable", verify=["show etherchannel summary"])
add(F, "EtherChannel Troubleshooting", "EtherChannel troubleshooting compares protocol, channel-group, mode, speed, duplex, trunk, native VLAN, and allowed VLAN settings on every member.", "Inspect bundle flags|Compare both endpoints|Correct member configuration consistently|Shut and re-enable only after the mismatch is removed", difficulty="Intermediate", related=["EtherChannel", "EtherChannel Failure"], verify=["show etherchannel summary", "show interfaces trunk", "show running-config interface port-channel 1"])


# Advanced platform guidance
F = "20 - Advanced Networking"
add(F, "Network Technology Lab Platform Guide", "This guide selects Packet Tracer, Wireshark, Linux, GNS3, EVE-NG, Cisco CML, or real hardware according to the feature being taught.", "Use Packet Tracer for CCNA-scale logic and GUI services|Use Wireshark for packet evidence|Use emulation for realistic IOS feature depth|Use real hardware for physical behavior and platform limits", difficulty="Intermediate", support="Yes", related=["Packet Capture", "Complete Enterprise Network Design"])
add(F, "Complete Enterprise Network Design", "A complete teaching enterprise combines hierarchical switching, routing, services, security, monitoring, redundancy, and controlled Internet access.", "Separate access distribution and edge roles|Use documented VLAN and IP plans|Add services only after routing works|Validate with a testing matrix", difficulty="Advanced", support="Partial", related=["Lab 29 - Complete Enterprise Network", "Networking Learning Roadmap"])


@dataclass
class LabSpec:
    number: int
    title: str
    objective: str
    devices: str
    tasks: list[str]
    tests: list[str]
    related: list[str]
    difficulty: str = "Beginner"
    support: str = "Yes"

    @property
    def filename(self) -> str:
        return f"Lab {self.number:02d} - {self.title}"


LABS = [
    LabSpec(1, "Basic Router and Switch Configuration", "Securely name, address, verify, and save one router and one switch.", "1 router, 1 switch, 1 PC", ["Cable PC1 to SW1 and SW1 to R1.", "Apply the router and switch baseline configurations.", "Configure one management subnet.", "Verify console, interface, and saved state."], ["PC1 reaches R1", "SW1 management address responds", "Startup configurations exist"], ["Cisco Router Basic Configuration", "Cisco Switch Basic Configuration"]),
    LabSpec(2, "IPv4 Addressing", "Assign valid IPv4 addresses, masks, and gateways to two LANs connected by one router.", "1 router, 2 switches, 2 PCs", ["Create two /24 LANs.", "Address one router interface in each LAN.", "Configure unique PC addresses and correct gateways.", "Verify local and routed pings."], ["Each PC reaches its gateway", "PC1 reaches PC2"], ["IPv4 Addressing", "Default Gateway"]),
    LabSpec(3, "Subnetting", "Design and implement subnets derived from one /24 block.", "1 router, 2 switches, 4 PCs", ["Divide 192.168.1.0/24 into /27 subnets.", "Document network, usable range, and broadcast.", "Assign two subnets to router interfaces and endpoints.", "Verify no duplicate or out-of-range addresses."], ["All hosts reach their gateway", "Inter-subnet ping succeeds"], ["Subnetting Step by Step", "Subnetting Cheat Sheet"]),
    LabSpec(4, "VLAN Configuration", "Create Administration, Staff, and Students VLANs and place endpoint ports correctly.", "2 switches, 6 PCs", ["Create VLANs 10, 20, and 30 on both switches.", "Assign two access ports per VLAN.", "Verify VLAN membership before adding trunks.", "Test same-switch same-VLAN behavior."], ["Same-VLAN local pings succeed", "Different VLANs remain isolated"], ["VLAN", "VLAN Configuration"]),
    LabSpec(5, "802.1Q Trunking", "Carry VLANs 10, 20, and 30 between two switches over one trunk.", "2 switches, 6 PCs", ["Reuse the three-VLAN access design.", "Configure the inter-switch link as a trunk on both ends.", "Allow VLANs 10,20,30.", "Verify tagging behavior in Simulation Mode."], ["Same-VLAN cross-switch pings succeed", "show interfaces trunk lists all VLANs"], ["802.1Q Trunking", "Trunk Configuration"]),
    LabSpec(6, "Router on a Stick", "Route between three VLANs with one router physical interface and 802.1Q subinterfaces.", "1 router, 2 switches, 6 PCs", ["Build VLANs and trunks.", "Configure router subinterfaces for VLANs 10,20,30.", "Use each subinterface address as its VLAN gateway.", "Verify connected routes and inter-VLAN traffic."], ["Each PC reaches its gateway", "VLAN10 reaches VLAN20 and VLAN30"], ["Router on a Stick", "Trunk Configuration"], difficulty="Intermediate"),
    LabSpec(7, "Multilayer Switch Inter-VLAN Routing", "Use SVIs and ip routing to route between VLANs on a multilayer switch.", "1 multilayer switch, 2 access switches, 6 PCs", ["Create VLANs on all switches.", "Configure access and trunk ports.", "Create one SVI per VLAN on the multilayer switch.", "Enable ip routing and verify connected routes."], ["SVIs are up/up", "All VLANs route through the multilayer switch"], ["Layer 3 Switch Inter-VLAN Routing", "SVI Routing"], difficulty="Intermediate"),
    LabSpec(8, "Static Routing", "Connect three router LANs with explicit static routes.", "3 routers, 3 switches, 3 PCs", ["Address LAN and point-to-point links.", "Verify directly connected neighbors.", "Add destination routes on every router.", "Trace end-to-end traffic."], ["All remote LANs appear as static routes", "PC1 reaches PC3"], ["Static Routing", "Default Route"], difficulty="Intermediate"),
    LabSpec(9, "RIPv2", "Exchange classless routes across three routers with RIPv2.", "3 routers, 3 switches, 3 PCs", ["Build and address three routed LANs.", "Enable RIPv2 and disable auto-summary.", "Advertise only connected networks.", "Inspect protocols and learned R routes."], ["All routers learn remote LANs", "End-to-end pings succeed"], ["RIP", "RIPv2 Configuration"], difficulty="Intermediate"),
    LabSpec(10, "OSPF", "Form single-area OSPF adjacencies and exchange LAN routes.", "3 routers, 3 switches, 3 PCs", ["Address all links and verify direct reachability.", "Assign unique router IDs.", "Advertise interfaces into area 0 with correct wildcards.", "Verify Full neighbors and O routes."], ["Neighbors reach Full", "All LAN routes appear as O", "PC1 reaches PC3"], ["OSPF Single Area", "OSPF Neighbourship"], difficulty="Intermediate"),
    LabSpec(11, "Central DHCP Server", "Serve multiple VLANs from dedicated DHCP server 200.100.10.5 using relay.", "1 multilayer switch or router, 2 switches, Server0, 6 PCs", ["Give Server0 static address 200.100.10.5.", "Create one DHCP pool per client VLAN.", "Configure ip helper-address on every remote client gateway.", "Use DHCP on clients and inspect leases."], ["Every client receives the correct subnet", "Gateways and DNS values match the pool", "Inter-VLAN routing works"], ["Dedicated DHCP Server", "DHCP Relay"], difficulty="Intermediate"),
    LabSpec(12, "DNS Server", "Resolve a classroom web-server name through Packet Tracer DNS.", "1 router, 1 switch, DNS server, web server, 2 PCs", ["Configure static server addresses.", "Enable DNS and create an A record.", "Point clients to the DNS server.", "Test name and address separately."], ["nslookup returns the web server address", "Browser opens the named site"], ["DNS", "Packet Tracer DNS Server"]),
    LabSpec(13, "NTP Server", "Synchronize Cisco device time with a Packet Tracer NTP server.", "1 router, Server0", ["Configure IP reachability.", "Enable Server0 NTP service.", "Configure ntp server on the router.", "Verify clock and association state."], ["Router reaches Server0", "Clock reports synchronized"], ["NTP", "Cisco NTP Configuration"]),
    LabSpec(14, "SNMP Monitoring", "Query Cisco system OIDs from a Packet Tracer manager.", "1 router, 1 PC", ["Configure read-only SNMPv2c.", "Set location and contact.", "Use MIB Browser to query sysName and sysUpTime.", "Verify agent counters."], ["Ping succeeds", "MIB Browser returns valid values"], ["SNMP", "Cisco SNMP Configuration"]),
    LabSpec(15, "Syslog Server", "Send timestamped Cisco IOS events to a central Packet Tracer Syslog server.", "1 router, Server0", ["Enable Server0 Syslog service.", "Configure timestamps and logging host.", "Set informational threshold.", "Generate and verify an interface event."], ["Server receives Router0 messages", "Messages contain useful timestamps"], ["Syslog", "Cisco Syslog Configuration"]),
    LabSpec(16, "AAA", "Protect device login with local AAA and preserve a recovery path.", "1 router, 1 switch, 1 PC", ["Configure management IP connectivity.", "Create a local privileged user.", "Enable AAA and a local login method.", "Test a second session before closing the first."], ["Authorized user logs in", "Invalid login is rejected"], ["AAA", "Local AAA"], difficulty="Intermediate"),
    LabSpec(17, "SSH Remote Management", "Configure encrypted SSH-only VTY management.", "1 router, 1 switch, 1 PC", ["Set hostname and domain name.", "Create a local admin and RSA keys.", "Restrict VTY transport to SSH.", "Connect from PC1 and verify the session."], ["show ip ssh reports version 2", "SSH login succeeds", "Telnet is rejected"], ["SSH", "Cisco SSH Configuration"]),
    LabSpec(18, "ACL", "Use standard and extended ACLs to permit required traffic and block one defined flow.", "2 routers, 2 switches, 3 PCs, 1 server", ["Document the desired traffic matrix.", "Write the ACL in evaluation order.", "Apply it once in the correct direction.", "Test permitted and denied flows and inspect counters."], ["Allowed flows succeed", "Denied flow fails", "ACL hit counts increase"], ["ACL", "Extended ACL"], difficulty="Intermediate"),
    LabSpec(19, "NAT and PAT", "Translate private inside clients to an outside address with PAT.", "2 routers, 2 switches, 2 PCs, server", ["Build inside and outside networks.", "Verify routing before NAT.", "Mark interfaces and match inside sources.", "Generate traffic and inspect translations."], ["Inside client reaches outside server", "PAT translation appears"], ["NAT", "PAT"], difficulty="Intermediate"),
    LabSpec(20, "STP", "Build a switch triangle and verify deterministic root selection and failover.", "3 switches, 2 PCs", ["Create VLAN 10 trunks.", "Set primary and backup root priorities.", "Identify root, designated, and alternate roles.", "Fail the root path and verify reconvergence."], ["One redundant path is non-forwarding", "PC connectivity recovers after failure"], ["STP", "STP Configuration"]),
    LabSpec(21, "RSTP", "Compare rapid convergence with a redundant Rapid PVST+ topology.", "3 switches, 2 PCs", ["Enable rapid-pvst consistently.", "Configure root placement.", "Identify alternate ports.", "Measure observable convergence after a link failure."], ["Rapid mode appears in summary", "Alternate path forwards after failure"], ["RSTP", "RSTP vs STP"], difficulty="Intermediate"),
    LabSpec(22, "EtherChannel", "Bundle two switch links with LACP and carry VLAN trunks over Port-channel1.", "2 switches, 4 PCs", ["Configure identical member properties.", "Use active on one side and passive on the other.", "Configure Port-channel1 as a trunk.", "Verify bundle flags and test one member failure."], ["show etherchannel summary shows bundled members", "Traffic survives one member failure"], ["EtherChannel", "LACP"], difficulty="Intermediate"),
    LabSpec(23, "HSRP", "Provide a redundant virtual default gateway with active and standby routers.", "2 routers, 1 switch, 1 PC", ["Configure unique physical gateway addresses.", "Configure one shared virtual IP.", "Set priority and preempt.", "Fail the active router and verify takeover."], ["PC reaches virtual gateway", "Standby becomes active", "Preferred router reclaims active"], ["HSRP", "HSRP Configuration"], difficulty="Intermediate"),
    LabSpec(24, "Port Security", "Restrict an access port with sticky MAC learning and a defined violation action.", "1 switch, 2 PCs", ["Configure a static access port.", "Enable sticky learning and maximum addresses.", "Choose restrict or shutdown.", "Move a different PC to the port and inspect the result."], ["Authorized PC works", "Violation counter increases"], ["Switch Port Security", "Port Security Troubleshooting"]),
    LabSpec(25, "DHCP Snooping", "Block rogue DHCP offers and build trusted client bindings.", "2 switches, legitimate server, rogue server, 2 PCs", ["Enable snooping for the client VLAN.", "Trust only the legitimate server uplink.", "Leave endpoint and rogue ports untrusted.", "Compare client leases before and after protection."], ["Legitimate lease succeeds", "Rogue offer is blocked", "Binding table populates"], ["DHCP Snooping", "Dynamic ARP Inspection"], difficulty="Intermediate"),
    LabSpec(26, "FTP and TFTP", "Transfer a user file with FTP and back up a Cisco configuration with TFTP.", "1 router, 1 switch, Server0, 1 PC", ["Enable FTP and TFTP on Server0.", "Create an FTP user and test transfer.", "Copy the router running configuration to TFTP.", "Verify filenames and restore in a controlled test."], ["FTP upload/download works", "TFTP backup exists"], ["FTP", "Cisco Configuration Backup Using TFTP"]),
    LabSpec(27, "IPv6", "Address two IPv6 LANs and route between them.", "1 router, 2 switches, 2 PCs", ["Enable IPv6 unicast routing.", "Assign /64 prefixes to router LAN interfaces.", "Configure clients with static IPv6 or SLAAC.", "Inspect neighbor and route tables."], ["Clients reach their link-local gateway", "End-to-end IPv6 ping succeeds"], ["IPv6", "IPv6 SLAAC"], difficulty="Intermediate"),
    LabSpec(28, "Wireless Networking", "Build a secured WLAN and connect wireless clients to a local server.", "1 wireless router or AP, 2 wireless clients, server", ["Plan SSID and addressing.", "Configure WPA2 with a strong lab passphrase.", "Associate clients and obtain addresses.", "Verify radio, IP, and application connectivity separately."], ["Clients associate securely", "Clients receive correct addressing", "Server is reachable"], ["Wireless Networking", "WPA2"]),
    LabSpec(29, "Complete Enterprise Network", "Integrate hierarchical switching, routing, centralized services, security, monitoring, redundancy, and Internet simulation.", "Multiple routers, multilayer and access switches, VLANs, servers, endpoints, ISP", ["Create VLANs 10 Administration, 20 Staff, 30 Students, 40 IT, 50 Servers, and 99 Management.", "Build redundant trunks and EtherChannels with deterministic STP roots.", "Configure HSRP gateways and inter-VLAN routing.", "Run OSPF between routed infrastructure devices.", "Use dedicated DHCP server 200.100.10.5 with relay; do not create router pools.", "Add DNS, NTP, Syslog, SNMP, AAA, SSH, ACL, NAT/PAT, and port security.", "Document every interface, address, cable, and test."], ["Every VLAN receives correct DHCP", "DNS and web service work", "Routing survives one path failure", "HSRP and STP failover succeed", "Management and monitoring records are visible", "Internet simulation follows ACL and NAT policy"], ["Complete Enterprise Network Design", "Testing Matrix Template"], difficulty="Advanced", support="Partial"),
    LabSpec(30, "Network Troubleshooting Challenge", "Diagnose a deliberately broken enterprise topology without erasing configurations.", "Use a copy of Lab 29 with seeded faults", ["Record symptoms before changing anything.", "Use bottom-up and follow-the-path methods.", "Find faults across VLANs, trunks, routing, DHCP, DNS, ACL, NAT, STP, and management.", "Make one controlled repair at a time.", "Complete an evidence and verification report."], ["All required tests recover", "Every repair has evidence", "No unrelated configuration was deleted"], ["Network Troubleshooting Methodology", "Cisco Troubleshooting Commands"], difficulty="Advanced", support="Partial"),
]


def render_lab(lab: LabSpec) -> str:
    tasks = "\n".join(f"{i}. {task}" for i, task in enumerate(lab.tasks, 1))
    tests = "\n".join(f"| Test {i} | {test} | Success |" for i, test in enumerate(lab.tests, 1))
    links = "\n".join(f"- [[{name}]]" for name in lab.related)
    return frontmatter(lab.filename, "Packet Tracer Labs", lab.difficulty, lab.support,
                       lab.related, ["networking", "packet-tracer", "lab", "teaching"], "lab") + "\n\n" + clean(f"""
    # {lab.filename}

    > [!abstract]
    > {lab.objective}

    > [!info] Packet Tracer Support: {lab.support}
    > Confirm every required command on the selected Packet Tracer device model. Use GNS3, EVE-NG, Cisco CML, Wireshark, Linux, or real hardware when a listed feature is partial.

    ## 1. Learning Objectives

    - Explain the purpose of the technology before configuring it.
    - Build and address the topology from a documented plan.
    - Apply device-specific configuration in the correct mode.
    - Verify operation with commands and endpoint tests.
    - Diagnose one controlled failure without erasing the configuration.

    ## 2. Required Devices

    {lab.devices}

    ## 3. Topology

    ```text
    Endpoint(s) ---- Access/Distribution ---- Router or Service ---- Destination
           |                 |                       |
           +----------- verification points --------+
    ```

    Draw the exact port-to-port topology before cabling. Record any interface name that differs from the related configuration note.

    ## 4. Addressing and Interface Plan

    | Device | Interface | Address/VLAN | Connected to | Purpose |
    |---|---|---|---|---|
    | Complete before configuration | | | | |

    > [!important]
    > Validate every network address, mask, wildcard, VLAN, gateway, and next hop before entering IOS commands.

    ## 5. Implementation Tasks

    {tasks}

    ## 6. Configuration Rules

    1. Configure one device at a time and label every code block with the device name.
    2. Verify directly connected operation before adding routing, services, or security.
    3. Use `no shutdown` on required routed interfaces.
    4. Save only after the current stage passes its tests.
    5. Use the linked subject notes for verified command syntax and explanations.

    ## 7. Baseline Verification

    ```cisco
    show ip interface brief
    show interfaces status
    show vlan brief
    show interfaces trunk
    show ip route
    ```

    Run only the commands relevant to each device type.

    ## 8. Testing Matrix

    | Test | Requirement | Expected |
    |---|---|---|
    {tests}

    ## 9. Controlled Failure

    Select one cable, interface, route, VLAN, service, or policy directly related to the lab. Record the symptom, predict which verification output will change, introduce the fault, confirm the prediction, repair it, and repeat the testing matrix.

    ## 10. Troubleshooting Record

    | Symptom | Possible cause | Command/evidence | Fix | Verification |
    |---|---|---|---|---|
    | | | | | |

    ## 11. Student Exercise

    ### Beginner

    Complete the core implementation tasks with the addressing plan provided by the lecturer.

    ### Intermediate

    Change the addressing or VLAN plan while preserving the same functional requirements.

    ### Advanced

    Exchange a topology with another student, insert two documented faults, and troubleshoot without revealing the faults.

    ## 12. Lecturer Solution

    Use the related configuration notes and templates to build a validated reference solution. Keep the final device configurations hidden until students submit their topology, verification evidence, and fault report.

    ## 13. Viva Questions

    1. What user-visible problem does this lab solve?
    2. Which command provides the strongest proof of correct protocol state?
    3. Which wrong address, mask, VLAN, interface, or policy would cause the same symptom?
    4. What Packet Tracer limitation would require another platform?

    ## 14. Related Notes

    {links}
    - [[Networking Dashboard]]
    """) + "\n"


TEMPLATES = {
    "Basic Router Template": """enable
configure terminal
hostname <ROUTER-NAME>
enable secret <ENABLE-SECRET>
service password-encryption
banner motd #Authorized Access Only#
username <ADMIN-USER> privilege 15 secret <ADMIN-SECRET>
interface <INTERFACE>
 ip address <IP-ADDRESS> <SUBNET-MASK>
 no shutdown
exit
line console 0
 login local
exit
line vty 0 4
 login local
 transport input ssh
end
copy running-config startup-config""",
    "Basic Switch Template": """enable
configure terminal
hostname <SWITCH-NAME>
enable secret <ENABLE-SECRET>
service password-encryption
vlan <MANAGEMENT-VLAN>
 name MANAGEMENT
interface vlan <MANAGEMENT-VLAN>
 ip address <SWITCH-IP> <SUBNET-MASK>
 no shutdown
exit
ip default-gateway <GATEWAY>
end
copy running-config startup-config""",
    "Layer 3 Switch Template": """enable
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
copy running-config startup-config""",
    "VLAN Template": """enable
configure terminal
vlan <VLAN-ID>
 name <VLAN-NAME>
exit
interface <ACCESS-INTERFACE>
 switchport mode access
 switchport access vlan <VLAN-ID>
 no shutdown
end
copy running-config startup-config""",
    "Trunk Template": """enable
configure terminal
interface <TRUNK-INTERFACE>
 switchport mode trunk
 switchport trunk allowed vlan <VLAN-LIST>
 switchport trunk native vlan <NATIVE-VLAN>
 no shutdown
end
copy running-config startup-config""",
    "Router-on-a-Stick Template": """enable
configure terminal
interface <PHYSICAL-INTERFACE>
 no shutdown
interface <PHYSICAL-INTERFACE>.<VLAN-ID>
 encapsulation dot1Q <VLAN-ID>
 ip address <GATEWAY> <SUBNET-MASK>
end
copy running-config startup-config""",
    "Static Route Template": """enable
configure terminal
ip route <DESTINATION-NETWORK> <SUBNET-MASK> <NEXT-HOP>
ip route 0.0.0.0 0.0.0.0 <DEFAULT-NEXT-HOP>
end
copy running-config startup-config""",
    "RIP Template": """enable
configure terminal
router rip
 version 2
 no auto-summary
 network <CONNECTED-MAJOR-NETWORK>
end
copy running-config startup-config""",
    "OSPF Template": """enable
configure terminal
router ospf <PROCESS-ID>
 router-id <ROUTER-ID>
 network <NETWORK> <WILDCARD> area <AREA-ID>
end
copy running-config startup-config""",
    "DHCP Relay Template": """enable
configure terminal
interface <CLIENT-GATEWAY-INTERFACE>
 ip helper-address <DHCP-SERVER-IP>
 no shutdown
end
copy running-config startup-config""",
    "ACL Template": """enable
configure terminal
ip access-list extended <ACL-NAME>
 permit <PROTOCOL> <SOURCE> <SOURCE-WILDCARD> <DESTINATION> <DESTINATION-WILDCARD>
 deny ip any any log
exit
interface <INTERFACE>
 ip access-group <ACL-NAME> <in|out>
end
copy running-config startup-config""",
    "NAT Template": """enable
configure terminal
access-list 1 permit <INSIDE-NETWORK> <WILDCARD>
interface <INSIDE-INTERFACE>
 ip nat inside
interface <OUTSIDE-INTERFACE>
 ip nat outside
ip nat inside source list 1 interface <OUTSIDE-INTERFACE> overload
end
copy running-config startup-config""",
    "STP Template": """enable
configure terminal
spanning-tree mode rapid-pvst
spanning-tree vlan <VLAN-ID> root primary
spanning-tree vlan <BACKUP-VLAN-ID> root secondary
interface <EDGE-INTERFACE>
 spanning-tree portfast
 spanning-tree bpduguard enable
end
copy running-config startup-config""",
    "EtherChannel Template": """enable
configure terminal
interface range <MEMBER-INTERFACE-1> - <MEMBER-INTERFACE-2>
 channel-group <CHANNEL-ID> mode <active|passive|desirable|auto>
 no shutdown
interface port-channel <CHANNEL-ID>
 switchport mode trunk
 switchport trunk allowed vlan <VLAN-LIST>
end
copy running-config startup-config""",
    "HSRP Template": """enable
configure terminal
interface <GATEWAY-INTERFACE>
 ip address <PHYSICAL-IP> <SUBNET-MASK>
 standby <GROUP-ID> ip <VIRTUAL-IP>
 standby <GROUP-ID> priority <PRIORITY>
 standby <GROUP-ID> preempt
 standby <GROUP-ID> track <UPSTREAM-INTERFACE> <DECREMENT>
 no shutdown
end
copy running-config startup-config""",
    "SSH Template": """enable
configure terminal
hostname <HOSTNAME>
ip domain-name <DOMAIN-NAME>
username <ADMIN-USER> privilege 15 secret <ADMIN-SECRET>
crypto key generate rsa modulus 2048
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
end
copy running-config startup-config""",
    "AAA Template": """enable
configure terminal
aaa new-model
username <ADMIN-USER> privilege 15 secret <ADMIN-SECRET>
aaa authentication login default local
line vty 0 4
 login authentication default
 transport input ssh
end
copy running-config startup-config""",
    "NTP Template": """enable
configure terminal
clock timezone <ZONE> <HOURS-OFFSET> <MINUTES-OFFSET>
ntp server <NTP-SERVER-IP>
end
copy running-config startup-config""",
    "SNMP Template": """enable
configure terminal
snmp-server community <READ-COMMUNITY> ro
snmp-server location <LOCATION>
snmp-server contact <CONTACT>
snmp-server host <MANAGER-IP> version 2c <READ-COMMUNITY>
snmp-server enable traps
end
copy running-config startup-config""",
    "Syslog Template": """enable
configure terminal
service timestamps log datetime msec
logging <SYSLOG-SERVER-IP>
logging trap <SEVERITY>
end
copy running-config startup-config""",
}


TEMPLATE_RELATED = {
    "Basic Router Template": "Cisco Router Basic Configuration",
    "Basic Switch Template": "Cisco Switch Basic Configuration",
    "Layer 3 Switch Template": "Cisco Multilayer Switch Configuration",
    "Router-on-a-Stick Template": "Router on a Stick",
    "Static Route Template": "Static Routing",
    "Trunk Template": "Trunk Configuration",
}


def render_config_template(title: str, config: str) -> str:
    related_name = TEMPLATE_RELATED.get(title, title.removesuffix(" Template"))
    return frontmatter(title, "Configuration Templates", "Intermediate", "Yes",
                       [related_name, "Cisco Troubleshooting Commands"],
                       ["networking", "cisco", "configuration-template"], "template") + "\n\n" + clean(f"""
    # {title}

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
    {clean(config)}
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

    - [[{related_name}]]
    - [[Cisco Troubleshooting Commands]]
    - [[Networking Dashboard]]
    """) + "\n"


CHEAT_SHEETS = {
    "Cisco Show Commands Cheat Sheet": [
        ("show ip interface brief", "Compact Layer 3 interface state and addresses"),
        ("show interfaces status", "Switch port status, VLAN, duplex, and speed"),
        ("show vlan brief", "VLAN database and access-port membership"),
        ("show interfaces trunk", "Operational trunks and carried VLANs"),
        ("show spanning-tree vlan <ID>", "Root, roles, state, cost, and priority"),
        ("show etherchannel summary", "Bundle protocol and member flags"),
        ("show ip route", "IPv4 routing table"),
        ("show ip protocols", "Dynamic routing process settings"),
        ("show cdp neighbors detail", "Direct Cisco neighbor details"),
        ("show logging", "Logging destinations and buffered events"),
    ],
    "Cisco Routing Commands Cheat Sheet": [
        ("ip route <NET> <MASK> <NEXT-HOP>", "Create an IPv4 static route"),
        ("router rip", "Enter RIP configuration"),
        ("router ospf <PID>", "Start an OSPF process"),
        ("router eigrp <AS>", "Start classic EIGRP"),
        ("show ip route", "Verify installed routes"),
        ("show ip ospf neighbor", "Verify OSPF adjacencies"),
        ("show ip eigrp neighbors", "Verify EIGRP neighbors"),
        ("traceroute <IP>", "Display routed hop path"),
    ],
    "Cisco Switching Commands Cheat Sheet": [
        ("switchport mode access", "Force an access port"),
        ("switchport access vlan <ID>", "Assign the access VLAN"),
        ("switchport mode trunk", "Force a static trunk"),
        ("switchport trunk allowed vlan <LIST>", "Restrict trunk VLANs"),
        ("spanning-tree vlan <ID> root primary", "Prefer this switch as root"),
        ("channel-group <ID> mode active", "Create an LACP bundle"),
        ("show mac address-table", "Inspect learned MAC addresses"),
        ("show interfaces trunk", "Verify trunk state"),
    ],
    "Cisco Security Commands Cheat Sheet": [
        ("username <USER> privilege 15 secret <SECRET>", "Create protected local administrator"),
        ("transport input ssh", "Allow SSH on VTY lines"),
        ("show access-lists", "Inspect ACL entries and counters"),
        ("show port-security", "Inspect switch port security"),
        ("show ip dhcp snooping", "Inspect snooping state"),
        ("show ip arp inspection", "Inspect DAI state"),
        ("show ip nat translations", "Inspect NAT/PAT state"),
    ],
    "Cisco Troubleshooting Cheat Sheet": [
        ("show running-config", "Compare active configuration with design"),
        ("show ip interface brief", "Start with interface state"),
        ("show interfaces", "Inspect counters, duplex, and errors"),
        ("show arp", "Check IPv4-to-MAC resolution"),
        ("show mac address-table", "Follow Layer 2 learning"),
        ("show ip route", "Follow Layer 3 forwarding"),
        ("ping <IP>", "Test reachability"),
        ("traceroute <IP>", "Find the first failing routed hop"),
        ("show logging", "Correlate device events"),
    ],
    "Networking Port Numbers Cheat Sheet": [
        ("FTP TCP 20/21", "File data/control"), ("SSH TCP 22", "Encrypted administration"),
        ("Telnet TCP 23", "Legacy clear-text administration"), ("SMTP TCP 25", "Mail transfer"),
        ("DNS UDP/TCP 53", "Name resolution"), ("DHCP UDP 67/68", "Address leasing"),
        ("TFTP UDP 69", "Simple file transfer"), ("HTTP TCP 80", "Web"),
        ("POP3 TCP 110", "Mail retrieval"), ("NTP UDP 123", "Time synchronization"),
        ("IMAP TCP 143", "Mailbox synchronization"), ("SNMP UDP 161/162", "Management/traps"),
        ("HTTPS TCP 443", "Encrypted web"), ("Syslog UDP 514", "Traditional logging"),
        ("RADIUS UDP 1812/1813", "Authentication/accounting"),
    ],
    "Subnetting Cheat Sheet": [
        ("/8 255.0.0.0", "16,777,216 addresses"),
        ("/16 255.255.0.0", "65,536 addresses"),
        ("/23 255.255.254.0", "512 addresses, 510 traditional usable hosts"),
        ("/24 255.255.255.0", "256 addresses, 254 usable"),
        ("/25 255.255.255.128", "128 addresses, 126 usable"),
        ("/26 255.255.255.192", "64 addresses, 62 usable"),
        ("/27 255.255.255.224", "32 addresses, 30 usable"),
        ("/28 255.255.255.240", "16 addresses, 14 usable"),
        ("/29 255.255.255.248", "8 addresses, 6 usable"),
        ("/30 255.255.255.252", "4 addresses, 2 usable"),
    ],
}


def render_cheat_sheet(title: str, rows: list[tuple[str, str]]) -> str:
    table = "\n".join(f"| `{command}` | {purpose} |" for command, purpose in rows)
    return frontmatter(title, "Commands Cheat Sheets", "Beginner", "Yes",
                       ["Cisco Troubleshooting Commands", "Networking Dashboard"],
                       ["networking", "cheat-sheet", "teaching"], "cheat-sheet") + "\n\n" + clean(f"""
    # {title}

    > [!abstract]
    > Quick classroom reference. Confirm syntax with `?` on the selected IOS image before applying a command.

    | Command or value | Purpose |
    |---|---|
    {table}

    ## Use Safely

    - Start with read-only `show`, ping, or lookup commands.
    - Record the expected result before changing configuration.
    - Do not copy placeholders or example credentials into production.

    ## Related Notes

    - [[Cisco Troubleshooting Commands]]
    - [[Networking Dashboard]]
    """) + "\n"


VIVA_TOPICS = [
    "OSI Model", "TCP-IP Model", "IPv4 Addressing", "Subnetting Basics", "VLAN",
    "802.1Q Trunking", "Static Routing", "RIP", "OSPF", "DHCP", "DNS", "STP",
    "EtherChannel", "HSRP", "ACL", "NAT", "AAA", "SSH", "SNMP", "Syslog", "NTP",
    "IPv6", "Network Troubleshooting Methodology",
]

VIVA_FALLBACK = {
    "STP": ("STP prevents Layer 2 loops while retaining redundant paths.", "root bridge, root port, designated port, alternate port", "show spanning-tree vlan 10"),
    "HSRP": ("HSRP provides a virtual default gateway with active and standby Cisco routers.", "virtual IP, active, standby, priority, preempt", "show standby brief"),
    "SNMP": ("SNMP lets a manager poll agents and receive notifications through MIB objects.", "manager, agent, MIB, OID, trap", "show snmp"),
    "Syslog": ("Syslog sends timestamped event messages to local or remote logging destinations.", "facility, severity, mnemonic, timestamp", "show logging"),
    "NTP": ("NTP synchronizes device clocks to trusted time sources.", "client, server, stratum, association", "show ntp associations"),
}


def find_topic(title: str) -> Topic | None:
    return next((item for item in TOPICS if item.title == title), None)


def render_viva(topic_name: str) -> str:
    spec = find_topic(topic_name)
    if spec:
        summary = spec.summary
        terms = ", ".join(spec.points[:5]) or "the core terminology"
        verification = spec.verify[0] if spec.verify else "the relevant show command and an end-to-end test"
        layer = spec.layer
        ports = spec.ports
        support = spec.support
        related = spec.related[:3]
    else:
        summary, terms, verification = VIVA_FALLBACK[topic_name]
        layer, ports, support = "See the protocol overview", "See the protocol overview", "Yes"
        related = [topic_name, "Networking Dashboard"]

    beginner = [
        (f"What is {topic_name}?", summary),
        (f"Why is {topic_name} used?", "It provides predictable network behavior that can be designed, verified, and troubleshot rather than relying on accidental defaults."),
        (f"Which OSI layer is most closely associated with {topic_name}?", layer),
        (f"Which port or protocol number is important for {topic_name}?", ports),
        (f"Name two important {topic_name} terms.", terms),
        (f"Is {topic_name} supported in Packet Tracer?", f"Packet Tracer Support: {support}. Always confirm the selected model and image."),
        (f"What should be checked before configuring {topic_name}?", "Check cabling, interface state, addressing, VLANs, and baseline reachability first."),
        (f"Which command can help verify {topic_name}?", verification),
        (f"What is one common classroom mistake with {topic_name}?", "Students often use the correct command on the wrong interface or with values that do not match the topology plan."),
        (f"How should a student prove {topic_name} works?", "Show the relevant device state and then demonstrate the expected end-to-end traffic or service result."),
    ]
    intermediate = [
        (f"Describe the operational sequence for {topic_name}.", f"Follow these core ideas in order: {terms}. Explain the control information and resulting forwarding or service state."),
        (f"How would you design a small {topic_name} lab?", "Use the fewest devices that still expose the control exchange, one successful path, one verification point, and one controlled failure."),
        (f"How do you distinguish a {topic_name} fault from a physical fault?", "Verify link and interface state first. If Layer 1 is healthy, compare the technology-specific state and counters."),
        (f"How do you distinguish a {topic_name} fault from an IP addressing fault?", "Verify the local address, mask, gateway, and routing independently before interpreting protocol state."),
        (f"What output would you record before changing {topic_name}?", f"Record {verification}, interface state, relevant configuration, and an endpoint test."),
        (f"Why should only one variable be changed during {topic_name} troubleshooting?", "A controlled change preserves evidence and shows whether the tested theory was correct."),
        (f"What security concern applies to {topic_name}?", "Restrict infrastructure access, authenticate peers or managers where supported, use least privilege, and log changes."),
        (f"What Packet Tracer limitation can affect {topic_name}?", "Packet Tracer may omit advanced commands, packet details, scale, timers, cryptography, or production debug output."),
        (f"How would you document a working {topic_name} configuration?", "Record topology, interface and address tables, device-specific blocks, verification output, tests, and known platform limitations."),
        (f"How would you create a useful {topic_name} failure demonstration?", "Introduce one realistic fault, ask students to predict the changed output, verify the symptom, repair the cause, and retest."),
    ]
    advanced = [
        (f"How would {topic_name} change in a larger enterprise?", "Add hierarchy, redundancy, security policy, scale boundaries, centralized monitoring, configuration standards, and rollback planning."),
        (f"How would you validate {topic_name} during a change window?", "Capture a baseline, apply staged changes, run protocol and end-to-end tests, monitor logs, and execute rollback if acceptance criteria fail."),
        (f"Which hidden dependency can make {topic_name} appear correctly configured but still fail?", "Return routing, an upstream policy, time, name resolution, VLAN transport, or a platform capability can fail outside the local configuration."),
        (f"How would you secure and monitor {topic_name} in production?", "Use trusted peers, authentication and encryption where available, infrastructure ACLs, centralized logs, metrics, and alert thresholds."),
        (f"How would you teach {topic_name} without encouraging command memorization?", "Begin with the failure it solves, visualize the packet or state transition, have students predict output, then map each command to one design requirement."),
    ]

    def qblock(items: list[tuple[str, str]]) -> str:
        return "\n\n".join(f"### {i}. {question}\n\n**Answer:** {answer}" for i, (question, answer) in enumerate(items, 1))

    related_links = "\n".join(f"- [[{name}]]" for name in related)
    title = f"{topic_name} Viva Questions"
    return frontmatter(title, "Viva and Revision Questions", "Mixed", support,
                       [topic_name] + related, ["networking", "viva", "teaching"], "question-bank") + "\n\n" + clean(f"""
    # {title}

    > [!abstract]
    > 25 questions with answers: 10 beginner, 10 intermediate, and 5 advanced.

    ## Beginner Questions

    {qblock(beginner)}

    ## Intermediate Questions

    {qblock(intermediate)}

    ## Advanced Questions

    {qblock(advanced)}

    ## Related Notes

    - [[{topic_name}]]
    {related_links}
    """) + "\n"


APPENDICES = {
    "OSI Model": """
## Layer Reference Table

| Layer | Main function | Typical protocols/examples | PDU | Addressing/devices |
|---:|---|---|---|---|
| 7 Application | User and infrastructure services | HTTP, DNS, DHCP, SMTP, SNMP | Data | Servers, proxies, clients |
| 6 Presentation | Format, compression, encryption | TLS, encoding, serialization | Data | Hosts and applications |
| 5 Session | Establish and manage conversations | Session checkpoints, RPC concepts | Data | Hosts and applications |
| 4 Transport | End-to-end process delivery | TCP, UDP | Segment/datagram | Port numbers, firewalls |
| 3 Network | Logical addressing and routing | IPv4, IPv6, ICMP, OSPF | Packet | IP addresses, routers |
| 2 Data Link | Local framing and switching | Ethernet, 802.1Q, STP | Frame | MAC addresses, switches |
| 1 Physical | Signals, media, connectors | Copper, fiber, radio | Bits | Hubs, cabling, transceivers |
""",
    "Common Network Ports": """
## Required Port Reference

| Protocol | Port(s) | Transport |
|---|---:|---|
| FTP | 20/21 | TCP |
| SSH | 22 | TCP |
| Telnet | 23 | TCP |
| SMTP | 25 | TCP |
| DNS | 53 | UDP and TCP |
| DHCP | 67/68 | UDP |
| TFTP | 69 | UDP |
| HTTP | 80 | TCP |
| POP3 | 110 | TCP |
| NTP | 123 | UDP |
| IMAP | 143 | TCP |
| SNMP | 161/162 | UDP |
| HTTPS | 443 | TCP |
| Syslog | 514 | UDP in the Packet Tracer lab |
| RADIUS | 1812/1813 | UDP |
""",
    "Subnetting Step by Step": """
## Worked Examples

### 192.168.1.0/27

- Mask: `255.255.255.224`
- Block size: `32`
- First subnet: network `.0`, hosts `.1-.30`, broadcast `.31`
- Second subnet: network `.32`, hosts `.33-.62`, broadcast `.63`

### 200.100.10.0/28

- Mask: `255.255.255.240`
- Block size: `16`
- First subnet: network `.0`, hosts `.1-.14`, broadcast `.15`
- Next subnet begins at `.16`

### Address 172.16.20.140/23

- Mask: `255.255.254.0`
- Third-octet block size: `2`
- Network: `172.16.20.0`
- Usable range: `172.16.20.1-172.16.21.254`
- Broadcast: `172.16.21.255`
""",
    "RIP vs OSPF vs EIGRP": """
## Comparison Table

| Feature | RIP | OSPF | EIGRP |
|---|---|---|---|
| Type | Distance vector | Link state | Advanced distance vector |
| Algorithm | Bellman-Ford concepts | SPF/Dijkstra | DUAL |
| Metric | Hop count | Cost | Composite metric |
| Common AD | 120 | 110 | 90 internal |
| Convergence | Slow | Fast | Fast |
| Scale | Small | Medium to very large | Medium to large Cisco-oriented networks |
| Maximum | 15 routed hops | Area and LSDB design limits | Platform and design limits |
""",
}

APPENDICES["Lab 29 - Complete Enterprise Network"] = """
## 15. Validated Enterprise Reference Design

> [!important]
> This design intentionally uses the required teaching address `200.100.10.5` for DHCP. It is a classroom value, not a recommendation to use unassigned public space in production.

### 15.1 Logical topology

```mermaid
flowchart TB
ISP[ISP Router] --- EDGE[EDGE1]
EDGE --- D1[DSW1]
EDGE --- D2[DSW2]
D1 == LACP Port-channel1 == D2
D1 --- A1[ASW1]
D2 --- A1
D1 --- A2[ASW2]
D2 --- A2
A1 --- USERS[Administration / Staff / Students / IT]
A2 --- SERVERS[DHCP / DNS / NTP / Syslog / SNMP / AAA / Web]
```

### 15.2 Device list

| Device | Suggested Packet Tracer type | Role |
|---|---|---|
| ISP | Cisco ISR router | Internet simulation and test loopback |
| EDGE1 | Cisco 2911 or equivalent | OSPF edge, default route, NAT/PAT |
| DSW1, DSW2 | Cisco 3560 multilayer switches | SVIs, HSRP, OSPF, STP roots |
| ASW1, ASW2 | Cisco 2960 switches | User and server access |
| Seven Server-PT devices | Packet Tracer servers | Central services |
| Client PCs | Packet Tracer PCs | DHCP and policy tests |

### 15.3 VLAN and IP plan

| VLAN | Name | Subnet | HSRP gateway | DSW1 | DSW2 |
|---:|---|---|---|---|---|
| 10 | Administration | `192.168.10.0/24` | `192.168.10.1` | `.2` | `.3` |
| 20 | Staff | `192.168.20.0/24` | `192.168.20.1` | `.2` | `.3` |
| 30 | Students | `192.168.30.0/24` | `192.168.30.1` | `.2` | `.3` |
| 40 | IT | `192.168.40.0/24` | `192.168.40.1` | `.2` | `.3` |
| 50 | Servers | `200.100.10.0/24` | `200.100.10.1` | `.2` | `.3` |
| 99 | Management | `192.168.99.0/24` | `192.168.99.1` | `.2` | `.3` |

Routed links:

| Link | First address | Second address |
|---|---|---|
| EDGE1 G0/0 to DSW1 G0/1 | `10.255.0.1/30` | `10.255.0.2/30` |
| EDGE1 G0/1 to DSW2 G0/1 | `10.255.0.5/30` | `10.255.0.6/30` |
| ISP G0/0 to EDGE1 G0/2 | `203.0.113.1/30` | `203.0.113.2/30` |
| ISP Loopback0 | `198.51.100.1/32` | Internet test destination |

### 15.4 Cable and interface plan

| Connection | Interfaces | Cable/port mode |
|---|---|---|
| ISP to EDGE1 | `G0/0` to `G0/2` | Copper, routed |
| EDGE1 to DSW1 | `G0/0` to `G0/1` | Copper, routed |
| EDGE1 to DSW2 | `G0/1` to `G0/1` | Copper, routed |
| DSW1 to DSW2 | `F0/23-24` on both | Two copper links, LACP trunk |
| DSWs to ASW1 | DSW `G0/2`, ASW `G0/1-2` | Redundant trunks |
| DSWs to ASW2 | DSW `F0/21-22`, ASW `G0/1-2` | Redundant trunks |
| End devices | Access switch FastEthernet ports | Copper straight-through, access mode |

Confirm actual interfaces before configuration and adjust consistently if the chosen model differs.

## 16. Server Configuration

All servers use mask `255.255.255.0` and gateway `200.100.10.1`.

| Server | Address | Packet Tracer service |
|---|---|---|
| DHCP | `200.100.10.5` | DHCP On |
| DNS | `200.100.10.10` | DNS On |
| NTP | `200.100.10.15` | NTP On |
| Syslog | `200.100.10.20` | SYSLOG On |
| SNMP manager | `200.100.10.25` | MIB Browser/manager PC if preferred |
| AAA | `200.100.10.30` | AAA On; add infrastructure clients |
| Web | `200.100.10.40` | HTTP/HTTPS On |

### Dedicated DHCP pools

Create these pools on Server0; do not configure router DHCP pools.

| Pool | Network/mask | Default gateway | DNS | Start IP | Maximum users |
|---|---|---|---|---|---:|
| ADMIN | `192.168.10.0/24` | `192.168.10.1` | `200.100.10.10` | `192.168.10.21` | 200 |
| STAFF | `192.168.20.0/24` | `192.168.20.1` | `200.100.10.10` | `192.168.20.21` | 200 |
| STUDENTS | `192.168.30.0/24` | `192.168.30.1` | `200.100.10.10` | `192.168.30.21` | 200 |
| IT | `192.168.40.0/24` | `192.168.40.1` | `200.100.10.10` | `192.168.40.21` | 200 |

Create DNS record `intranet.network.lab` pointing to `200.100.10.40`.

## 17. EDGE1 Full Configuration

```cisco
enable
configure terminal
hostname EDGE1
ip domain-name network.lab
username admin privilege 15 secret <STRONG-SECRET>
crypto key generate rsa modulus 2048
ip ssh version 2

interface gigabitEthernet 0/0
 description TO-DSW1
 ip address 10.255.0.1 255.255.255.252
 ip nat inside
 no shutdown
interface gigabitEthernet 0/1
 description TO-DSW2
 ip address 10.255.0.5 255.255.255.252
 ip nat inside
 no shutdown
interface gigabitEthernet 0/2
 description TO-ISP
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
 no shutdown

access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface gigabitEthernet 0/2 overload
ip route 0.0.0.0 0.0.0.0 203.0.113.1

router ospf 1
 router-id 3.3.3.3
 network 10.255.0.0 0.0.0.3 area 0
 network 10.255.0.4 0.0.0.3 area 0
 default-information originate

ntp server 200.100.10.15
service timestamps log datetime msec
logging 200.100.10.20
logging trap informational
snmp-server community TEACHING-RO ro
snmp-server location Enterprise-Lab
snmp-server contact Lecturer

line vty 0 4
 login local
 transport input ssh
end
copy running-config startup-config
```

## 18. ISP Full Configuration

```cisco
enable
configure terminal
hostname ISP
interface gigabitEthernet 0/0
 description TO-EDGE1
 ip address 203.0.113.1 255.255.255.252
 no shutdown
interface loopback 0
 ip address 198.51.100.1 255.255.255.255
ip route 200.100.10.0 255.255.255.0 203.0.113.2
end
copy running-config startup-config
```

## 19. DSW1 Full Configuration

```cisco
enable
configure terminal
hostname DSW1
ip routing
spanning-tree mode rapid-pvst
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 40
 name IT
vlan 50
 name SERVERS
vlan 99
 name MANAGEMENT

interface gigabitEthernet 0/1
 no switchport
 ip address 10.255.0.2 255.255.255.252
 no shutdown
interface gigabitEthernet 0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface fastEthernet 0/21
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface range fastEthernet 0/23 - 24
 channel-group 1 mode active
 no shutdown
interface port-channel 1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99

interface vlan 10
 ip address 192.168.10.2 255.255.255.0
 standby 10 ip 192.168.10.1
 standby 10 priority 110
 standby 10 preempt
 ip helper-address 200.100.10.5
interface vlan 20
 ip address 192.168.20.2 255.255.255.0
 standby 20 ip 192.168.20.1
 standby 20 priority 100
 standby 20 preempt
 ip helper-address 200.100.10.5
interface vlan 30
 ip address 192.168.30.2 255.255.255.0
 standby 30 ip 192.168.30.1
 standby 30 priority 110
 standby 30 preempt
 ip helper-address 200.100.10.5
 ip access-group STUDENT-IN in
interface vlan 40
 ip address 192.168.40.2 255.255.255.0
 standby 40 ip 192.168.40.1
 standby 40 priority 100
 standby 40 preempt
 ip helper-address 200.100.10.5
interface vlan 50
 ip address 200.100.10.2 255.255.255.0
 standby 50 ip 200.100.10.1
 standby 50 priority 110
 standby 50 preempt
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 standby 99 ip 192.168.99.1
 standby 99 priority 100
 standby 99 preempt

ip access-list extended STUDENT-IN
 deny ip 192.168.30.0 0.0.0.255 192.168.10.0 0.0.0.255
 permit ip any any

spanning-tree vlan 10,30,50 root primary
spanning-tree vlan 20,40,99 root secondary
router ospf 1
 router-id 1.1.1.1
 passive-interface default
 no passive-interface gigabitEthernet 0/1
 network 10.255.0.0 0.0.0.3 area 0
 network 192.168.0.0 0.0.255.255 area 0
 network 200.100.10.0 0.0.0.255 area 0

ntp server 200.100.10.15
logging 200.100.10.20
snmp-server community TEACHING-RO ro
end
copy running-config startup-config
```

## 20. DSW2 Configuration Differences

Use the complete DSW1 block with these deliberate replacements; every unlisted VLAN, trunk, ACL, helper, NTP, Syslog, and SNMP line remains identical.

| Item | DSW2 value |
|---|---|
| Hostname | `DSW2` |
| Routed uplink | `G0/1 = 10.255.0.6/30` |
| OSPF router ID | `2.2.2.2` |
| OSPF transit network | `10.255.0.4 0.0.0.3 area 0` |
| SVI physical address | Use `.3` instead of `.2` |
| Priority 110 | VLANs 20, 40, 99 |
| Priority 100 | VLANs 10, 30, 50 |
| STP root primary | VLANs 20, 40, 99 |
| STP root secondary | VLANs 10, 30, 50 |

This alignment keeps the HSRP active gateway on the same distribution switch as the STP root for each VLAN.

## 21. ASW1 Full Configuration

```cisco
enable
configure terminal
hostname ASW1
spanning-tree mode rapid-pvst
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 40
 name IT
vlan 50
 name SERVERS
vlan 99
 name MANAGEMENT
interface gigabitEthernet 0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface gigabitEthernet 0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface range fastEthernet 0/1 - 4
 switchport mode access
 switchport access vlan 10
interface range fastEthernet 0/5 - 8
 switchport mode access
 switchport access vlan 20
interface range fastEthernet 0/9 - 12
 switchport mode access
 switchport access vlan 30
interface range fastEthernet 0/13 - 16
 switchport mode access
 switchport access vlan 40
interface range fastEthernet 0/1 - 16
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation restrict
interface vlan 99
 ip address 192.168.99.11 255.255.255.0
 no shutdown
ip default-gateway 192.168.99.1
end
copy running-config startup-config
```

## 22. ASW2 Full Configuration

```cisco
enable
configure terminal
hostname ASW2
spanning-tree mode rapid-pvst
vlan 10
 name ADMINISTRATION
vlan 20
 name STAFF
vlan 30
 name STUDENTS
vlan 40
 name IT
vlan 50
 name SERVERS
vlan 99
 name MANAGEMENT
interface gigabitEthernet 0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface gigabitEthernet 0/2
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
interface range fastEthernet 0/1 - 7
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
interface vlan 99
 ip address 192.168.99.12 255.255.255.0
 no shutdown
ip default-gateway 192.168.99.1
end
copy running-config startup-config
```

## 23. Client Configuration

Set user PCs to **DHCP**. Verify that each client receives an address from its VLAN pool, the correct HSRP gateway, and DNS server `200.100.10.10`.

Use static management addresses for infrastructure devices and static addresses for all servers.

## 24. Enterprise Acceptance Matrix

| Test | Source | Destination | Expected |
|---|---|---|---|
| DHCP | Each user VLAN | `200.100.10.5` | Correct lease through relay |
| DNS | User PC | `intranet.network.lab` | Resolves to `200.100.10.40` |
| Inter-VLAN | Administration PC | Staff PC | Success |
| Student policy | Student PC | Administration PC | Denied |
| Web | User PC | `200.100.10.40` | Page loads |
| NTP | EDGE1 and DSWs | `200.100.10.15` | Synchronized |
| Syslog | Infrastructure | `200.100.10.20` | Events received |
| SNMP | Manager `.25` | Infrastructure | System OIDs returned |
| OSPF | DSW1/DSW2 | EDGE1 | Full neighbors and routes |
| PAT | Private user VLAN | `198.51.100.1` | Success with translation |
| Server Internet | Web server | `198.51.100.1` | Success through routed public classroom subnet |
| HSRP | Client | VLAN virtual gateway | Survives active DSW failure |
| STP | PC on ASW1 | Server on ASW2 | Survives one trunk failure |
| EtherChannel | DSW1 | DSW2 | Survives one member failure |

## 25. Enterprise Troubleshooting Order

1. Verify physical links and interface state.
2. Verify VLAN creation, access membership, trunks, EtherChannel, and STP.
3. Verify SVIs, HSRP roles, helper addresses, and ACL placement.
4. Verify routed uplinks and OSPF neighbors/routes.
5. Verify each central service by IP before testing by name.
6. Verify NAT only after inside-to-edge routing works.
7. Test one redundancy failure at a time and allow convergence.
8. Record evidence in [[Testing Matrix Template]].
"""


def render_moc(title: str, description: str, items: list[str]) -> str:
    links = "\n".join(f"- [[{item}]]" for item in items)
    return frontmatter(title, "Dashboard", "Mixed", "Yes", items[:8],
                       ["networking", "moc", "teaching"], "map-of-content") + "\n\n" + clean(f"""
    # {title}

    > [!abstract]
    > {description}

    ## Teaching Sequence

    {links}

    ## Lecturer Workflow

    1. Start with the concept note.
    2. Demonstrate the control exchange or forwarding path.
    3. Use the configuration note or template.
    4. Complete the Packet Tracer lab.
    5. Introduce one fault and use the troubleshooting guide.
    6. Finish with the viva bank and quick revision.

    ## Related Navigation

    - [[Networking Dashboard]]
    - [[Networking Learning Roadmap]]
    - [[Network Protocol Master Index]]
    """) + "\n"


MOCS = {
    "Switching MOC": ("Switching, VLAN, trunking, spanning tree, EtherChannel, and inter-VLAN routing teaching path.", ["Ethernet", "MAC Addressing", "VLAN", "VLAN Configuration", "802.1Q Trunking", "Trunk Configuration", "STP", "RSTP", "PortFast", "BPDU Guard", "EtherChannel", "LACP", "Router on a Stick", "Layer 3 Switch Inter-VLAN Routing"]),
    "Routing MOC": ("IPv4 routing progression from gateways and static routes through RIP, OSPF, and EIGRP.", ["IPv4 Addressing", "Default Gateway", "Static Routing", "Default Route", "Floating Static Route", "RIP", "RIPv2 Configuration", "OSPF", "OSPF Single Area", "OSPF Multi Area", "EIGRP", "RIP vs OSPF vs EIGRP"]),
    "Security MOC": ("Secure management, AAA, traffic policy, translation, and Layer 2 access protections.", ["SSH", "Cisco SSH Configuration", "AAA", "RADIUS", "TACACS+", "ACL", "Standard ACL", "Extended ACL", "NAT", "PAT", "Switch Port Security", "DHCP Snooping", "Dynamic ARP Inspection", "IP Source Guard"]),
    "Network Services MOC": ("Address, name, time, file, web, email, logging, and management services.", ["DHCP", "Dedicated DHCP Server", "DHCP Relay", "DNS", "NTP", "FTP", "TFTP", "HTTP", "HTTPS", "SNMP", "Syslog", "Network Monitoring"]),
    "Troubleshooting MOC": ("Layered methodology, Cisco evidence commands, packet capture, and common fault guides.", ["Network Troubleshooting Methodology", "Cisco Troubleshooting Method", "OSI Troubleshooting", "Cisco Troubleshooting Commands", "Packet Capture", "PC Cannot Get DHCP Address", "PC Cannot Ping Gateway", "VLAN Communication Failure", "OSPF Neighbour Not Forming", "ACL Blocking Traffic", "NAT Not Working"]),
}


PROTOCOL_INDEX = clean("""
---
title: "Network Protocol Master Index"
category: "Dashboard"
difficulty: "Mixed"
packet_tracer_supported: "Mixed"
related_protocols: []
tags:
  - networking
  - moc
  - teaching
type: "master-index"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# Network Protocol Master Index

> [!abstract]
> Layered index that distinguishes protocols, services, Cisco technologies, security mechanisms, and general network features.

## Layer 2

- [[Ethernet]]
- [[ARP]]
- [[STP]]
- [[RSTP]]
- [[LACP]]
- [[PAgP]]
- [[CDP]]
- [[LLDP]]
- [[802.1Q Trunking]]

## Layer 3

- [[IPv4 Addressing]]
- [[IPv6]]
- [[ICMP]]
- [[OSPF]]
- [[RIP]]
- [[EIGRP]]
- [[IPsec]]
- [[GRE Tunnel]]

## Transport

- [[TCP]]
- [[UDP]]

## Application and Services

- [[DHCP]]
- [[DNS]]
- [[HTTP]]
- [[HTTPS]]
- [[FTP]]
- [[TFTP]]
- [[SSH]]
- [[Telnet]]
- [[SMTP]]
- [[POP3]]
- [[IMAP]]
- [[SNMP]]
- [[NTP]]
- [[Syslog]]
- [[RADIUS]]
- [[TACACS+]]

## High Availability

- [[HSRP]]
- [[VRRP]]
- [[GLBP]]

## Security Mechanisms

- [[ACL]]
- [[NAT]]
- [[Switch Port Security]]
- [[DHCP Snooping]]
- [[Dynamic ARP Inspection]]
- [[IP Source Guard]]
- [[AAA]]

## Classification Reminder

| Class | Examples |
|---|---|
| Protocol | OSPF, TCP, DNS, STP |
| Network service | DHCP, NTP, Syslog |
| Cisco technology | HSRP, CDP, PAgP |
| Security mechanism | ACL, DAI, port security |
| Network feature | NAT, EtherChannel, SVI |

---

**Home:** [[Networking Dashboard]]
""") + "\n"


ROADMAP = clean("""
---
title: "Networking Learning Roadmap"
category: "Dashboard"
difficulty: "Mixed"
packet_tracer_supported: "Mixed"
related_protocols: []
tags:
  - networking
  - roadmap
  - teaching
type: "roadmap"
status: "active"
created: "2026-08-11"
updated: "2026-08-11"
---

# Networking Learning Roadmap

> [!abstract]
> Recommended progression from first principles to integrated enterprise troubleshooting.

```mermaid
flowchart LR
F[Fundamentals] --> A[Addressing] --> S[Switching] --> R[Routing] --> N[Services] --> SEC[Security] --> HA[High Availability] --> M[Management] --> ADV[Advanced] --> T[Troubleshooting]
```

## Stage 1 - Fundamentals

1. [[OSI Model]]
2. [[TCP-IP Model]]
3. [[Ethernet]]
4. [[MAC Addressing]]
5. [[ARP]]
6. [[IPv4 Addressing]]
7. [[ICMP]]
8. [[TCP]]
9. [[UDP]]

## Stage 2 - Addressing

10. [[Subnet Mask]]
11. [[Subnetting Basics]]
12. [[CIDR]]
13. [[VLSM]]

## Stage 3 - Switching

14. [[VLAN]]
15. [[VLAN Configuration]]
16. [[802.1Q Trunking]]
17. [[STP]]
18. [[RSTP]]
19. [[EtherChannel]]

## Stage 4 - Routing

20. [[Router on a Stick]]
21. [[Static Routing]]
22. [[RIP]]
23. [[OSPF]]
24. [[EIGRP]]

## Stage 5 - Services

25. [[DHCP]]
26. [[DNS]]
27. [[NTP]]
28. [[FTP]] and [[TFTP]]
29. [[HTTP]] and [[HTTPS]]

## Stage 6 - Security

30. [[SSH]]
31. [[AAA]]
32. [[ACL]]
33. [[Switch Port Security]]
34. [[DHCP Snooping]]
35. [[Dynamic ARP Inspection]]
36. [[NAT]]

## Stage 7 - High Availability

37. [[HSRP]]
38. [[VRRP]]
39. [[EtherChannel]] redundancy

## Stage 8 - Management

40. [[SNMP]]
41. [[Syslog]]
42. [[CDP]]
43. [[LLDP]]
44. [[Wireshark]]

## Stage 9 - Advanced

45. [[IPv6]]
46. [[VPN]]
47. [[IPsec]]
48. [[GRE Tunnel]]
49. [[PPP]]

## Stage 10 - Troubleshooting

50. [[Network Troubleshooting Methodology]]
51. [[Cisco Troubleshooting Commands]]
52. [[Packet Capture]]
53. [[Lab 30 - Network Troubleshooting Challenge]]

---

**Home:** [[Networking Dashboard]]
""") + "\n"


def render_dashboard() -> str:
    folder_links = "\n".join(
        f"- [[Index - {folder.split(' - ', 1)[1]}|{folder}]]" for folder in FOLDERS
    )
    return frontmatter("Networking Dashboard", "Dashboard", "Mixed", "Mixed", [],
                       ["networking", "dashboard", "teaching"], "dashboard") + "\n\n" + clean(f"""
    # Networking Dashboard

    > [!abstract]
    > Main navigation for the complete Cisco networking teaching, Packet Tracer lab, revision, viva, and troubleshooting vault.

    ## Start Here

    - [[Networking Learning Roadmap]] - recommended teaching and study sequence.
    - [[Network Protocol Master Index]] - protocols and technologies by layer and function.
    - [[How to Use This Teaching Vault]] - lecturer and student workflow.
    - [[Lab 29 - Complete Enterprise Network]] - integrated capstone.
    - [[Lab 30 - Network Troubleshooting Challenge]] - final practical challenge.

    ## Maps of Content

    - [[Switching MOC]]
    - [[Routing MOC]]
    - [[Security MOC]]
    - [[Network Services MOC]]
    - [[Troubleshooting MOC]]

    ## Folder Navigation

    {folder_links}

    ## Teaching Philosophy

    Every major subject should answer:

    ```text
    WHAT it is
    WHY it is needed
    WHERE it is used
    HOW it works
    HOW to configure it
    HOW to verify it
    HOW it fails
    HOW to troubleshoot it
    ```

    ## Platform Legend

    | Value | Meaning |
    |---|---|
    | Yes | Packet Tracer demonstrates the essential behavior |
    | Partial | Use Packet Tracer for basics and another platform for missing depth |
    | No | Use GNS3, EVE-NG, Cisco CML, Linux, Wireshark, or real hardware |

    ## Quick Classroom Links

    - [[Cisco Show Commands Cheat Sheet]]
    - [[Networking Port Numbers Cheat Sheet]]
    - [[Subnetting Cheat Sheet]]
    - [[Cisco Troubleshooting Cheat Sheet]]
    - [[Practical Examination Template]]
    - [[Viva Session Guide]]
    """) + "\n"


MANUAL_NOTES = {
    "How to Use This Teaching Vault": ("The vault supports lesson preparation, demonstrations, labs, revision, assessment, viva practice, and troubleshooting.", """
## Lecturer Workflow

1. Select a stage in [[Networking Learning Roadmap]].
2. Open the subject through its MOC or folder index.
3. Teach WHAT, WHY, WHERE, and HOW before showing commands.
4. Demonstrate the related configuration and verification.
5. Assign the Packet Tracer lab without revealing the lecturer solution.
6. Use the viva bank and troubleshooting guide for assessment.

## Student Workflow

1. Read the concept note and create a one-page summary.
2. Predict the packet or protocol sequence.
3. Complete the lab and save verification evidence.
4. Break one controlled item and repair it.
5. Answer the beginner, intermediate, and advanced viva questions.

## Maintenance Rules

- Keep one canonical note per exact title.
- Cross-link theory, configuration, lab, troubleshooting, cheat sheet, and viva notes.
- Validate commands on the selected device model.
- Record Packet Tracer limitations explicitly.
- Never publish example passwords or community strings as production values.
"""),
    "Lesson Plan Template": ("Reusable plan for one networking lesson and practical demonstration.", """
## Lesson Details

| Field | Entry |
|---|---|
| Topic | |
| Audience | Beginner / Intermediate / Advanced |
| Duration | |
| Prerequisites | |
| Packet Tracer file | |

## Outcomes

- Explain the problem and terminology.
- Predict the protocol or forwarding sequence.
- Configure and verify the required behavior.
- Diagnose one common fault.

## Sequence

1. Hook: user-visible failure or design question.
2. Diagram: packet path or state transition.
3. Demonstration: correct configuration.
4. Guided practice: students reproduce one stage.
5. Fault: lecturer introduces one mistake.
6. Assessment: exit questions and verification evidence.
"""),
    "Practical Examination Template": ("Reusable Cisco Packet Tracer practical examination with objective marking evidence.", """
## Candidate Instructions

- Do not erase configurations unless instructed.
- Label devices and links.
- Save all device configurations.
- Submit the Packet Tracer file and verification evidence.

## Tasks

| Task | Requirement | Marks |
|---|---|---:|
| Addressing | Correct unique addresses, masks, and gateways | 15 |
| Switching | VLANs, access ports, trunks, and STP | 20 |
| Routing | Correct routes and adjacencies | 20 |
| Services | Required server/client behavior | 15 |
| Security | Management and traffic policy | 15 |
| Verification | Commands and testing matrix | 10 |
| Documentation | Labels and saved configuration | 5 |

## Examiner Faults

Insert faults only after saving a clean reference copy. Record the intended symptom, diagnostic evidence, and accepted repair.
"""),
    "Viva Session Guide": ("A consistent method for conducting fair beginner, intermediate, and advanced networking viva sessions.", """
## Format

1. Start with one definition question.
2. Ask the student to draw or explain a packet path.
3. Show one command output and request interpretation.
4. Present one fault symptom and ask for the first three checks.
5. Finish with one design or security trade-off.

## Scoring

| Level | Evidence |
|---|---|
| Beginner | Correct terminology and purpose |
| Intermediate | Correct configuration and verification reasoning |
| Advanced | Design, failure analysis, security, and trade-offs |

Use the topic-specific question banks in [[Index - Viva and Revision Questions]].
"""),
    "Packet Tracer Demonstration Guide": ("A repeatable method for clear Packet Tracer classroom demonstrations.", """
## Before Class

- Build a clean reference file and a separate broken copy.
- Confirm device models support every command.
- Label interfaces, VLANs, and subnets.
- Prepare expected output screenshots or text.

## During Class

1. Show the topology and addressing table.
2. Configure one device at a time.
3. Explain every important command.
4. Verify after each layer.
5. Use Simulation Mode for ARP, ICMP, DHCP, DNS, STP, and routing messages.

## Common Mistakes

- Selecting the wrong interface.
- Forgetting `no shutdown`.
- Testing before links converge.
- Mismatching VLAN or trunk settings.
- Assuming all production IOS commands exist in Packet Tracer.
"""),
    "Student Exercise Design Guide": ("Guidance for creating three-level exercises without exposing the solution too early.", """
## Beginner

Provide the topology, addressing table, and exact functional target. Require configuration and verification.

## Intermediate

Provide requirements but require students to create part of the addressing, VLAN, or routing plan.

## Advanced

Provide business requirements, redundancy, security, and faults. Require a design justification and testing matrix.

## Lecturer Solution

Store the validated configuration after the student task section. Hide or distribute it separately during assessment.
"""),
    "Assessment Rubric": ("Common rubric for Packet Tracer labs, practical examinations, and troubleshooting reports.", """
## Rubric

| Criterion | Excellent | Competent | Needs improvement |
|---|---|---|---|
| Design | Consistent, scalable, documented | Functional with minor omissions | Inconsistent or incomplete |
| Configuration | Correct device, mode, and values | Mostly correct | Commands copied without design match |
| Verification | Multiple protocol and end-to-end proofs | Basic proof | Claims without evidence |
| Troubleshooting | Theory, evidence, controlled fix | Finds and repairs fault | Deletes or guesses |
| Security | Least privilege and safe management | Basic controls | Insecure defaults |
| Communication | Clear tables, labels, and explanation | Understandable | Ambiguous or missing |
"""),
}


def render_manual(title: str, summary: str, body: str) -> str:
    return frontmatter(title, "Teaching Materials", "Mixed", "Yes",
                       ["Networking Dashboard", "Networking Learning Roadmap"],
                       ["networking", "teaching"], "teaching-material") + "\n\n" + clean(f"""
    # {title}

    > [!abstract]
    > {summary}

    {clean(body)}

    ## Related Notes

    - [[Networking Dashboard]]
    - [[Networking Learning Roadmap]]
    """) + "\n"


def render_folder_index(folder: str) -> str:
    folder_path = VAULT / folder
    label = folder.split(" - ", 1)[1]
    index_title = f"Index - {label}"
    notes = sorted(
        path.stem for path in folder_path.glob("*.md")
        if path.stem != index_title
    )
    links = "\n".join(f"- [[{name}]]" for name in notes) or "- No notes yet."
    return frontmatter(index_title, label, "Mixed", "Mixed", notes[:10],
                       ["networking", "index", "teaching"], "folder-index") + "\n\n" + clean(f"""
    # {index_title}

    > [!abstract]
    > Index for the **{label}** section of the teaching vault.

    ## Notes

    {links}

    ## Navigation

    - [[Networking Dashboard]]
    - [[Networking Learning Roadmap]]
    - [[Network Protocol Master Index]]
    """) + "\n"


LINK_REPLACEMENTS = {
    "Network Notes Home": "Networking Dashboard",
    "00 - NTP Overview": "NTP",
    "10 - NTP Packet Tracer Configuration": "Lab 13 - NTP Server",
    "00 - Syslog Overview": "Syslog",
    "10 - Syslog Packet Tracer Configuration": "Lab 15 - Syslog Server",
    "00 - SNMP Overview": "SNMP",
    "10 - SNMP Packet Tracer Configuration": "Lab 14 - SNMP Monitoring",
    "00 - HSRP Overview": "HSRP",
    "10 - HSRP Packet Tracer Configuration": "Lab 23 - HSRP",
    "00 - STP Overview": "STP",
    "10 - STP Packet Tracer Configuration": "Lab 20 - STP",
}


def repair_links_and_frontmatter(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    for old, new in LINK_REPLACEMENTS.items():
        content = content.replace(f"[[{old}", f"[[{new}")

    relative = path.relative_to(VAULT)
    category = relative.parts[0].split(" - ", 1)[-1]
    default_support = "Partial" if relative.parts[0].startswith(("11", "20")) else "Yes"

    if not content.startswith("---\n"):
        content = frontmatter(path.stem, category, "Mixed", default_support, [],
                              tags_for(relative.parts[0], path.stem)) + "\n\n" + content
    else:
        closing = content.find("\n---", 4)
        if closing == -1:
            raise ValueError(f"Unclosed frontmatter: {path}")
        fm = content[4:closing]
        additions = []
        if not re.search(r"(?m)^category:", fm):
            additions.append(f"category: {yaml_scalar(category)}")
        if not re.search(r"(?m)^difficulty:", fm):
            additions.append('difficulty: "Mixed"')
        if not re.search(r"(?m)^packet_tracer_supported:", fm):
            additions.append(f'packet_tracer_supported: "{default_support}"')
        if not re.search(r"(?m)^related_protocols:", fm):
            additions.append("related_protocols: []")
        if not re.search(r"(?m)^tags:", fm):
            additions.extend(["tags:", "  - networking", "  - teaching"])
        if additions:
            content = content[:closing] + "\n" + "\n".join(additions) + content[closing:]
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def append_once(path: Path, content: str, marker: str) -> None:
    current = path.read_text(encoding="utf-8")
    if marker not in current:
        path.write_text(current.rstrip() + "\n\n" + clean(content) + "\n", encoding="utf-8", newline="\n")


TESTING_MATRIX_TEMPLATE = frontmatter(
    "Testing Matrix Template", "Configuration Templates", "Mixed", "Yes",
    ["Lab 29 - Complete Enterprise Network", "Network Troubleshooting Methodology"],
    ["networking", "testing", "configuration-template"], "template"
) + "\n\n" + clean("""
# Testing Matrix Template

> [!abstract]
> Record the source, destination, expected result, actual result, and evidence for every important service and failure path.

| Test | Source | Destination | Expected | Actual | Evidence |
|---|---|---|---|---|---|
| Local gateway | PC1 | VLAN gateway | Success | | |
| Inter-VLAN | VLAN10 PC | VLAN20 PC | Success or policy deny | | |
| DHCP | Client | DHCP server | Correct lease | | |
| DNS | Client | Server name | Resolves | | |
| NTP | Router | NTP server | Synchronized | | |
| Syslog | Device | Syslog server | Message received | | |
| SNMP | Manager | Agent | OID returned | | |
| Routing | Branch LAN | Data-center LAN | Success | | |
| Internet | Inside PC | ISP test server | Success through PAT | | |
| HSRP failover | Client | Virtual gateway | Recovers | | |
| STP failover | PC1 | PC2 | Recovers | | |

## Acceptance Rule

Do not mark a service complete from configuration alone. Record protocol state and an end-to-end result.
""") + "\n"


def main() -> None:
    for folder in FOLDERS:
        (VAULT / folder).mkdir(parents=True, exist_ok=True)

    preserved = {
        "NTP", "SNMP", "Syslog", "HSRP", "STP",
        "Lab 13 - NTP Server", "Lab 14 - SNMP Monitoring",
        "Lab 15 - Syslog Server", "Lab 20 - STP", "Lab 23 - HSRP",
        "Networking Note Template",
    }

    for spec in TOPICS:
        path = VAULT / spec.folder / f"{spec.title}.md"
        write(path, render_topic(spec), overwrite=path.stem not in preserved)

    for lab in LABS:
        path = VAULT / "15 - Packet Tracer Labs" / f"{lab.filename}.md"
        write(path, render_lab(lab), overwrite=path.stem not in preserved)

    for title, config in TEMPLATES.items():
        write(VAULT / "16 - Configuration Templates" / f"{title}.md",
              render_config_template(title, config), overwrite=True)
    write(VAULT / "16 - Configuration Templates" / "Testing Matrix Template.md",
          TESTING_MATRIX_TEMPLATE, overwrite=True)

    for title, rows in CHEAT_SHEETS.items():
        write(VAULT / "17 - Commands Cheat Sheets" / f"{title}.md",
              render_cheat_sheet(title, rows), overwrite=True)

    for viva_topic in VIVA_TOPICS:
        write(VAULT / "18 - Viva and Revision Questions" / f"{viva_topic} Viva Questions.md",
              render_viva(viva_topic), overwrite=True)

    for title, (summary, body) in MANUAL_NOTES.items():
        write(VAULT / "19 - Teaching Materials" / f"{title}.md",
              render_manual(title, summary, body), overwrite=True)

    write(VAULT / "00 - Dashboard" / "Networking Dashboard.md", render_dashboard(), overwrite=True)
    write(VAULT / "00 - Dashboard" / "Network Protocol Master Index.md", PROTOCOL_INDEX, overwrite=True)
    write(VAULT / "00 - Dashboard" / "Networking Learning Roadmap.md", ROADMAP, overwrite=True)
    for title, (description, items) in MOCS.items():
        write(VAULT / "00 - Dashboard" / f"{title}.md",
              render_moc(title, description, items), overwrite=True)

    # Add high-value reference tables to generated notes without duplicating them on reruns.
    for title, appendix in APPENDICES.items():
        matches = [path for path in VAULT.rglob(f"{title}.md")]
        if len(matches) == 1:
            marker = clean(appendix).splitlines()[0]
            append_once(matches[0], appendix, marker)

    for path in VAULT.rglob("*.md"):
        repair_links_and_frontmatter(path)

    # Folder indexes are built after all notes exist so their link lists stay complete.
    for folder in FOLDERS:
        title = f"Index - {folder.split(' - ', 1)[1]}"
        write(VAULT / folder / f"{title}.md", render_folder_index(folder), overwrite=True)

    for path in VAULT.rglob("*.md"):
        repair_links_and_frontmatter(path)

    names: dict[str, Path] = {}
    for path in VAULT.rglob("*.md"):
        if path.stem in names:
            raise ValueError(f"Duplicate note name: {path.stem}: {names[path.stem]} and {path}")
        names[path.stem] = path

    print(f"Built {len(names)} Markdown notes in {len(FOLDERS)} teaching folders.")


if __name__ == "__main__":
    main()
