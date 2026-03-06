from Aho_corasick import compare_features
from load_data import *
from  data_clean import *
from database import *
from plot import *

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 

def main():

    # 从数据库中读取特征集
    database_features = load_database_features()
    
    # # 假设已知列是 database_features 的列名（不包含ID）
    known_columns = database_features.columns.tolist()

    # 读取测试集数据
    test_data = load_test_data('data/cleaned_data.csv', known_columns, database_features)
    
    plot()

    # 使用 Aho-Corasick 算法比较特征集与测试集
    anomaly_data_df, anomaly_count, anomaly_ratio = compare_features(database_features, test_data)
    print(f"异常数据的数量: {anomaly_count}")
    print(f"异常数据占总测试数据的比例: {anomaly_ratio * 100:.2f}%")

    # 保存异常数据
    save_anomaly_data(anomaly_data_df)



if __name__ == "__main__":
    main()