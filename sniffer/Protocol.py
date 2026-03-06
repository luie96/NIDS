
# 提供了协议类型的标准化定义和解析功能，确保系统在处理数据包时能正确识别协议。

from enum import Enum

class Protocol(Enum):
    TCP = 1
    UDP = 2
    HTTP = 3
    icmp = 4

def protocol(istr):

    str = istr.lower().strip()
    if (str == "tcp"):
        return Protocol.TCP
    elif (str == "udp"):
        return Protocol.UDP
    elif (str == "http"):
        return Protocol.HTTP
    elif (str == "icmp"):
        return Protocol.icmp
    else:
        raise ValueError("Invalid rule : incorrect protocol : '" + istr + "'.")