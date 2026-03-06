import re
from scapy.all import *
from scapy.all import IP, TCP, UDP, IPv6
from Utils import *
from Rule import *

RED = '\033[91m'
ENDC = '\033[0m'
URG = 0x20

def ipString(ip):
    # 初始化输出字符串，添加 IP 头部的标题
    out = "[IP HEADER]" + "\n"
    # 依次添加 IP 头部的各个字段信息，包括版本、首部长度、服务类型等
    out += "\t Version: " + str(ip.version) + "\n"
    out += "\t IHL: " + str(ip.ihl * 4) + " bytes" + "\n"
    out += "\t ToS: " + str(ip.tos) + "\n"
    out += "\t Total Length: " + str(ip.len) + "\n"
    out += "\t Identification: " + str(ip.id) + "\n"
    out += "\t Flags: " + str(ip.flags) + "\n"
    out += "\t Fragment Offset: " + str(ip.frag) + "\n"
    out += "\t TTL: " + str(ip.ttl) + "\n"
    out += "\t Protocol: " + str(ip.proto) + "\n"
    out += "\t Header Checksum: " + str(ip.chksum) + "\n"
    out += "\t Source: " + str(ip.src) + "\n"
    out += "\t Destination: " + str(ip.dst) + "\n"
    # 如果 IP 首部长度大于 5（表示有选项字段），则添加选项字段信息
    if (ip.ihl > 5):
        out += "\t Options: " + str(ip.options) + "\n"
    return out

def matchedIpString(ip, rule):
    out = "[IP HEADER]" + "\n"
    out += "\t Version: " + str(ip.version) + "\n"
    if (hasattr(rule, "len")):
        out += RED + "\t IHL: " + str(ip.ihl * 4) + " bytes" + ENDC + "\n"
    else:
        out += "\t IHL: " + str(ip.ihl * 4) + " bytes" + "\n"
    if (hasattr(rule, "tos")):
        out += RED + "\t ToS: " + str(ip.tos) + ENDC + "\n"
    else:
        out += "\t ToS: " + str(ip.tos) + "\n"
    out += "\t Total Length: " + str(ip.len) + "\n"
    out += "\t Identification: " + str(ip.id) + "\n"
    out += "\t Flags: " + str(ip.flags) + "\n"
    if (hasattr(rule, "offset")):
        out += RED + "\t Fragment Offset: " + str(ip.frag) + ENDC + "\n"
    else:
        out += "\t Fragment Offset: " + str(ip.frag) + "\n"
    out += "\t TTL: " + str(ip.ttl) + "\n"
    out += "\t Protocol: " + str(ip.proto) + "\n"
    out += "\t Header Checksum: " + str(ip.chksum) + "\n"
    if (rule.srcIps.ipn.num_addresses == 1):
        out += RED + "\t Source: " + str(ip.src) + ENDC + "\n"
    else:
        out += "\t Source: " + str(ip.src) + "\n"
    if (rule.dstIps.ipn.num_addresses == 1):
        out += RED + "\t Destination: " + str(ip.dst) + ENDC + "\n"
    else:
        out += "\t Destination: " + str(ip.dst) + "\n"
    if (ip.ihl > 5):
        out += "\t Options : " + str(ip.options) + "\n"
    return out

def tcpString(tcp):
    out = "[TCP Header]" + "\n"
    out += "\t Source Port: " + str(tcp.sport) + "\n"
    out += "\t Destination Port: " + str(tcp.dport) + "\n"
    out += "\t Sequence Number: " + str(tcp.seq) + "\n"
    out += "\t Acknowledgment Number: " + str(tcp.ack) + "\n"
    out += "\t Data Offset: " + str(tcp.dataofs) + "\n"
    out += "\t Reserved: " + str(tcp.reserved) + "\n"
    out += "\t Flags: " + tcp.underlayer.sprintf("%TCP.flags%") + "\n"
    out += "\t Window Size: " + str(tcp.window) + "\n"
    out += "\t Checksum: " + str(tcp.chksum) + "\n"
    if (tcp.flags & URG):
        out += "\t Urgent Pointer: " + str(tcp.window) + "\n"
    if (tcp.dataofs > 5):
        out += "\t Options: " + str(tcp.options) + "\n"
    return out

def matchedTcpString(tcp, rule):
    out = "[TCP Header]" + "\n"
    if (hasattr(rule.srcPorts, "listPorts") and len(rule.srcPorts.listPorts) == 1):
        out += RED + "\t Source Port: " + str(tcp.sport) + ENDC + "\n"
    else:
        out += "\t Source Port: " + str(tcp.sport) + "\n"
    if (hasattr(rule.dstPorts, "listPorts") and len(rule.dstPorts.listPorts) == 1):
        out += RED + "\t Destination Port: " + str(tcp.dport) + ENDC + "\n"
    else:
        out += "\t Destination Port: " + str(tcp.dport) + "\n"
    if (hasattr(rule, "seq")):
        out += RED + "\t Sequence Number: " + str(tcp.seq) + ENDC + "\n"
    else:
        out += "\t Sequence Number: " + str(tcp.seq) + "\n"
    if (hasattr(rule, "ack")):
        out += RED + "\t Acknowledgment Number: " + str(tcp.ack) + ENDC + "\n"
    else:
        out += "\t Acknowledgment Number: " + str(tcp.ack) + "\n"
    out += "\t Data Offset: " + str(tcp.dataofs) + "\n"
    out += "\t Reserved: " + str(tcp.reserved) + "\n"
    if (hasattr(rule,"flags")):
        out += RED + "\t Flags:" + tcp.underlayer.sprintf("%TCP.flags%") + ENDC + "\n"
    else:
        out += "\t Flags:" + tcp.underlayer.sprintf("%TCP.flags%") + "\n"
    out += "\t Window Size: " + str(tcp.window) + "\n"
    out += "\t Checksum: " + str(tcp.chksum) + "\n"
    if (tcp.flags & URG):
        out += "\t Urgent Pointer: " + str(tcp.window) + "\n"
    if (tcp.dataofs > 5):
        out += "\t Options: " + str(tcp.options) + "\n"
    return out

def udpString(udp):
    out = "[UDP Header]" + "\n"
    out += "\t Source Port: " + str(udp.sport) + "\n"
    out += "\t Destination Port: " + str(udp.dport) + "\n"
    out += "\t Length: " + str(udp.len) + "\n"
    out += "\t Checksum: " + str(udp.chksum) + "\n"
    return out

def matchedUdpString(udp, rule):
    out = "[UDP Header]" + "\n"
    if (hasattr(rule.srcPorts, "listPorts") and len(rule.srcPorts.listPorts) == 1):
        out += RED + "\t Source Port: " + str(udp.sport) + ENDC + "\n"
    else:
        out += "\t Source Port: " + str(udp.sport) + "\n"
    if (hasattr(rule.dstPorts, "listPorts") and len(rule.dstPorts.listPorts) == 1):
        out += RED + "\t Destination Port: " + str(udp.dport) + ENDC + "\n"
    else:
        out += "\t Destination Port: " + str(udp.dport) + "\n"
    out += "\t Length: " + str(udp.len) + "\n"
    out += "\t Checksum: " + str(udp.chksum) + "\n"
    return out

def payloadString(pkt):
    if (pkt.payload):
        data = str(pkt.payload)
        lines = data.splitlines()
        s = ""
        for line in lines:
            s += "\t" + line + "\n"
        out = s
        return out
    else:
        return ""

def matchedTcpPayloadString(tcp, rule):
    out = "[TCP Payload]" + "\n"
    if (hasattr(rule, "http_request")):
        out += RED + "HTTP Request: " + str(rule.http_request) + ENDC + "\n"
    if (hasattr(rule, "content") and tcp.payload):
        data = str(tcp.payload)
        data = re.sub(rule.content, RED + rule.content + ENDC, data)
        lines = data.splitlines()
        s = ""
        for line in lines:
            s += "\t" + line + "\n"
        out += s
        return out
    else:
        return out + payloadString(tcp)

def matchedUdpPayloadString(udp, rule):
    out = "[UDP Payload]" + "\n"
    if (hasattr(rule, "content") and udp.payload):
        data = str(udp.payload)
        data = re.sub(rule.content, RED + rule.content + ENDC, data)
        lines = data.splitlines()
        s = ""
        for line in lines:
            s += "\t" + line + "\n"
        out += s
    else:
        return out + payloadString(udp)







# def packetString(pkt):
#     return pkt.summary()

# def matchedPacketString(pkt, rule):
#     summary = pkt.summary()
#     additional_info = ""
#     if hasattr(rule, "msg"):
#         additional_info += f"\nMessage: {rule.msg}"
#     if hasattr(rule, "tos"):
#         additional_info += f"\nTOS: {rule.tos}"
#     if hasattr(rule, "len"):
#         additional_info += f"\nLength: {rule.len}"
#     if hasattr(rule, "offset"):
#         additional_info += f"\nOffset: {rule.offset}"
#     if hasattr(rule, "seq"):
#         additional_info += f"\nSequence: {rule.seq}"
#     if hasattr(rule, "ack"):
#         additional_info += f"\nAcknowledgment: {rule.ack}"
#     if hasattr(rule, "flags"):
#         additional_info += f"\nFlags: {rule.flags}"
#     if hasattr(rule, "http_request"):
#         additional_info += f"\nHTTP Request: {rule.http_request}"
#     if hasattr(rule, "content"):
#         additional_info += f"\nContent: {rule.content}"

#     return summary + additional_info



def packetString(pkt):
    # 初始化输出字符串
    out = ""
    # 检查数据包中是否包含 IP 层
    if (IP in pkt):
        out += ipString(pkt[IP])
    elif (IPv6 in pkt):
        # TODO
        pass
    # 检查数据包中是否包含 TCP 层
    if (TCP in pkt):
        out += tcpString(pkt[TCP])
        # 添加 TCP 负载的标题
        out += "[TCP Payload]" + "\n"
        out += payloadString(pkt[TCP])
    # 检查数据包中是否包含 UDP 层
    elif (UDP in pkt):
        out += udpString(pkt[UDP])
        out += "[UDP Payload]" + "\n"
        out += payloadString(pkt[UDP])
    return out

def matchedPacketString(pkt, rule):
    out = ""
    if (IP in pkt):
        out += matchedIpString(pkt[IP], rule)
    elif (IPv6 in pkt):
        # TODO
        pass
    # 检查数据包中是否包含 TCP 层
    if (TCP in pkt):
        out += matchedTcpString(pkt[TCP], rule)
        out += matchedTcpPayloadString(pkt[TCP], rule)
    # 检查数据包中是否包含 UDP 层
    elif (UDP in pkt):
        out += matchedUdpString(pkt[UDP], rule)
        out += matchedUdpPayloadString(pkt[UDP], rule)
    return out