from scapy.all import *
import logging
from RuleFileReader import *
from Sniffer import *
from configure_logging import *
from process_packet import *
import write_to_csv

RED = '\033[91m'
BLUE = '\033[34m'
GREEN = '\033[32m'
ENDC = '\033[0m'


def main(filename):
    # 初始化日志系统
    try:
        log_file = configure_logging()
        logging.info(f"Starting NIDS with rule file: {filename}")
    except Exception as e:
        print(f"Critical error: {str(e)}")
        return

    # 读取规则文件
    try:
        global ruleList
        ruleList, errorCount = read(filename)
    except Exception as e:
        print(f"Critical error: {e}")
        return
    
 

    # 存储匹配的数据包信息
    matches = []

    # # 开始网络数据包嗅探
    sniffer = Sniffer(ruleList,matches)
    # # 调用 Sniffer 实例的 start 方法，启动嗅探过程
    sniffer.start()

    # 等待用户输入或程序结束时保存结果到 CSV 文件
    try:
        input("Press Enter to stop sniffing and save results to CSV...\n")
        sniffer.stop()  # 停止嗅探
        sniffer.join()  # 等待线程结束
    except KeyboardInterrupt:
        sniffer.stop()  # 捕获键盘中断，停止嗅探
        sniffer.join()  # 等待线程结束

    # 将匹配结果写入 CSV 文件
    write_to_csv(matches)
    print(f"Sniffing stopped. Results saved to sniff_results.csv")

    # # 运行主循环
    # root.mainloop()

# 初始化一个空的规则列表
ruleList = list()
if __name__ == "__main__":
    default_rule_file = "rules/exampleRules.txt"  # 请根据实际情况修改路径
    main(default_rule_file)




 
    # # 加载攻击特征库
    # attack_features = load_attack_features_from_database()

    # # 实时匹配与检测循环
    # while True:
    #     real_time_data = get_real_time_data()  # 从数据采集模块获取实时数据
    #     detection_results = ac.search(real_time_data)
    #     handle_detection_results(detection_results)