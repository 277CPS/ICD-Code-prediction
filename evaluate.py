import json


def calculate_accuracy_and_print_errors(answer_file, output_file):
    try:
        # 读取答案文件
        with open(answer_file, 'r', encoding='utf-8') as f:
            answers = json.load(f)
        # 读取输出文件
        with open(output_file, 'r', encoding='utf-8') as f:
            outputs = json.load(f)

        # 创建答案字典，方便查找
        answer_dict = {item["病案标识"]: item["预测结果"] for item in answers}

        correct_count = 0
        total_count = len(outputs)

        for output in outputs:
            case_id = output["病案标识"]
            predicted_result = output["预测结果"]
            if case_id in answer_dict and answer_dict[case_id] == predicted_result:
                correct_count += 1
            else:
                print(f"病案标识: {case_id}, 预测结果: {predicted_result}, 正确答案: {answer_dict.get(case_id, '未知')}")

        accuracy = correct_count / total_count if total_count > 0 else 0
        return accuracy

    except FileNotFoundError:
        print("错误：文件未找到。")
    except json.JSONDecodeError:
        print("错误：JSON文件解析失败。")
    except KeyError:
        print("错误：JSON文件中缺少必要的键。")


# 示例调用
answer_file = 'Mdev.json'
output_file = 'MMTT2EtF.json'
accuracy = calculate_accuracy_and_print_errors(answer_file, output_file)
print(f"准确率: {accuracy * 100:.2f}%")