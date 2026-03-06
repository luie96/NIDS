import oracledb
import pandas as pd
from data_clean import *

# 数据库连接信息
username = "Luie"
password = "luie123"
dsn = "localhost:1521/ORCL"

def create_connection():
    """
    创建并返回数据库连接。
    """
    try:
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        print("成功连接数据库！")
        return connection
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"连接失败：{error.message}")
        return None

def insert_data_to_database(data_file):
    """
    将清洗后的数据插入到数据库中，并确保 rate 字段的数据格式为 0.00。
    """
    db_connection = create_connection()
    if db_connection is not None:
        try:
            cursor = db_connection.cursor()
            
            # 检查并删除序列
            try:
                cursor.execute("DROP SEQUENCE attack_features_seq")
            except oracledb.DatabaseError as e:
                error, = e.args
                if error.code != 2289:  # 2289 表示序列不存在
                    raise
            
            # 检查并删除表
            try:
                cursor.execute("DROP TABLE attack_features CASCADE CONSTRAINTS")
            except oracledb.DatabaseError as e:
                error, = e.args
                if error.code != 942:  # 942 表示表不存在
                    raise
            
            # 创建序列用于自增主键
            cursor.execute("""
                CREATE SEQUENCE attack_features_seq
                START WITH 1
                INCREMENT BY 1
            """)
            
            # 创建表
            cursor.execute("""
                CREATE TABLE attack_features (
                    id NUMBER PRIMARY KEY,
                    duration VARCHAR2(255),       
                    protocol_type VARCHAR2(255),
                    service VARCHAR2(255),
                    flag VARCHAR2(255),
                    src_bytes NUMBER,
                    dst_bytes NUMBER,
                    land NUMBER,
                    wrong_fragment NUMBER,
                    hot NUMBER,
                    num_failed_logins NUMBER,
                    logged_in NUMBER,
                    num_compromised NUMBER,
                    is_guest_login NUMBER,
                    count NUMBER,
                    srv_count NUMBER,
                    serror_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    rerror_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    srv_rerror_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    same_srv_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    diff_srv_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    srv_diff_host_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_count NUMBER,
                    dst_host_srv_count NUMBER,
                    dst_host_same_srv_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_diff_srv_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_same_src_port_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_srv_diff_host_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_serror_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_srv_serror_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_rerror_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    dst_host_srv_rerror_rate NUMBER(10, 2),  -- 修改为保留小数点后两位
                    class_type NUMBER
                )
            """)
            
            # 创建触发器，用于自动填充自增主键
            cursor.execute("""
                CREATE OR REPLACE TRIGGER attack_features_trg
                BEFORE INSERT ON attack_features
                FOR EACH ROW
                BEGIN
                    SELECT attack_features_seq.NEXTVAL INTO :new.id FROM DUAL;
                END;
            """)
            
            # 插入数据
            cleaned_data = pd.read_csv(data_file)
            for _, row in cleaned_data.iterrows():
                cursor.execute("""
                    INSERT INTO attack_features (
                        duration, protocol_type, service, flag, src_bytes, dst_bytes, land, wrong_fragment, hot, num_failed_logins, 
                        logged_in, num_compromised, is_guest_login, count, srv_count, serror_rate, rerror_rate,
                        srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate, dst_host_count,
                        dst_host_srv_count, dst_host_same_srv_rate, dst_host_diff_srv_rate,
                        dst_host_same_src_port_rate, dst_host_srv_diff_host_rate, dst_host_serror_rate,
                        dst_host_srv_serror_rate, dst_host_rerror_rate, dst_host_srv_rerror_rate, class_type
                    ) VALUES (
                        :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20,
                        :21, :22, :23, :24, :25, :26, :27, :28, :29, :30, :31, :32
                    )
                """, (
                    row.get('duration', None), 
                    row.get('protocol_type', None), 
                    row.get('service', None), 
                    row.get('flag', None), 
                    row.get('src_bytes', None), 
                    row.get('dst_bytes', None), 
                    row.get('land', None), 
                    row.get('wrong_fragment', None), 
                    row.get('hot', None), 
                    row.get('num_failed_logins', None), 
                    row.get('logged_in', None), 
                    row.get('num_compromised', None), 
                    row.get('is_guest_login', None),
                    row.get('count', None), 
                    row.get('srv_count', None), 
                    float(f"{row.get('serror_rate', 0.0):.2f}"), 
                    float(f"{row.get('rerror_rate', 0.0):.2f}"),
                    float(f"{row.get('srv_rerror_rate', 0.0):.2f}"), 
                    float(f"{row.get('same_srv_rate', 0.0):.2f}"), 
                    float(f"{row.get('diff_srv_rate', 0.0):.2f}"), 
                    float(f"{row.get('srv_diff_host_rate', 0.0):.2f}"), 
                    row.get('dst_host_count', None),
                    row.get('dst_host_srv_count', None), 
                    float(f"{row.get('dst_host_same_srv_rate', 0.0):.2f}"), 
                    float(f"{row.get('dst_host_diff_srv_rate', 0.0):.2f}"),
                    float(f"{row.get('dst_host_same_src_port_rate', 0.0):.2f}"), 
                    float(f"{row.get('dst_host_srv_diff_host_rate', 0.0):.2f}"), 
                    float(f"{row.get('dst_host_serror_rate', 0.0):.2f}"),
                    float(f"{row.get('dst_host_srv_serror_rate', 0.0):.2f}"), 
                    float(f"{row.get('dst_host_rerror_rate', 0.0):.2f}"), 
                    float(f"{row.get('dst_host_srv_rerror_rate', 0.0):.2f}"), 
                    row.get('class_type', None)
                ))
            
            db_connection.commit()
            print("数据已成功插入到 Oracle 数据库中。")


        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"数据库操作出错：{error.message}")
            db_connection.rollback()
        finally:
            if cursor:
                cursor.close()
            db_connection.close()
            print("数据库连接已关闭。")

