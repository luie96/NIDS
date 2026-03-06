from collections import deque
import pandas as pd

class AhoCorasick:
    def __init__(self):
        self.root = {'children': {}, 'fail': None, 'output': []}

    def add_pattern(self, pattern, pattern_id):
        node = self.root
        for char in pattern:
            if char not in node['children']:
                node['children'][char] = {'children': {}, 'fail': None, 'output': []}
            node = node['children'][char]
        node['output'].append(pattern_id)

    def build_failure_links(self):
        queue = deque()
        self.root['fail'] = self.root
        for char, child in self.root['children'].items():
            child['fail'] = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for char, child in current['children'].items():
                queue.append(child)
                fail_node = current['fail']
                while fail_node != self.root and char not in fail_node['children']:
                    fail_node = fail_node['fail']
                if char in fail_node['children']:
                    child['fail'] = fail_node['children'][char]
                else:
                    child['fail'] = self.root

    def search(self, text):
        current = self.root
        results = []
        for i, char in enumerate(text):
            while current != self.root and char not in current['children']:
                current = current['fail']
            if char in current['children']:
                current = current['children'][char]
            temp = current
            while temp != self.root:
                if temp['output']:
                    for pattern_id in temp['output']:
                        results.append((pattern_id, i - len(text) + 1))
                temp = temp['fail']
        return results

def compare_features(database_features, test_data):
    if not isinstance(database_features, pd.DataFrame):
        raise TypeError("database_features 必须是 Pandas DataFrame 类型")
    if not isinstance(test_data, pd.DataFrame):
        raise TypeError("test_data 必须是 Pandas DataFrame 类型")
    
    if not(set(database_features.columns[:-1]) == set(test_data.columns[:-1])):
        raise ValueError("database_features和test_data的列名不一致")

    patterns = []
    pattern_strings = []
    for idx, feature in database_features.iterrows():
        if feature['CLASS_TYPE'] == 1:  
            pattern = feature.drop('CLASS_TYPE').to_dict()
            patterns.append(pattern)
            pattern_str = ",".join([f"{k}={v}" for k, v in pattern.items()])
            pattern_strings.append(pattern_str)

    if not patterns:
        print("没有异常模式，无法检测异常。")
        return pd.DataFrame(), 0, 0.0

    ac = AhoCorasick()
    for idx, pattern_str in enumerate(pattern_strings):
        ac.add_pattern(pattern_str, idx)
        
    ac.build_failure_links()

    result_df = test_data.copy()
    result_df['CLASS_TYPE'] = 0  

    anomaly_data = []

    for idx, row in result_df.iterrows():
        test_feature = row.drop(['CLASS_TYPE']).to_dict()
        test_str = ",".join([f"{k}={v}" for k, v in test_feature.items()])
        matches = ac.search(test_str)
        if matches:
            result_df.at[idx, 'CLASS_TYPE'] = 1
            anomaly_row = row.copy()
            anomaly_row['CLASS_TYPE'] = 1
            anomaly_data.append(anomaly_row)

    anomaly_data = pd.DataFrame(anomaly_data)
    anomaly_count = len(anomaly_data)
    anomaly_ratio = anomaly_count / len(test_data) if not test_data.empty else 0.0
    return anomaly_data, anomaly_count, anomaly_ratio
