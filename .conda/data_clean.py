import pandas as pd
from database import *

def clean_data(input_file, output_file):
    """
    清洗数据并保存到指定文件。
    """
    # 读取数据
    df = pd.read_csv(input_file)
    
    # 1. 去除重复值
    df = df.drop_duplicates()
    
    # 2. 处理缺失值
    df = df.dropna()
    
    # 3. 标准化数据格式
    df['duration'] = df['duration'].astype(int)
    for col in df.columns:
        if 'bytes' in col:
            df[col] = df[col].astype(int)
    
    # 4. 特征选择，去除与入侵检测关联性较弱的特征
    columns_to_drop = ['urgent', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'srv_serror_rate']
    df = df.drop([col for col in columns_to_drop if col in df.columns], axis=1)
    
    # 5. 将分类标签转换为数值类型
    if 'class_type' in df.columns:
        df['class_type'] = df['class_type'].map({'normal': 0, 'anomaly': 1})
    
    # 保存清洗后的数据
    df.to_csv(output_file, index=False)


# # 数据清洗
# clean_data('data/train_data.csv', 'data/cleaned_data.csv')
# clean_data('data/test_data.csv', 'data/cleaned_test_data.csv')
#     # 将清洗后的训练集存入数据库
# insert_data_to_database('data/cleaned_data.csv')