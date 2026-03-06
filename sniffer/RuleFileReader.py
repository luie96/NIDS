# 实现了规则文件的读取、解析及错误处理
from Rule import *

def read(filename):
    """
    读取包含规则的输入文件，并返回规则列表和解析错误的行数。
    :param filename: 包含规则的文件的名称
    :return: 一个元组，包含解析后的规则列表和解析错误的行数
    """
    
    l = list()
    with open(filename, 'r') as f:
        ruleErrorCount = 0
        for line in f:
            try:
                rule = Rule(line)
                l.append(rule)
            except ValueError as err:
                ruleErrorCount += 1
                print(err)
    return l, ruleErrorCount