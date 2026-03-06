# NIDS 2.5

网络入侵检测系统（Network Intrusion Detection System）2.5 版本，包含基于规则的实时流量嗅探与基于特征的异常检测模块。

## 项目结构

```
NIDS_2.5/
├── sniffer/           # 实时数据包嗅探与规则匹配
│   ├── NIDS.py        # 主入口：加载规则、启动嗅探、保存结果
│   ├── Sniffer.py     # 嗅探线程与抓包逻辑
│   ├── RuleFileReader.py  # 规则文件解析
│   ├── Rule.py        # 规则定义与匹配
│   ├── process_packet.py  # 数据包处理与告警
│   ├── gui.py         # 图形界面（wxPython）
│   └── ...
├── .conda/            # 异常检测与数据分析
│   ├── entrance.py    # 入口：数据库特征、Aho-Corasick 匹配、绘图
│   ├── Aho_corasick.py    # Aho-Corasick 多模式匹配
│   ├── database.py    # Oracle 数据库连接与读写
│   ├── load_data.py   # 数据加载
│   ├── data_clean.py  # 数据清洗
│   └── plot.py        # 可视化（混淆矩阵等）
├── rules/             # 检测规则（类 Snort 语法）
│   └── exampleRules.txt
├── data/              # 数据文件（如 cleaned_data.csv、anomaly_data.csv）
└── logs/              # 运行日志
```

## 功能概览

- **规则引擎**：从 `rules/` 读取规则文件，对实时流量进行协议、端口、内容等匹配并告警。
- **数据包嗅探**：基于 Scapy 抓包，将匹配结果写入 CSV（如 `sniff_results.csv`）。
- **异常检测**：从数据库加载特征集，用 Aho-Corasick 与测试集比对，输出异常比例并保存异常数据。
- **可视化**：混淆矩阵、分类报告等（matplotlib/seaborn）。

## 环境要求

- Python 3.x
- 主要依赖：`scapy`、`pandas`、`matplotlib`、`seaborn`、`numpy`、`scikit-learn`、`oracledb`、`wxPython`

（可选）使用 conda 或 pip 安装依赖，例如：

```bash
pip install scapy pandas matplotlib seaborn numpy scikit-learn oracledb wxPython
```

**注意**：`.conda` 模块依赖 Oracle 数据库，需配置 `database.py` 中的连接信息（建议使用环境变量，勿将密码提交到仓库）。

## 运行方式

### 嗅探模块（sniffer）

在项目根目录下，确保规则文件路径正确（默认 `rules/exampleRules.txt`），然后执行：

```bash
cd sniffer
python NIDS.py
```

按提示按 Enter 停止嗅探，结果会保存到 CSV。

### 异常检测模块（.conda）

需先配置数据库并准备好特征数据与测试数据路径（如 `data/cleaned_data.csv`），然后：

```bash
cd .conda
python entrance.py
```

## 规则文件格式

规则文件为每行一条规则，语法示例（见 `rules/exampleRules.txt`）：

```
alert udp any any -> 8.8.8.8 53 (msg:"DNS to Google"; service:DNS;)
alert tcp any any -> any 80 (msg:"HTTP traffic"; service:HTTP; content:"GET";)
```

支持协议（如 tcp/udp）、源/目的地址与端口、以及简单 content 匹配。

## 许可证

请根据项目实际情况添加或修改许可证信息。
