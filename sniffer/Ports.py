class Ports:
    def __init__(self, string):
        try:
            if (string == "any"):
                self.type = "any"
            elif ":" in string:
                # 处理端口范围情况
                self.type = "range"
                strs = string.split(":")
                if (string[0] == ":"):
                    # 处理类似 ":100" 的情况，表示端口 <= 100
                    self.lowPort = -1
                    self.highPort = int(strs[1])
                elif string[len(string) - 1] == ":":
                    # 处理类似 "100:" 的情况，表示端口 >= 100
                    self.lowPort = int(strs[0])
                    self.highPort = -1
                else:
                    # 处理正常范围，如 "30:100"
                    self.lowPort = int(strs[0])
                    self.highPort = int(strs[1])
            elif "," in string:
                # 处理逗号分隔的端口列表
                self.type = "list"
                self.listPorts = list()
                strs = string.split(",")
                for s in strs:
                    self.listPorts.append(int(s))
            else:
                # 处理单个端口的情况，如 "80"
                self.type = "list"
                self.listPorts = list()
                self.listPorts.append(int(string))
        except:
            raise ValueError("Incorrect input string.")

    def contains(self, port):
        if (self.type == "any"):
            return True
        elif (self.type == "range"):
            if (self.lowPort == -1):
                return port <= self.highPort
            elif (self.highPort == -1):
                return port >= self.lowPort
            else:
                return self.lowPort <= port and port <= self.highPort
        elif (self.type == "list"):
            return port in self.listPorts

    def __repr__(self):
        if (self.type == "any"):
            return "any"
        elif (self.type == "range"):
            if (self.lowPort == -1):
                return ":" + str(self.highPort)
            else:
                if (self.highPort == -1):
                    return str(self.lowPort) + ":"
                else:
                    return str(self.lowPort) + ":" + str(self.highPort)
        elif (self.type == "list"):
            return self.listPorts.__repr__()