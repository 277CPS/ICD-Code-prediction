import json


def merge_json_records(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1:
            data1 = json.load(file1)
        with open(file2_path, 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)

        merged_data = []
        deleted_content = {}
        for record1 in data1:
            for record2 in data2:
                if record1["病案标识"] == record2["病案标识"]:
                    result2 = record2['预测结果']
                    if record1['预测结果'] in result2:
                        removed = record1['预测结果']
                        result2 = result2.replace(record1['预测结果'], '').strip()
                        if result2 == '':
                            result2 = record1['预测结果']
                        if record1["病案标识"] not in deleted_content:
                            deleted_content[record1["病案标识"]] = []
                        deleted_content[record1["病案标识"]].append(removed)
                    merged_result = f"[{record1['预测结果']}|{result2}]"
                    merged_record = {
                        "病案标识": record1["病案标识"],
                        "预测结果": merged_result
                    }
                    merged_data.append(merged_record)
        if deleted_content:
            print("删除的内容：")
            for case_id, removed in deleted_content.items():
                print(f"病案标识 {case_id}: {', '.join(removed)}")
        return merged_data
    except FileNotFoundError:
        print("错误：文件未找到。")
    except json.JSONDecodeError:
        print("错误：JSON 文件解析失败。")
    except Exception as e:
        print(f"错误：发生了未知错误：{e}")


file1_path = 'Mdev.json'
file2_path = 'dev-oT.json'
merged_result = merge_json_records(file1_path, file2_path)
if merged_result:
    try:
        with open('dev+dev-oT.json', 'w', encoding='utf-8') as output_file:
            json.dump(merged_result, output_file, ensure_ascii=False, indent=4)
        print("融合结果已成功写入 Tm1+other5.json 文件。")
    except Exception as e:
        print(f"写入文件时出现错误：{e}")
