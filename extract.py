import json

try:
    with open('GP.jsonl', 'r', encoding='utf-8') as infile:
        with open('NF.jsonl', 'w', encoding='utf-8') as outfile:
            for line in infile:
                try:
                    data = json.loads(line)
                    if 'predict' in data:
                        outfile.write(json.dumps(data['predict'], ensure_ascii=False) + '\n')
                except json.JSONDecodeError:
                    print("解析 JSONL 文件中的某行时出错，请检查文件内容。")
    print("数据抽取完成，结果已保存到 new_file.jsonl 文件中。")
except FileNotFoundError:
    print("未找到指定的 JSONL 文件，请确保文件存在。")
