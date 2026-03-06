# 用于在一个独立的线程中捕获网络数据包，并根据预定义的规则对捕获到的数据包进行检测。如果数据包匹配某个规则，将记录日志并打印详细信息

from enum import Enum
from scapy.all import *
from scapy.all import TCP

# 定义一个包含常见 HTTP 请求方法的列表，用于判断数据包是否为 HTTP 请求
HTTPcommands = ["GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]

def isHTTP(pkt):
    """
    判断一个数据包是否为 HTTP 数据包。
    :param pkt: Scapy 的数据包对象，待检测的网络数据包
    :return: bool，若为 HTTP 数据包返回 True，否则返回 False
    """
    if (TCP in pkt and pkt[TCP].payload):
        data = str(pkt[TCP].payload)
        words = data.split('/')
        if (len(words) >= 1 and words[0].rstrip() == "HTTP"):
            return True
        words = data.split(' ')
        if (len(words) >= 1 and words[0].rstrip() in HTTPcommands):
            return True
        else:
            return False
    else:
        return False