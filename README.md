# Network Notes

A structured Cisco networking learning and teaching vault built with Markdown and Obsidian. The project combines theory, configuration examples, practical exercises, troubleshooting material, classroom resources, and Cisco Packet Tracer labs in one navigable repository.

The content is suitable for:

- Students learning networking from fundamentals to enterprise topics.
- Lecturers preparing lessons, demonstrations, practicals, viva questions, and assessments.
- Lab users practising Cisco IOS configuration and verification.
- Anyone building a searchable personal networking knowledge base.

## Project highlights

- 379 Markdown notes in the learning vault.
- 30 numbered practice labs.
- 46 numbered step-by-step Cisco configuration guides, plus 10 category guides.
- Topic notes covering fundamentals, switching, routing, services, security, high availability, monitoring, WANs, VPNs, wireless, IPv6, and troubleshooting.
- Teaching templates, cheat sheets, viva questions, lesson resources, and assessment materials.
- Advanced enterprise projects and ready-to-open Cisco Packet Tracer practicals.
- Obsidian-friendly navigation using dashboards, maps of content, tags, frontmatter, and wikilinks.

## Start here

| Goal | Recommended page |
|---|---|
| Open the main vault dashboard | [Networking Dashboard](00%20-%20Start%20Here/Networking%20Dashboard.md) |
| Follow the recommended study order | [Networking Learning Roadmap](00%20-%20Start%20Here/Networking%20Learning%20Roadmap.md) |
| Begin as a student | [Student Dashboard](00%20-%20Start%20Here/Student%20Dashboard.md) |
| Prepare material as a lecturer | [Lecturer Dashboard](00%20-%20Start%20Here/Lecturer%20Dashboard.md) |
| Find a protocol or technology | [Network Protocol Master Index](00%20-%20Start%20Here/Network%20Protocol%20Master%20Index.md) |
| Choose a practical exercise | [Lab Dashboard](02%20-%20Practice%20Labs/Lab%20Dashboard.md) |
| Find copy-ready configurations | [Configuration Library Dashboard](05%20-%20Step-by-Step%20Configurations/Configuration%20Library%20Dashboard.md) |
| Find classroom resources | [Teaching Toolkit Dashboard](03%20-%20Teaching%20Toolkit/Teaching%20Toolkit%20Dashboard.md) |
| Explore integrated projects | [Advanced Projects Dashboard](04%20-%20Advanced%20Projects/Advanced%20Projects%20Dashboard.md) |

If you open the project in Obsidian, start with `00 - Start Here/Networking Dashboard.md`.

## Learning path

The suggested progression is:

1. Network fundamentals and models.
2. IPv4 addressing, subnetting, CIDR, and VLSM.
3. Ethernet switching, VLANs, trunks, STP, and EtherChannel.
4. Static routing, RIP, OSPF, and EIGRP.
5. DHCP, DNS, NTP, file transfer, web, and email services.
6. SSH, AAA, ACLs, Layer 2 security, NAT, and PAT.
7. HSRP, VRRP, GLBP, and resilient network design.
8. SNMP, Syslog, CDP, LLDP, and network monitoring.
9. WAN technologies, VPNs, wireless, and IPv6.
10. Integrated troubleshooting and enterprise projects.

## Repository structure

The repository root is also the Obsidian vault root. The learning folders are directly accessible on GitHub and after cloning or downloading the project.

```text
Network-Notes/
├── .obsidian/                         Obsidian vault settings
├── .vault-tools/                      Historical maintenance scripts
├── .gitattributes
├── 00 - Start Here/                   Dashboards, indexes, and roadmaps
├── 01 - Learn/                        Topic explanations and troubleshooting
├── 02 - Practice Labs/                Labs 01 through 30
├── 03 - Teaching Toolkit/             Templates, cheat sheets, viva, and lessons
├── 04 - Advanced Projects/            Enterprise and platform-level projects
├── 05 - Step-by-Step Configurations/  Copy-ready Cisco configuration guides
├── Images and Source/                 Supporting images and source material
├── Practical with Sample Code and Configs/
│   ├── HSRP Gateway Redundancy Lab/
│   ├── Three-Router OSPF Lab/
│   └── Three-Router Static Routing Lab/
├── New Text Document.txt              Existing empty placeholder
└── README.md
```

The scripts in `.vault-tools/` still reference the older `Newroking` layout and need their paths reviewed before use. They are not required to browse the notes or open the vault.

### Learning topics

The `01 - Learn` section is organized into:

- Fundamentals.
- IP addressing and subnetting.
- Switching and VLANs.
- Routing.
- Network services.
- High availability.
- Security.
- Monitoring and management.
- WAN, VPN, and wireless networking.
- IPv6.
- Troubleshooting.

### Step-by-step configuration library

The `05 - Step-by-Step Configurations` section contains guided Cisco configurations grouped into:

- Device foundations.
- Switching and inter-VLAN routing.
- Routing protocols.
- Network services.
- Security.
- High availability.
- Monitoring and management.
- WAN, VPN, and wireless.
- IPv6.
- Integrated enterprise configuration.

## Featured Packet Tracer practicals

### HSRP Gateway Redundancy Lab

A three-router high-availability practical covering corrected Layer 2 cabling, HSRP virtual gateways, priorities, preemption, interface tracking, floating static routes, verification, and failover testing.

- [Open the HSRP practical folder](Practical%20with%20Sample%20Code%20and%20Configs/HSRP%20Gateway%20Redundancy%20Lab/)
- [Read the HSRP configuration guide](Practical%20with%20Sample%20Code%20and%20Configs/HSRP%20Gateway%20Redundancy%20Lab/HSRP%20Gateway%20Redundancy%20Lab%20-%20Configuration%20Guide.md)

### Three-Router OSPF Lab

A three-router practical covering OSPF neighbor formation, route advertisement, passive interfaces, verification, and troubleshooting.

- [Open the OSPF practical folder](Practical%20with%20Sample%20Code%20and%20Configs/Three-Router%20OSPF%20Lab/)
- [Read the OSPF practical guide](Practical%20with%20Sample%20Code%20and%20Configs/Three-Router%20OSPF%20Lab/Cisco%20Packet%20Tracer%20%E2%80%93%20Three-Router%20OSPF%20Lab.md)

### Three-Router Static Routing Lab

A three-LAN practical for configuring routed interfaces, `/30` transit networks, static routes, PC gateways, end-to-end tests, traceroute, and common routing troubleshooting.

- [Open the static-routing practical folder](Practical%20with%20Sample%20Code%20and%20Configs/Three-Router%20Static%20Routing%20Lab/)

Packet Tracer `.pkt` files are binary files and cannot be previewed meaningfully on GitHub. Download or clone the repository and open them with Cisco Packet Tracer.

## Using the project with Obsidian

Obsidian is the recommended way to use the complete vault because the notes use wikilinks, callouts, tags, frontmatter, and connected dashboards.

1. Clone the repository or download and extract its ZIP archive.
2. Open Obsidian.
3. Select **Open folder as vault**.
4. Choose the repository folder itself (`Network-Notes`, or `Network Notes` if that is your local folder name). It contains `.obsidian` and `00 - Start Here` directly.
5. Open `00 - Start Here/Networking Dashboard.md`.

The included `.obsidian` folder contains the vault configuration. Obsidian is recommended but not required; every learning note is still a normal Markdown file.

If you previously opened the nested `Networking` folder as your vault, reopen the repository root after updating. The notes, attachments, and settings have moved together, so existing note links retain their targets.

## Cloning the repository

```bash
git clone https://github.com/UdayaSri0/Network-Notes.git
cd Network-Notes
```

You can also browse the Markdown files directly on GitHub without installing Obsidian.

## Using the practical labs

For a reliable lab workflow:

1. Read the objective and topology requirements.
2. Build or open the topology in Cisco Packet Tracer.
3. Complete the addressing table before entering commands.
4. Configure interfaces and use `no shutdown` where required.
5. Configure switching, routing, services, or security in the order shown.
6. Verify each stage before moving to the next stage.
7. Test the expected success path.
8. Perform the documented failure or troubleshooting tests.
9. Save the device configurations and Packet Tracer file.

Useful Cisco IOS verification commands include:

```cisco
show ip interface brief
show interfaces status
show vlan brief
show ip route
show running-config
ping <destination>
traceroute <destination>
```

Use the commands relevant to the technology being practised; additional verification commands are included in the individual lab guides.

## Note design

Major notes are designed to answer the following questions:

- **What** is the technology?
- **Why** is it used?
- **Where** does it operate in a network?
- **How** does it work?
- How is it **configured**?
- How is it **verified**?
- How can it **fail**?
- How is it **troubleshot**?

Most notes include YAML frontmatter for classification and Obsidian search. Wikilinks use unique note names so related material remains easy to discover inside the vault.

## Contributing

Contributions that improve technical accuracy, clarity, lab coverage, or navigation are welcome.

When adding or updating content:

1. Use a clear, unique, descriptive filename.
2. Place the note in the most relevant section.
3. Follow the existing YAML frontmatter style when editing vault notes.
4. Link related topics with Obsidian wikilinks.
5. Include configuration, verification, failure cases, and troubleshooting where applicable.
6. Test Cisco IOS commands in an appropriate lab environment.
7. Do not commit passwords, private addresses from real environments, API keys, or other sensitive information.
8. Keep images and Packet Tracer files close to the practical that uses them, or place shared media in `Images and Source`.

Before submitting a change, check that links work, code blocks are correctly fenced, filenames are readable, and lab addressing is internally consistent.

## Technical and safety notes

- Configurations are intended for education and lab use. Validate them before using them on production equipment.
- Cisco IOS commands and supported features can vary by device model, image, license, and software version.
- Some examples preserve addressing from their original teaching diagrams. Replace example addressing with an approved private or assigned address plan in real networks.
- A successful ping alone does not prove that redundancy, security, or failure recovery is working; complete the verification and failure tests in each guide.

## Project status

This is an actively developed learning vault. Content, navigation, and practical files may continue to expand as new networking topics and labs are added.

## License

No license file is currently included in this repository. Unless a license is added, obtain permission from the repository owner before copying, redistributing, or republishing the project outside the permissions automatically provided by GitHub.
