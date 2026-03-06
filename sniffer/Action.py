# 为系统提供了统一的动作标识规范，用于处理检测到数据包时的响应逻辑，确保规则解析的正确性

from enum import Enum  

# 定义action枚举类，定义枚举成员alert，其值为1，表示当NIDS检测到数据包时刻采取发出警报的操作
class Action(Enum):
    ALERT = 1

def action(istr):
    str = istr.lower().strip()
    if (str == "alert"):
        return Action.ALERT
    else:
        raise ValueError("Invalid rule : incorrect action : '" + istr + "'.")
