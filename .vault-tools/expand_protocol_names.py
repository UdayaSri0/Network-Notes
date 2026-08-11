from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "Newroking"


FOLDER_RENAMES = {
    "01 - Learn/02 - IP Addressing and Subnetting": "01 - Learn/02 - Internet Protocol (IP) Addressing and Subnetting",
    "01 - Learn/03 - Switching and VLANs": "01 - Learn/03 - Switching and Virtual Local Area Networks (VLANs)",
    "01 - Learn/09 - WAN VPN and Wireless": "01 - Learn/09 - Wide Area Networks (WAN), Virtual Private Networks (VPN), and Wireless",
    "01 - Learn/10 - IPv6": "01 - Learn/10 - Internet Protocol Version 6 (IPv6)",
}


NOTE_RENAMES = {
    "ARP": "ARP - Address Resolution Protocol",
    "ICMP": "ICMP - Internet Control Message Protocol",
    "TCP": "TCP - Transmission Control Protocol",
    "UDP": "UDP - User Datagram Protocol",
    "CDP": "CDP - Cisco Discovery Protocol",
    "LLDP": "LLDP - Link Layer Discovery Protocol",
    "CIDR": "CIDR - Classless Inter-Domain Routing",
    "VLSM": "VLSM - Variable Length Subnet Masking",
    "VLAN": "VLAN - Virtual Local Area Network",
    "SVI": "SVI - Switched Virtual Interface",
    "STP": "STP - Spanning Tree Protocol",
    "RSTP": "RSTP - Rapid Spanning Tree Protocol",
    "PVST+": "PVST+ - Per-VLAN Spanning Tree Plus",
    "LACP": "LACP - Link Aggregation Control Protocol",
    "PAgP": "PAgP - Port Aggregation Protocol",
    "RIP": "RIP - Routing Information Protocol",
    "OSPF": "OSPF - Open Shortest Path First",
    "EIGRP": "EIGRP - Enhanced Interior Gateway Routing Protocol",
    "DHCP": "DHCP - Dynamic Host Configuration Protocol",
    "DNS": "DNS - Domain Name System",
    "NTP": "NTP - Network Time Protocol",
    "FTP": "FTP - File Transfer Protocol",
    "TFTP": "TFTP - Trivial File Transfer Protocol",
    "HTTP": "HTTP - Hypertext Transfer Protocol",
    "HTTPS": "HTTPS - Hypertext Transfer Protocol Secure",
    "SMTP": "SMTP - Simple Mail Transfer Protocol",
    "POP3": "POP3 - Post Office Protocol Version 3",
    "IMAP": "IMAP - Internet Message Access Protocol",
    "HSRP": "HSRP - Hot Standby Router Protocol",
    "VRRP": "VRRP - Virtual Router Redundancy Protocol",
    "GLBP": "GLBP - Gateway Load Balancing Protocol",
    "AAA": "AAA - Authentication, Authorization, and Accounting",
    "RADIUS": "RADIUS - Remote Authentication Dial-In User Service",
    "TACACS+": "TACACS+ - Terminal Access Controller Access-Control System Plus",
    "SSH": "SSH - Secure Shell",
    "ACL": "ACL - Access Control List",
    "NAT": "NAT - Network Address Translation",
    "PAT": "PAT - Port Address Translation",
    "SNMP": "SNMP - Simple Network Management Protocol",
    "SNMPv2c": "SNMPv2c - Simple Network Management Protocol Version 2c",
    "SNMPv3": "SNMPv3 - Simple Network Management Protocol Version 3",
    "VPN": "VPN - Virtual Private Network",
    "IPsec": "IPsec - Internet Protocol Security",
    "GRE Tunnel": "GRE - Generic Routing Encapsulation Tunnel",
    "PPP": "PPP - Point-to-Point Protocol",
    "HDLC": "HDLC - High-Level Data Link Control",
    "IPv4 Addressing": "IPv4 - Internet Protocol Version 4 Addressing",
    "IPv6": "IPv6 - Internet Protocol Version 6",
    "DHCPv6": "DHCPv6 - Dynamic Host Configuration Protocol for IPv6",
    "IPv6 OSPFv3": "OSPFv3 - Open Shortest Path First Version 3 for IPv6",
    "WPA2": "WPA2 - Wi-Fi Protected Access 2",
    "WPA3": "WPA3 - Wi-Fi Protected Access 3",
}


def exact_note(name: str) -> Path:
    matches = [path for path in VAULT.rglob(f"{name}.md") if path.stem == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one note named {name!r}, found {len(matches)}")
    return matches[0]


def update_title_and_aliases(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    end = content.find("\n---", 4)
    if not content.startswith("---\n") or end < 0:
        raise RuntimeError(f"Malformed frontmatter: {path}")

    frontmatter = content[4:end]
    frontmatter = re.sub(r'(?m)^title:.*$', f'title: "{new}"', frontmatter, count=1)

    if not re.search(r"(?m)^aliases:", frontmatter):
        alias_block = f'aliases:\n  - "{old}"\n  - "{new.split(" - ", 1)[1]}"\n'
        type_match = re.search(r"(?m)^type:", frontmatter)
        if type_match:
            frontmatter = frontmatter[:type_match.start()] + alias_block + frontmatter[type_match.start():]
        else:
            frontmatter = frontmatter.rstrip() + "\n" + alias_block.rstrip()
    else:
        alias_end = re.search(r"(?m)^[A-Za-z_][A-Za-z0-9_-]*:", frontmatter[frontmatter.find("aliases:") + len("aliases:"):])
        insert_at = len(frontmatter)
        if alias_end:
            insert_at = frontmatter.find("aliases:") + len("aliases:") + alias_end.start()
        block = frontmatter[frontmatter.find("aliases:"):insert_at]
        additions = []
        if old not in block:
            additions.append(f'  - "{old}"')
        full = new.split(" - ", 1)[1]
        if full not in block:
            additions.append(f'  - "{full}"')
        if additions:
            frontmatter = frontmatter[:insert_at].rstrip() + "\n" + "\n".join(additions) + "\n" + frontmatter[insert_at:].lstrip("\n")

    body = content[end + 4:]
    body = re.sub(r"(?m)^# .+$", f"# {new}", body, count=1)
    path.write_text("---\n" + frontmatter.rstrip() + "\n---" + body.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    for old_relative, new_relative in FOLDER_RENAMES.items():
        old_path = VAULT / old_relative
        new_path = VAULT / new_relative
        if new_path.exists() and not old_path.exists():
            continue
        if not old_path.exists():
            raise RuntimeError(f"Missing source folder: {old_path}")
        if new_path.exists():
            raise RuntimeError(f"Destination folder exists: {new_path}")
        old_path.rename(new_path)

    moved: dict[str, Path] = {}
    for old, new in NOTE_RENAMES.items():
        new_matches = [path for path in VAULT.rglob(f"{new}.md") if path.stem == new]
        if new_matches:
            if len(new_matches) != 1:
                raise RuntimeError(f"Duplicate destination note: {new}")
            moved[old] = new_matches[0]
            continue
        source = exact_note(old)
        destination = source.with_name(f"{new}.md")
        if destination.exists():
            raise RuntimeError(f"Destination exists: {destination}")
        source.rename(destination)
        moved[old] = destination

    for path in VAULT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for old, new in NOTE_RENAMES.items():
            # Expand only an exact wikilink target, not a longer title that starts
            # with the same acronym (for example DHCP Relay or TCP-IP Model).
            pattern = r"\[\[" + re.escape(old) + r"(?=(?:\||#|\]\]))"
            content = re.sub(pattern, f"[[{new}", content)
        path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")

    for old, path in moved.items():
        update_title_and_aliases(path, old, NOTE_RENAMES[old])

    # Repair links produced by the earlier prefix-expansion pass. A repair is
    # accepted only when it resolves to one actual unique note basename.
    actual_names = {path.stem for path in VAULT.rglob("*.md")}
    ordered = sorted(NOTE_RENAMES.items(), key=lambda item: len(item[1]), reverse=True)

    def repair_target(match: re.Match[str]) -> str:
        target = match.group(1)
        if target in actual_names:
            return match.group(0)
        for old, new in ordered:
            if not target.startswith(new):
                continue
            candidate = old + target[len(new):]
            candidate = NOTE_RENAMES.get(candidate, candidate)
            if candidate in actual_names:
                return f"[[{candidate}"
        return match.group(0)

    for path in VAULT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        content = re.sub(r"\[\[([^\]|#]+)", repair_target, content)
        path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")

    print(f"Expanded {len(NOTE_RENAMES)} protocol and technology names.")


if __name__ == "__main__":
    main()
