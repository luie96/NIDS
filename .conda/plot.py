import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report
from pathlib import Path
from load_data import *

# 在代码库中添加可视化函数
def plot_feature_distributions(df, save_path):
    """特征分布可视化"""
    # 筛选数值
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # 设置画布和子图布局
    plt.figure(figsize=(15, 20))
    # 绘制每个特征的分布图
    for i, col in enumerate(numeric_cols, 1):
        plt.subplot(8, 4, i)
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f'Distribution of {col}')
        plt.xlabel(col)
    # 调整布局并保存
    plt.tight_layout()
    plt.savefig(save_path / 'feature_distributions.png')
    plt.close()

def plot_correlation_matrix(df, save_path):
    """特征相关性矩阵"""
    # 1. 筛选数值型列并删除非数值列（如字符串）
    numeric_df = df.select_dtypes(include=[np.number])
    

    # 2. 计算相关系数矩阵
    corr = numeric_df.corr()
    
    # 3. 绘制热力图
    plt.figure(figsize=(20, 15))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Feature Correlation Matrix')
    plt.xticks(rotation=45, ha='right')  # 旋转x轴标签并右对齐
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # 4. 保存结果
    plt.savefig(save_path / 'correlation_matrix.png')
    plt.close()


def plot_anomaly_probability(anomaly_probabilities, save_path):
    """异常概率分布直方图"""
    plt.figure(figsize=(10, 6))
    sns.histplot(anomaly_probabilities, kde=True, bins=20)
    plt.title('Distribution of Anomaly Probabilities')
    plt.xlabel('Probability')
    plt.ylabel('Frequency')
    plt.savefig(save_path / 'anomaly_probability.png')
    plt.close()


def plot_confusion_matrix(y_true, y_pred, save_path):
    """混淆矩阵"""
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap='Blues')
    plt.title('Confusion Matrix')
    plt.savefig(save_path / 'confusion_matrix.png')
    plt.close()

def plot_classification_report(y_true, y_pred, save_path):
    """分类报告文本图"""
    report = classification_report(y_true, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    plt.figure(figsize=(10, 6))
    sns.heatmap(report_df.iloc[:-1, :].astype(float), annot=True, cmap='viridis')
    plt.title('Classification Report')
    plt.savefig(save_path / 'classification_report.png')
    plt.close()


def plot_anomaly_ratio(test_df, save_path):
    """异常比例饼图"""
    # 统计类别分别
    counts = test_df['CLASS_TYPE'].value_counts()
    print("CLASS_TYPE 类别及数量：")
    print(counts)  # 输出实际类别和数量
    # 定义标签
    labels = ['Normal', 'Anomaly']
    # 绘制饼图
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    # 添加标题并保存
    plt.title('Anomaly Detection Results')
    plt.savefig(save_path / 'anomaly_ratio.png')
    plt.close()

def plot_feature_comparison(df, feature, save_path):
    """特征对比箱线图"""
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='CLASS_TYPE', y=feature, data=df)
    plt.title(f'{feature} Distribution by Class Type')
    plt.xlabel('Class Type (0=Normal, 1=Anomaly)')
    plt.ylabel(feature)
    plt.savefig(save_path / f'{feature}_comparison.png')
    plt.close()


def plot():


    alldata = load_database()

    # 创建可视化保存目录
    vis_dir = Path('data/vis')
    vis_dir.mkdir(parents=True, exist_ok=True)

    # 异常比例可视化
    plot_feature_distributions(alldata, vis_dir)
    plot_correlation_matrix(alldata, vis_dir)

    # 示例调用其他函数，这里使用占位符数据
    y_true = alldata['CLASS_TYPE']  # 替换为实际的真实标签
    y_pred = alldata['CLASS_TYPE']  # 替换为实际的预测标签
    anomaly_probabilities = np.random.rand(len(alldata))  # 替换为实际的概率数组
    test_df = alldata.copy()  # 替换为实际的测试数据集
    feature = 'DURATION'  # 替换为实际的特征名称

    plot_anomaly_probability(anomaly_probabilities, vis_dir)
    plot_confusion_matrix(y_true, y_pred, vis_dir)
    plot_classification_report(y_true, y_pred, vis_dir)
    plot_anomaly_ratio(test_df, vis_dir)
    plot_feature_comparison(df=alldata, feature=feature, save_path=vis_dir)



