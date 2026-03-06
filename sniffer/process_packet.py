import logging
import datetime
from gui import *
from gui import update_gui
from scapy.layers.inet import  IP  # 



def process_packet(packet, rules, matches):
    for rule in rules:
        if rule.match(packet):
            # 提取基本信息
            time = datetime.datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S')
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = rule.protocol.value
            action = rule.action.name
            message = rule.msg if hasattr(rule, "msg") else "No message provided"

            # 提取和计算其他字段
            duration = 0  # 需要根据实际情况计算
            protocol_type = protocol  # 根据协议类型设置
            service = "unknown"  # 根据服务类型设置
            flag = "unknown"  # 根据标志设置
            src_bytes = len(packet)  # 源字节数
            dst_bytes = 0  # 目的字节数
            land = 0  # 是否为 LAND 攻击
            wrong_fragment = 0  # 错误分片数
            hot = 0  # 热登录次数
            num_failed_logins = 0  # 失败登录次数
            logged_in = 0  # 是否登录
            num_compromised = 0  # 被攻破次数
            is_guest_login = 0  # 是否为访客登录
            count = 1  # 计数
            srv_count = 1  # 服务计数
            serror_rate = 0.0  # 服务错误率
            rerror_rate = 0.0  # 服务错误率
            srv_rerror_rate = 0.0  # 服务错误率
            same_srv_rate = 0.0  # 相同服务率
            diff_srv_rate = 0.0  # 不同服务率
            srv_diff_host_rate = 0.0  # 服务不同主机率
            dst_host_count = 1  # 目的主机计数
            dst_host_srv_count = 1  # 目的主机服务计数
            dst_host_same_srv_rate = 0.0  # 目的主机相同服务率
            dst_host_diff_srv_rate = 0.0  # 目的主机不同服务率
            dst_host_same_src_port_rate = 0.0  # 目的主机相同源端口率
            dst_host_srv_diff_host_rate = 0.0  # 目的主机服务不同主机率
            dst_host_serror_rate = 0.0  # 目的主机服务错误率
            dst_host_srv_serror_rate = 0.0  # 目的主机服务错误率
            dst_host_rerror_rate = 0.0  # 目的主机服务错误率
            dst_host_srv_rerror_rate = 0.0  # 目的主机服务错误率
            class_ = "unknown"  # 类别

            # 将匹配信息添加到 matches 列表
            matches.append({
                "duration": duration,
                "protocol_type": protocol_type,
                "service": service,
                "flag": flag,
                "src_bytes": src_bytes,
                "dst_bytes": dst_bytes,
                "land": land,
                "wrong_fragment": wrong_fragment,
                "hot": hot,
                "num_failed_logins": num_failed_logins,
                "logged_in": logged_in,
                "num_compromised": num_compromised,
                "is_guest_login": is_guest_login,
                "count": count,
                "srv_count": srv_count,
                "serror_rate": serror_rate,
                "rerror_rate": rerror_rate,
                "srv_rerror_rate": srv_rerror_rate,
                "same_srv_rate": same_srv_rate,
                "diff_srv_rate": diff_srv_rate,
                "srv_diff_host_rate": srv_diff_host_rate,
                "dst_host_count": dst_host_count,
                "dst_host_srv_count": dst_host_srv_count,
                "dst_host_same_srv_rate": dst_host_same_srv_rate,
                "dst_host_diff_srv_rate": dst_host_diff_srv_rate,
                "dst_host_same_src_port_rate": dst_host_same_src_port_rate,
                "dst_host_srv_diff_host_rate": dst_host_srv_diff_host_rate,
                "dst_host_serror_rate": dst_host_serror_rate,
                "dst_host_srv_serror_rate": dst_host_srv_serror_rate,
                "dst_host_rerror_rate": dst_host_rerror_rate,
                "dst_host_srv_rerror_rate": dst_host_srv_rerror_rate,
                "class": class_
            })

            print(rule.get_matched_print_message(packet))
            logging.info(rule.get_matched_message(packet))
            update_gui(matches)
            return True
    return False