import csv


def write_to_csv(matches, filename="sniff_results.csv"):
    """
    将匹配的数据包信息写入 CSV 文件。

    参数:
        matches: 包含匹配数据包信息的列表
        filename: 输出的 CSV 文件名（默认: "sniff_results.csv"）
    """
    # 定义 CSV 文件的表头
    headers = [
        "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
        "land", "wrong_fragment", "hot", "num_failed_logins", "logged_in",
        "num_compromised", "is_guest_login", "count", "srv_count", "serror_rate",
        "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
        "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
        "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
        "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate",
        "dst_host_srv_rerror_rate", "class"
    ]

    # 写入 CSV 文件
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()  # 写入表头
        for match in matches:
            writer.writerow(match)  # 写入每一行数据