# 规范化处理规则中的 IP 地址和子网，支持网络入侵检测系统对数据包 IP 归属的判断。
from ipaddress import *

class IPNetwork:
    def __init__(self, string):
        try:
            # 去除字符串末尾的空白字符，检查是否为 'any'
            if (string.rstrip() == "any"):
                # 如果是 'any'，表示匹配所有 IP 地址，使用 '0.0.0.0/0' 网络
                self.ipn = ip_network(u'0.0.0.0/0')
            else:
                # 将输入字符串按 '/' 分割成列表
                strs = string.split("/")
                if (len(strs) >= 2):
                    # 如果分割后的列表长度大于等于 2，说明输入是 CIDR 表示法； 提取 CIDR 块中的子网掩码位数
                    bloc = int(strs[1])
                    # bloc = 32 - bloc  # 这行代码被注释掉了，可能是原作者的一个未使用的处理逻辑；使用分割后的 IP 地址和子网掩码位数构造一个 IP 网络对象
                    self.ipn = ip_network(strs[0] + "/" + str(bloc))
                else:
                    # 如果分割后的列表长度小于 2，说明输入是一个单独的 IP 地址;将其转换为 CIDR 表示法，子网掩码为 32 位，表示单个 IP 地址
                    self.ipn = ip_network(strs[0] + "/32")
        except:
            raise ValueError("Incorrect input string.")

    def contains(self, ip):
        return (ip in self.ipn)

    def __repr__(self):
        return self.ipn.__repr__()