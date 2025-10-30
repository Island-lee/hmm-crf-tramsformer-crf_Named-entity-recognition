import json
from datetime import datetime, timedelta
import requests
from typing import List

# pod_id
def get_all_metrics_from_prometheus(ip: str, port: str) -> List:
    PROMETHEUS_API_URL = f"http://{ip}:{port}"
    url = f"{PROMETHEUS_API_URL}/api/v1/label/__name__/values"
    response = requests.get(url)
    metric_names = []
    if response.status_code == 200:
        data = response.json()
        metric_names = data.get('data', [])
        print("=== 所有 Prometheus Metric 名称 ===")
        output_file = "all_metrics.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for name in metric_names:
                f.write(name + '\n')
    else:
        print(f"获取 metric 名称失败，状态码: {response.status_code}")
        print(response.text)

    return metric_names

def get_label_keys_for_metric(ip: str, port: str, metric_name: str):
    PROMETHEUS_API_URL = f"http://{ip}:{port}"
    url = f"{PROMETHEUS_API_URL}/api/v1/series"
    end = int(datetime.now().timestamp())
    start = int((datetime.now() - timedelta(hours=1)).timestamp())

    params = {
        'match[]': f'{{__name__="{metric_name}"}}',
        'start': start,
        'end': end
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"获取 metric '{metric_name}' 的 label keys 失败，状态码: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    metric_series = data.get('data', [])

    label_keys_set = set()
    for series in metric_series:
        labels = list(series.keys())
        labels = [label for label in labels if label != "__name__"]
        label_keys_set.update(labels)

    return sorted(label_keys_set)  # 排序后返回，方便阅读


def save_to_json(metric_label_data, filename="metrics_with_labels.json"):
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(metric_label_data, f, ensure_ascii=False, indent=2)
    print(f"所有 Metrics 及其 Label Keys 已保存到 JSON 文件：{filename}")


if __name__ == "__main__":
    server = "192.168.122.100"
    port = "9090"
    metric_names = get_all_metrics_from_prometheus(server, port)
    print(metric_names)
    all_metric_label_data = {}
    for metric_name in metric_names:
        metric_labels = get_label_keys_for_metric(server, port, metric_name)
        all_metric_label_data[metric_name] = metric_labels

    save_to_json(all_metric_label_data)

