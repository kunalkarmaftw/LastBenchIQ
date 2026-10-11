"""Ground-truth question dataset for Computer Networks, extracted by reading the
scanned papers visually (not by OCR).

Why this file exists:
  1. It is the BENCHMARK. EPIC 3 requires >=90% recall from the automated
     segmenter; "90% of what" is defined here.
  2. It is the seed of the supervised training set for EPIC 5.
  3. It proves the extraction approach: Tesseract mangles the marks column on
     these scans, a vision model does not.

Source: ml/data/raw_papers/cn/CN_PYQ_merged.pdf (9 pages, 7 papers, 2016-2024)
Units are recorded AS PRINTED ON THE PAPER. They are not assumed to match the
current syllabus -- the 2019 paper files link-state routing under Unit-I, while
the current syllabus places routing in Unit III. Mapping to the live syllabus is
a separate step, which is the point of the syllabus-matching feature.
"""

import json
from pathlib import Path

# (q_no, part, text, marks, unit_as_printed)
PAPERS: list[dict] = [
    {
        "paper_id": "CN_2016_MAY",
        "year": 2016, "session": "May-June", "paper_code": "BCA-210",
        "semester": 4, "max_marks": 75, "pages": [1],
        "questions": [
            ("Q1", "a", "What are the two types of line configuration?", 2.5, "COMPULSORY"),
            ("Q1", "b", "List four design issues in DLL of OSI model.", 2.5, "COMPULSORY"),
            ("Q1", "c", "What is bandwidth-delay product?", 2.5, "COMPULSORY"),
            ("Q1", "d", "Name two types of connectors for fiber-optic cables.", 2.5, "COMPULSORY"),
            ("Q1", "e", "A multiplexer combines four 100kbps channels cables. Using a time slot of 2 bits. What is the frame rate and frame duration?", 2.5, "COMPULSORY"),
            ("Q1", "f", "What is dynamic routing?", 2.5, "COMPULSORY"),
            ("Q1", "g", "What is SYN flooding attack?", 2.5, "COMPULSORY"),
            ("Q1", "h", "Define Piggybacking and its benefit.", 2.5, "COMPULSORY"),
            ("Q1", "i", "What does the Shannon capacity have to do with data communication?", 2.5, "COMPULSORY"),
            ("Q1", "j", "What is the use of sockets in process-to-process communication?", 2.5, "COMPULSORY"),
            ("Q2", "a", "Explain multimode and single mode for propagating light along optical channels.", 5, "UNIT-I"),
            ("Q2", "b", "Discuss various design issues for presentation and application layer of OSI model.", 7.5, "UNIT-I"),
            ("Q3", "a", "What is the role of DTE-DCE interface in internetworking? Explain with some examples.", 7.5, "UNIT-I"),
            ("Q3", "b", "Describe the three types of transmission impairment.", 5, "UNIT-I"),
            ("Q4", "a", "Discuss LRC, VRC and CRC error detection mechanisms.", 7.5, "UNIT-II"),
            ("Q4", "b", "What is Normal response mode and asynchronous balanced mode in data link control protocols.", 5, "UNIT-II"),
            ("Q5", "a", "What is Synchronous Time-division multiplexing? Explain the process of Interleaving in TDM.", 7.5, "UNIT-II"),
            ("Q5", "b", "What is Broadband ISDN? How BRI and PRI works?", 5, "UNIT-II"),
            ("Q6", "a", "What is a Router? How router boots up? Explain the role of IOS in routers.", 7.5, "UNIT-III"),
            ("Q6", "b", "What is flooding in routing? Discuss the working of any dynamic routing algorithm.", 5, "UNIT-III"),
            ("Q7", "a", "Explain the different types of classes in IPV4 addressing (classfull addressing)", 5, "UNIT-III"),
            ("Q7", "b", "Describe distance vector and link state routing algorithm.", 7.5, "UNIT-III"),
            ("Q8", "a", "What is port addressing? List three ICANN ranges for port addressing.", 5, "UNIT-IV"),
            ("Q8", "b", "With respect to TCP discuss the role of the following: (i) Sequence Number (ii) Acknowledgement Number (iii) Window size (iv) Urgent points.", 7.5, "UNIT-IV"),
            ("Q9", "a", "Compare client-server and peer-to-peer application layer Paradigms", 5, "UNIT-IV"),
            ("Q9", "b", "With respect to UDP discuss the role of the following: (i) Pseudo header (ii) Destination port number (iii) Length field.", 7.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "CN_2017_MAY",
        "year": 2017, "session": "May", "paper_code": "BCA-210",
        "semester": 4, "max_marks": 75, "pages": [2],
        "questions": [
            ("Q1", "a", "Discuss different types of Network Models and topology.", 5, "COMPULSORY"),
            ("Q1", "b", "Distinguish between FDM, TDM and WDM.", 5, "COMPULSORY"),
            ("Q1", "c", "Describe three Internetworking Devices.", 5, "COMPULSORY"),
            ("Q1", "d", "Discuss design responsibilities of Data Link layer of OSI Model.", 5, "COMPULSORY"),
            ("Q1", "e", "What is two-node loop instability problem? Discuss its two solutions.", 5, "COMPULSORY"),
            ("Q2", None, "Describe different technical specifications of UTP, Coaxial cable and Fiber optic cable as transmission media.", 12.5, "UNIT-I"),
            ("Q3", None, "Discuss the following: (a) DTE-DCE Interface (b) Different types of Transmission Impairments (c) Design responsibility of transport layer in OSI model.", 12.5, "UNIT-I"),
            ("Q4", None, "Discuss the following w.r.t error detection and correction: (a) Redundancy (b) Hamming Code (c) Checksum", 12.5, "UNIT-II"),
            ("Q5", None, "Discuss the following w.r.t ISDN: (a) BRI (b) PRI (c) Different Reference points", 12.5, "UNIT-II"),
            ("Q6", None, "Explain the algorithm which forms the basis for Distance vector Routing? List its advantage and disadvantages.", 12.5, "UNIT-III"),
            ("Q7", None, "What is Classful addressing? Discuss the role of Netid, Hostid, Mask, Subnetting and Supernetting.", 12.5, "UNIT-III"),
            ("Q8", None, "Discuss responsibilities of Transport layer in OSI model. Explain the three-way handshake to establish the connection.", 12.5, "UNIT-IV"),
            ("Q9", None, "Explain the functionalities for the following: (a) Application Layer (b) Session Layer (c) Presentation Layer", 12.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "CN_2018_MAY",
        "year": 2018, "session": "May", "paper_code": "BCA-210",
        "semester": 4, "max_marks": 75, "pages": [3],
        "questions": [
            ("Q1", "a", "Explain Shannon Capacity Theorem.", 2.5, "COMPULSORY"),
            ("Q1", "b", "What are different components of data communication?", 2.5, "COMPULSORY"),
            ("Q1", "c", "Discuss different types of transmission impairments.", 2.5, "COMPULSORY"),
            ("Q1", "d", "What is Flooding?", 2.5, "COMPULSORY"),
            ("Q1", "e", "Write a short note on DNS.", 2.5, "COMPULSORY"),
            ("Q1", "f", "Define network. Discuss various network criteria.", 2.5, "COMPULSORY"),
            ("Q1", "g", "Explain Piggybacking and its benefits.", 2.5, "COMPULSORY"),
            ("Q1", "h", "What is a datagram?", 2.5, "COMPULSORY"),
            ("Q1", "i", "Discuss Broadband-ISDN.", 2.5, "COMPULSORY"),
            ("Q1", "j", "Write a short note on cable modems.", 2.5, "COMPULSORY"),
            ("Q2", "a", "Write a short note on guided media.", 8.5, "UNIT-I"),
            ("Q2", "b", "Define throughput, bandwidth, response time, and frequency.", 4, "UNIT-I"),
            ("Q3", "a", "Draw a neat diagram of OSI model and explain the functioning of each layer.", 9.5, "UNIT-I"),
            ("Q3", "b", "Differentiate between simplex, half duplex and full duplex.", 3, "UNIT-I"),
            ("Q4", "a", "Define ISDN. What are its various services and layers?", 6, "UNIT-II"),
            ("Q4", "b", "What is multiplexing? Explain various types of multiplexing.", 6.5, "UNIT-II"),
            ("Q5", "a", "Define Flow Control. Explain any one flow control algorithm.", 6.5, "UNIT-II"),
            ("Q5", "b", "Differentiate between circuit, packet and message switching.", 6, "UNIT-II"),
            ("Q6", "a", "What is routing? Explain distance vector routing algorithm with an example.", 6.5, "UNIT-III"),
            ("Q6", "b", "Write a short note on following networking devices: (i) repeaters (ii) bridges (iii) gateways (iv) routers", 6, "UNIT-III"),
            ("Q7", "a", "Explain static and dynamic routing.", 5, "UNIT-III"),
            ("Q7", "b", "What is forwarding function? Explain link state routing algorithm with an example.", 7.5, "UNIT-III"),
            ("Q8", "a", "Explain three-way handshaking connection management in TCP.", 7.5, "UNIT-IV"),
            ("Q8", "b", "Compare TCP and UDP Protocols.", 5, "UNIT-IV"),
            ("Q9", "a", "Explain TCP packet format in detail.", 8.5, "UNIT-IV"),
            ("Q9", "b", "What are the functions of session and presentation layer?", 4, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "CN_2019_APR",
        "year": 2019, "session": "April-May", "paper_code": "BCA-210",
        "semester": 4, "max_marks": 75, "pages": [4, 5],
        "questions": [
            ("Q1", "a", "Differentiate between LAN, MAN and WAN.", 5, "COMPULSORY"),
            ("Q1", "b", "Write a short note on DNS.", 5, "COMPULSORY"),
            ("Q1", "c", "Differentiate between TDM and FDM?", 5, "COMPULSORY"),
            ("Q1", "d", "How router boots up.", 5, "COMPULSORY"),
            ("Q1", "e", "What is the differences between physical & logical address? Give examples.", 5, "COMPULSORY"),
            ("Q1", "f", "Discuss 4 different topologies in detail with examples.", 5, "COMPULSORY"),
            ("Q2", "a", "Explain the process of link state routing. Explain the events when the routing table is exchanged between routers?", 6, "UNIT-I"),
            ("Q2", "b", "For the following topology, find the best path between each pair of nodes maintained in routing table using link state routing. Show the status of routing table at router A: [DIAGRAM]", 6.5, "UNIT-I"),
            ("Q3", None, "Discuss the different components required for data communication? Compare OSI and TCP/IP models. Discuss different layers & their functions briefly.", 12.5, "UNIT-I"),
            ("Q4", "a", "What is multiplexing? Explain various types of multiplexing.", 6.5, "UNIT-II"),
            ("Q4", "b", "Discuss ISDN, its services & layers.", 6, "UNIT-II"),
            ("Q5", "a", "What do you understand by the error detection and error correction? Explain any one of the error correction technique with suitable examples?", 6, "UNIT-II"),
            ("Q5", "b", "Which layer(s) is responsible for error detection and correction in OSI model?", 6.5, "UNIT-II"),
            ("Q6", "a", "What is flow control? Which two layers provide the functionality of flow control? How does their work differ?", 6, "UNIT-III"),
            ("Q6", "b", "Differentiate between circuit switching, packet switching, and message switching. Which one the following switching is shown in figure (a), figure (b) and figure (c)? Justify your answer. [DIAGRAM]", 6.5, "UNIT-III"),
            ("Q7", None, "What do you understand by routing? Explain any routing protocol in details? Differentiate between static & dynamic routing.", 12.5, "UNIT-III"),
            ("Q8", "a", "What are functions of session layers, presentation layers & applications in OSI models?", 6.5, "UNIT-IV"),
            ("Q8", "b", "Explain three way handshaking in TCP.", 6, "UNIT-IV"),
            ("Q9", "a", "Compare TCP and UDP protocols.", 6, "UNIT-IV"),
            ("Q9", "b", "Explain TCP packet format in detail.", 6.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "CN_2023_JAN",
        "year": 2023, "session": "January-February", "paper_code": "BCA-201",
        "semester": 3, "max_marks": 75, "pages": [6],
        "questions": [
            ("Q1", "a", "What is the use of topologies in networking?", 5, "COMPULSORY"),
            ("Q1", "b", "What do you understand by Line Configuration?", 5, "COMPULSORY"),
            ("Q1", "c", "Explain Attenuation and Distortion.", 5, "COMPULSORY"),
            ("Q1", "d", "How Synchronous TDM is different from Asynchronous TDM?", 5, "COMPULSORY"),
            ("Q1", "e", "Differentiate between \"packet switching\" & \"circuit switching\".", 5, "COMPULSORY"),
            ("Q1", "f", "How IPV4 is different from IPV6?", 5, "COMPULSORY"),
            ("Q1", "g", "What is the difference between single bit error & burst error?", 5, "COMPULSORY"),
            ("Q2", "a", "Describe the components of Data Communication along with diagram.", 5, "UNIT-I"),
            ("Q2", "b", "Explain OSI model. Write the functions and protocols of each layer.", 7.5, "UNIT-I"),
            ("Q3", "a", "Define networking and its goals.", 5, "UNIT-I"),
            ("Q3", "b", "Explain Transmission Impairment in detail.", 7.5, "UNIT-I"),
            ("Q4", "a", "What do you understand by Multiplexing? Describe WDM & FDM.", 5, "UNIT-II"),
            ("Q4", "b", "Explain Hamming Code with the help of an example.", 7.5, "UNIT-II"),
            ("Q5", "a", "Define Bit-Stuffing. How it is different from character stuffing?", 5, "UNIT-II"),
            ("Q5", "b", "Explain any three error detection methods?", 7.5, "UNIT-II"),
            ("Q6", "a", "What do you understand by Routing? Differentiate between adaptive and non-adaptive routing.", 5, "UNIT-III"),
            ("Q6", "b", "Describe repeater, router, switch, hub, bridge & gateway.", 7.5, "UNIT-III"),
            ("Q7", "a", "Differentiate between Distance Vector Routing & Link State Routing.", 5, "UNIT-III"),
            ("Q7", "b", "What is subnetting? Describe Unicast Routing Protocols.", 7.5, "UNIT-III"),
            ("Q8", "a", "Compare the TCP header with UDP header.", 5, "UNIT-IV"),
            ("Q8", "b", "Explain Connection Management with the help of a diagram.", 7.5, "UNIT-IV"),
            ("Q9", "a", "Discuss the design issue of session layer.", 5, "UNIT-IV"),
            ("Q9", "b", "Describe any five protocols present on application layer with their functionality.", 7.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "CN_2024_JAN",
        "year": 2024, "session": "January", "paper_code": "BCA-201",
        "semester": 3, "max_marks": 75, "pages": [7, 8],
        "questions": [
            ("Q1", "a", "Define a network. Discuss various Network Criteria.", 5, "COMPULSORY"),
            ("Q1", "b", "Compare TCP and UDP protocols", 5, "COMPULSORY"),
            ("Q1", "c", "Define Piggybacking and specify its benefit.", 5, "COMPULSORY"),
            ("Q1", "d", "Write a short note on Modems.", 5, "COMPULSORY"),
            ("Q1", "e", "Differentiate between Bridges and Routers.", 5, "COMPULSORY"),
            ("Q1", "f", "In reference to UDP, what is the role of Pseudoheader and the Length field?", 5, "COMPULSORY"),
            ("Q1", "g", "What is bit stuffing and byte stuffing?", 5, "COMPULSORY"),
            ("Q1", "h", "Compare and contrast the different Unguided transmission media.", 5, "COMPULSORY"),
            ("Q2", "a", "What is layered architecture? Explain the OSI model in brief.", 6.5, "UNIT-I"),
            ("Q2", "b", "Explain LAN, MAN & WAN.", 6, "UNIT-I"),
            ("Q3", "a", "Discuss the topologies in detail with examples.", 7.5, "UNIT-I"),
            ("Q3", "b", "Explain the Shannon capacity theorem.", 5, "UNIT-I"),
            ("Q4", "a", "What is understood by Flow Control? Explain any one Sliding Window ARQ protocol with diagrams and example.", 6.5, "UNIT-II"),
            ("Q4", "b", "Given a 10-bit sequence 1010011110 and a divisor of 1011, find the CRC and check your answer.", 6, "UNIT-II"),
            ("Q5", "a", "Discuss the sliding window protocol. Specify its advantages over stop and wait protocol.", 6.5, "UNIT-II"),
            ("Q5", "b", "Distinguish the following (i) Synchronous and Asynchronous TDM (ii) Circuit switching and Packet switching", 6, "UNIT-II"),
            ("Q6", None, "Explain the process of Distance vector routing with an example. Explain when the sharing happens and how routing tables are exchanged between routers.", 12.5, "UNIT-III"),
            ("Q7", "a", "A multiplexer combines four 100-Kbps channels using a time slot of 2 bits. Show the output with four arbitrary inputs. Calculate: Frame size, Frame rate, Frame duration, Bit rate of link.", 5, "UNIT-III"),
            ("Q7", "b", "What is understood by Classful addressing? Explain. What is its disadvantage?", 7.5, "UNIT-III"),
            ("Q8", "a", "Explain the functions and protocols of the Transport Layer.", 7.5, "UNIT-IV"),
            ("Q8", "b", "Explain Connection Management in reference to transport layer.", 5, "UNIT-IV"),
            ("Q9", None, "Explain the functions and design issues of Session layer, Presentation layer and Application layer.", 12.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "CN_2024_DEC",
        "year": 2024, "session": "December", "paper_code": "BCA-201",
        "semester": 3, "max_marks": 60, "pages": [9],
        "questions": [
            ("Q1", "a", "Explain the concept of distributed processing. How does it enhance the performance of network systems?", 4, "COMPULSORY"),
            ("Q1", "b", "Define attenuation, distortion, and noise in transmission. How do they affect signal quality?", 4, "COMPULSORY"),
            ("Q1", "c", "Describe the significance of modulation in telecommunication.", 4, "COMPULSORY"),
            ("Q1", "d", "Explain the mechanisms involved in flow control in data communication.", 4, "COMPULSORY"),
            ("Q1", "e", "Describe the process of IPv4 subnetting and its importance in network configurations.", 4, "COMPULSORY"),
            ("Q2", None, "Explain the essential components of a data communication system and their roles in facilitating communication. Use diagrams where necessary?", 10, "UNIT-I"),
            ("Q3", None, "Explain the differences between guided and unguided transmission media. Discuss the factors affecting propagation speed and throughput in these media types.", 10, "UNIT-I"),
            ("Q4", None, "Discuss various error detection and correction methods employed in the data link layer. Compare their effectiveness and implementation complexities.", 10, "UNIT-II"),
            ("Q5", None, "Compare the OSI and TCP/IP models in terms of their layer structures and the protocols associated with each layer.", 10, "UNIT-II"),
            ("Q6", "a", "Differentiate between WDM, TDM, and FDM in multiplexing techniques. Provide real-world applications for each.", 5, "UNIT-III"),
            ("Q6", "b", "Explain the principles of unicast routing protocols: RIP, OSPF, and BGP.", 5, "UNIT-III"),
            ("Q7", None, "Discuss the differences between static and dynamic routing. Explain Distance Vector and Link State routing protocols.", 10, "UNIT-III"),
            ("Q8", "a", "Compare IPv4 and IPv6 addressing schemes, highlighting their advantages and differences.", 5, "UNIT-IV"),
            ("Q8", "b", "Define the roles of the session layer, presentation layer, and application layer in the OSI model.", 5, "UNIT-IV"),
            ("Q9", None, "Discuss symmetric and asymmetric encryption techniques, highlighting their differences in terms of security, key distribution, and computational complexity.", 10, "UNIT-IV"),
        ],
    },
]


def build() -> list[dict]:
    rows: list[dict] = []
    for paper in PAPERS:
        for q_no, part, text, marks, unit in paper["questions"]:
            rows.append(
                {
                    "question_id": f"{paper['paper_id']}_{q_no}{part or ''}",
                    "paper_id": paper["paper_id"],
                    "year": paper["year"],
                    "session": paper["session"],
                    "paper_code": paper["paper_code"],
                    "semester": paper["semester"],
                    "paper_max_marks": paper["max_marks"],
                    "q_no": q_no,
                    "part": part,
                    "text": text,
                    "marks": marks,
                    "unit_as_printed": unit,
                    "has_diagram": "[DIAGRAM]" in text,
                }
            )
    return rows


if __name__ == "__main__":
    rows = build()
    out = Path(__file__).parent / "cn_questions_groundtruth.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    total_marks = sum(r["marks"] for r in rows)
    print(f"papers    : {len(PAPERS)}")
    print(f"questions : {len(rows)}")
    print(f"marks     : {total_marks}")
    print(f"written   : {out}")
    for p in PAPERS:
        got = sum(q[3] for q in p["questions"])
        print(f"  {p['paper_id']:14s} {len(p['questions']):3d} q  {got:6.1f} marks (paper max {p['max_marks']})")
