"""Current Computer Networks syllabus, structured for matching.

Source: the 2025 syllabus document (4 units, 46 hours).

Each topic carries `aliases` -- the vocabulary a question would actually use.
These exist because an exam question says "Explain Hamming Code", while the
syllabus says "error detection & correction methods". Matching on the syllabus
wording alone would miss it.
"""

SYLLABUS = {
    "subject": "Computer Networks",
    "code": "BCA-201",
    "year": 2025,
    "units": [
        {
            "unit": "UNIT-I",
            "hours": 12,
            "title": "Basic Concepts, OSI/TCP-IP Models, Transmission Media",
            "topics": [
                ("Components of data communication", ["components of data communication", "data communication system", "sender receiver medium protocol"]),
                ("Distributed processing", ["distributed processing"]),
                ("Line configuration", ["line configuration", "point to point", "multipoint"]),
                ("Topology", ["topology", "topologies", "star bus ring mesh"]),
                ("Transmission mode", ["transmission mode", "simplex", "half duplex", "full duplex"]),
                ("Categories of networks", ["LAN MAN WAN", "categories of networks", "network criteria", "define network"]),
                ("OSI model", ["OSI model", "layered architecture", "seven layers", "functions of each layer"]),
                ("TCP/IP model", ["TCP/IP model"]),
                ("Comparison of OSI and TCP/IP models", ["compare OSI and TCP/IP", "comparison of models"]),
                ("Guided transmission media", ["guided media", "UTP", "coaxial cable", "fiber optic", "optical channels", "multimode single mode"]),
                ("Unguided transmission media", ["unguided transmission media", "wireless media", "radio microwave infrared"]),
                ("Attenuation, distortion and noise", ["attenuation", "distortion", "noise", "transmission impairment"]),
                ("Throughput, propagation speed and time, wavelength", ["throughput", "propagation speed", "propagation time", "wavelength", "bandwidth", "response time"]),
                ("Shannon capacity", ["Shannon capacity", "Shannon capacity theorem"]),
            ],
        },
        {
            "unit": "UNIT-II",
            "hours": 12,
            "title": "Telephony and Data Link Layer",
            "topics": [
                ("Multiplexing (WDM, TDM, FDM)", ["multiplexing", "WDM", "TDM", "FDM", "interleaving", "synchronous TDM", "asynchronous TDM", "multiplexer frame rate"]),
                ("Circuit switching", ["circuit switching"]),
                ("Packet switching", ["packet switching"]),
                ("Message switching", ["message switching"]),
                ("Types of errors", ["types of errors", "single bit error", "burst error"]),
                ("Framing: character and bit stuffing", ["framing", "bit stuffing", "byte stuffing", "character stuffing"]),
                ("Error detection and correction methods", ["error detection", "error correction", "CRC", "checksum", "Hamming code", "LRC", "VRC", "redundancy", "parity"]),
                ("Flow control", ["flow control"]),
                ("Stop and wait ARQ", ["stop and wait ARQ", "stop & wait"]),
                ("Go-Back-N ARQ", ["Go-Back-N ARQ", "go back n"]),
                ("Selective repeat ARQ", ["selective repeat ARQ", "sliding window protocol", "sliding window ARQ", "piggybacking"]),
                ("Data link layer design issues", ["data link layer", "DLL design issues", "data link control"]),
            ],
        },
        {
            "unit": "UNIT-III",
            "hours": 12,
            "title": "Network Layer",
            "topics": [
                ("Internetworking devices", ["repeaters", "hubs", "bridges", "switches", "router", "gateway", "modems", "internetworking devices", "networking devices"]),
                ("IPv4 addressing", ["IPv4 addressing", "classful addressing", "classes in IPv4", "netid hostid mask", "physical and logical address"]),
                ("IPv6 addressing", ["IPv6", "IPv4 and IPv6", "IPv6 addressing"]),
                ("IPv4 subnetting", ["subnetting", "supernetting", "subnet mask"]),
                ("Unicast routing protocols: RIP, OSPF, BGP", ["RIP", "OSPF", "BGP", "unicast routing protocols"]),
                ("Static and dynamic routing", ["static routing", "dynamic routing", "adaptive routing", "non-adaptive routing", "routing methods"]),
                ("Routing basic commands", ["routing commands", "router boots", "router configuration"]),
                ("Distance vector protocol", ["distance vector", "two-node loop instability", "routing table exchange"]),
                ("Link state protocol", ["link state routing", "link state protocol", "flooding"]),
                ("Routing concepts and forwarding", ["what is routing", "forwarding function", "routing algorithm", "datagram"]),
            ],
        },
        {
            "unit": "UNIT-IV",
            "hours": 10,
            "title": "Transport and Upper Layers in OSI Model",
            "topics": [
                ("Transport layer functions and protocols", ["transport layer", "TCP", "UDP", "TCP header", "UDP header", "TCP packet format", "pseudo header", "port addressing", "sockets", "sequence number", "acknowledgement number", "window size"]),
                ("Connection management", ["connection management", "three way handshake", "three-way handshaking"]),
                ("Session layer functions", ["session layer"]),
                ("Presentation layer", ["presentation layer"]),
                ("Application layer", ["application layer", "DNS", "client-server", "peer-to-peer", "application layer protocols"]),
            ],
        },
    ],
}


def flat_topics() -> list[dict]:
    """Flatten to one row per syllabus topic, with its matching vocabulary."""
    rows = []
    for unit in SYLLABUS["units"]:
        for name, aliases in unit["topics"]:
            rows.append(
                {
                    "topic": name,
                    "unit": unit["unit"],
                    "unit_title": unit["title"],
                    "unit_hours": unit["hours"],
                    # The topic name itself is part of its own vocabulary.
                    "vocabulary": " ".join([name, *aliases]),
                }
            )
    return rows


if __name__ == "__main__":
    topics = flat_topics()
    print(f"units  : {len(SYLLABUS['units'])}")
    print(f"topics : {len(topics)}")
    for unit in SYLLABUS["units"]:
        print(f"  {unit['unit']} ({unit['hours']}h): {len(unit['topics'])} topics - {unit['title']}")
