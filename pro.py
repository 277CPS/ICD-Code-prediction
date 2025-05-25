
import json

try:
    # 从 JSON 文件中读取所有病案标识
    with open('ICD-Coding-test-B.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        case_identifiers = []
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict) and '病案标识' in item:
                    case_identifiers.append(item['病案标识'])
        elif isinstance(json_data, dict) and '病案标识' in json_data:
            case_identifiers.append(json_data['病案标识'])

    # 从 JSONL 文件中读取所有 predict 字段内容
    predict_values = []
    with open('mtt-5e-8e-5-2bs-dmtte.jsonl', 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            try:
                line_data = json.loads(line)
                if 'predict' in line_data:
                    predict_values.append(line_data['predict'])
            except json.JSONDecodeError:
                print("解析 JSONL 文件中的某行时出错，请检查文件内容。")

    # 确定循环次数，取两者长度的最小值
    min_length = min(len(case_identifiers), len(predict_values))

    merged_data_list = []
    for i in range(min_length):
        merged_data = {
            "病案标识": case_identifiers[i],
            "预测结果": predict_values[i]
        }
        merged_data_list.append(merged_data)

    # 将合并后的数据保存到新的 JSON 文件
    with open('mtt-5e-8e-5-2bs-dmtte.json', 'w', encoding='utf-8') as out_file:
        json.dump(merged_data_list, out_file, ensure_ascii=False, indent=4)

    print("数据抽取与合并完成，结果已保存到 new_result.json 文件中。")

except FileNotFoundError:
    print("未找到指定的文件，请确保文件存在。")
except json.JSONDecodeError:
    print("文件格式有误，请检查文件内容。")