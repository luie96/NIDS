from threading import Thread
from scapy.all import *
import logging
import process_packet
from scapy.layers.inet import TCP, UDP, IP  # 明确导入 UDP 和 IP 类


class Sniffer(Thread):
    def __init__(self, ruleList,matches):
        # 调用父类 `Thread` 的初始化方法
        Thread.__init__(self)
        # 标记线程是否停止的标志，初始为未停止
        self.stopped = False
        # 存储规则列表，供后续数据包检测使用
        self.ruleList = ruleList
        self.matches = matches
    
    # sniffer结束程序
    def stop(self):
        """设置停止标志，用于终止嗅探线程的运行。"""
        self.stopped = True

    
    def stopfilter(self, x):
        return self.stopped

    def inPacket(self, pkt):
        # 遍历所有规则，逐一检查数据包与规则的匹配情况
        for rule in self.ruleList:
            # 检查当前规则是否与数据包匹配
            matched = rule.match(pkt)
            if (matched):
                 # 处理匹配的数据包
                process_packet(pkt, [rule], self.matches)
                break
                # 获取匹配规则时需要记录的日志消息
                # logMessage = rule.getMatchedMessage(pkt)
                # # 记录警告级别的日志，便于后续查看匹配规则的数据包信息
                # logging.warning(logMessage)
                # print(rule.getMatchedPrintMessage(pkt))
            # else:
            #     print("error")

    
  
    # sniffer开始程序
    def run(self):
        # prn 数据包回调函数，捕获到每个数据包时调用inPacket方法，iface指定嗅探网络接口，filter BPF过滤器，store是否存储数据包到内存
        sniff(prn=self.inPacket, iface="WLAN", filter="", store=0, stop_filter=self.stopfilter)
