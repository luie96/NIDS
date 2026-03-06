import pandas as pd
import oracledb
import logging
import sys
import os


def load_database():
    """从数据库中加载所有特征集"""
    try:
        # user 参数指定数据库用户名，password 参数指定用户密码，dsn 参数指定数据库服务名
        db_connection = oracledb.connect(user="Luie", password="luie123", dsn="localhost:1521/ORCL")
        # 创建一个游标对象，用于执行 SQL 语句和获取查询结果
        cursor = db_connection.cursor()
        # 执行 SQL 查询语句，从 attack_features 表中选取所有记录
        cursor.execute("SELECT * FROM attack_features")

        # 获取列名
        column_names = [col[0] for col in cursor.description]
        # 获取数据
        features = cursor.fetchall()

        # 将数据和列名组合成 DataFrame
        features_df = pd.DataFrame(features, columns=column_names)

        # 排除 ID 列, 假设数据库列名是全大写
        features_df = features_df.drop(columns=['ID'], errors='ignore')  
        
        features_df['DURATION'] = pd.to_numeric(features_df['DURATION'], errors='coerce')
        # 将转换失败的值设为 NaN 或默认值
        features_df['DURATION'] = features_df['DURATION'].fillna(0)  # 根据业务逻辑选择填充方式
        
        # 定义需要格式化的 rate 字段列表
        rate_columns = [
            'SERROR_RATE', 'RERROR_RATE', 'SRV_RERROR_RATE', 'SAME_SRV_RATE',
            'DIFF_SRV_RATE', 'SRV_DIFF_HOST_RATE', 'DST_HOST_SAME_SRV_RATE',
            'DST_HOST_DIFF_SRV_RATE', 'DST_HOST_SAME_SRC_PORT_RATE',
            'DST_HOST_SRV_DIFF_HOST_RATE', 'DST_HOST_SERROR_RATE',
            'DST_HOST_SRV_SERROR_RATE', 'DST_HOST_RERROR_RATE',
            'DST_HOST_SRV_RERROR_RATE'
        ]

        # 对每个 rate 字段进行格式化
        for col in rate_columns:
            features_df[col] = pd.to_numeric(features_df[col], errors='coerce').round(2).astype(str)
            features_df[col] = features_df[col].apply(lambda x: f"{float(x):.2f}" if x != 'nan' else 'NaN')

        logging.info("成功从数据库加载所有特征集")

        return features_df
    except Exception as e:
        logging.error(f"从数据库加载特征集时出错: {e}")
        sys.exit(1)
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()



def load_database_features():
    """从数据库中加载异常特征集"""
    try:
        # user 参数指定数据库用户名，password 参数指定用户密码，dsn 参数指定数据库服务名
        db_connection = oracledb.connect(user="Luie", password="luie123", dsn="localhost:1521/ORCL")
        # 创建一个游标对象，用于执行 SQL 语句和获取查询结果
        cursor = db_connection.cursor()
         # 执行 SQL 查询语句，从 attack_features 表中选取所有 class_type 列为 1 的记录
        cursor.execute("SELECT * FROM attack_features WHERE class_type = 1")

        # 获取列名
        column_names = [col[0] for col in cursor.description]
        # 获取数据
        features = cursor.fetchall()

        # 将数据和列名组合成 DataFrame
        features_df = pd.DataFrame(features, columns=column_names)

        # 排除 ID 和 class_type 列, 假设数据库列名是全大写
        features_df = features_df.drop(columns=['ID'], errors='ignore')  
        
        features_df['DURATION'] = pd.to_numeric(features_df['DURATION'], errors='coerce')
        # 将转换失败的值设为 NaN 或默认值
        features_df['DURATION'] = features_df['DURATION'].fillna(0)  # 根据业务逻辑选择填充方式
        
        # 定义需要格式化的 rate 字段列表
        rate_columns = [
            'SERROR_RATE', 'RERROR_RATE', 'SRV_RERROR_RATE', 'SAME_SRV_RATE',
            'DIFF_SRV_RATE', 'SRV_DIFF_HOST_RATE', 'DST_HOST_SAME_SRV_RATE',
            'DST_HOST_DIFF_SRV_RATE', 'DST_HOST_SAME_SRC_PORT_RATE',
            'DST_HOST_SRV_DIFF_HOST_RATE', 'DST_HOST_SERROR_RATE',
            'DST_HOST_SRV_SERROR_RATE', 'DST_HOST_RERROR_RATE',
            'DST_HOST_SRV_RERROR_RATE'
        ]

        # 对每个 rate 字段进行格式化
        for col in rate_columns:
            features_df[col] = pd.to_numeric(features_df[col], errors='coerce').round(2).astype(str)
            features_df[col] = features_df[col].apply(lambda x: f"{float(x):.2f}" if x != 'nan' else 'NaN')

        logging.info("成功从数据库加载异常特征集")

        return features_df
    except Exception as e:
        logging.error(f"从数据库加载特征集时出错: {e}")
        sys.exit(1)
    finally:
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()

def load_test_data(file_path,known_columns, database_features):
    """加载测试数据"""
    try:
        test_df = pd.read_csv(file_path)
        
        # 将测试数据的列名转换为大写，并将下划线替换为空格（如果需要）
        test_df.columns = [col.upper().replace(' ', '_') for col in test_df.columns]
        
        # 错误代码片段（在 load_test_data 中）
        test_df = test_df.drop(columns=['ID'], errors='ignore')

        # 添加空的 CLASS_TYPE 列（值为 NaN）
        test_df['CLASS_TYPE'] = pd.NA  # 或者 test_df['CLASS_TYPE'] = None

        # 验证列名是否与已知列匹配
        if set(test_df.columns) != set(known_columns):
            logging.error(f"测试数据列与数据库特征列不匹配！测试列：{test_df.columns}，已知列：{known_columns}")
            sys.exit(1)        
        
        logging.info("成功加载测试数据")

        test_df['DURATION'] = test_df['DURATION'].astype('int64')

        # 定义需要格式化的 rate 字段列表
        rate_columns = [
            'SERROR_RATE', 'RERROR_RATE', 'SRV_RERROR_RATE', 'SAME_SRV_RATE',
            'DIFF_SRV_RATE', 'SRV_DIFF_HOST_RATE', 'DST_HOST_SAME_SRV_RATE',
            'DST_HOST_DIFF_SRV_RATE', 'DST_HOST_SAME_SRC_PORT_RATE',
            'DST_HOST_SRV_DIFF_HOST_RATE', 'DST_HOST_SERROR_RATE',
            'DST_HOST_SRV_SERROR_RATE', 'DST_HOST_RERROR_RATE',
            'DST_HOST_SRV_RERROR_RATE'
        ]

        # 对每个 rate 字段进行格式化
        for col in rate_columns:
            test_df[col] = pd.to_numeric(test_df[col], errors='coerce').round(2).astype(str)
            test_df[col] = test_df[col].apply(lambda x: f"{float(x):.2f}" if x != 'nan' else 'NaN')

        return test_df
    except Exception as e:
        logging.error(f"加载测试数据时出错: {e}")
        sys.exit(1)

def save_anomaly_data(anomaly_data):
    """保存异常数据到文件"""
    if anomaly_data.empty:
        logging.info("未发现异常数据。")
    else:
        # 将异常数据转换为 DataFrame
        anomaly_df = pd.DataFrame(anomaly_data)
        # 添加异常概率列
        # anomaly_df['anomaly_probability'] = anomaly_probabilities
        
        # 确保目录存在
        os.makedirs('data', exist_ok=True)
        
        # 保存到 CSV 文件
        anomaly_df.to_csv('data/anomaly_data.csv', index=False)
        logging.info("异常数据已保存到 anomaly_data.csv 文件中。")


