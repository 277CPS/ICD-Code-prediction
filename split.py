import json
import random


def split_dataset(file_path, validation_size=80):
    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 随机抽取验证集
        if len(data) < validation_size:
            raise ValueError("数据集中的数据数量少于验证集所需数量。")

        validation_indices = random.sample(range(len(data)), validation_size)
        validation_set = [data[i] for i in validation_indices]

        # 生成训练集
        train_set = [data[i] for i in range(len(data)) if i not in validation_indices]

        # 保存验证集和训练集
        with open('validation_set.json', 'w', encoding='utf-8') as val_file:
            json.dump(validation_set, val_file, ensure_ascii=False, indent=4)

        with open('train_set.json', 'w', encoding='utf-8') as train_file:
            json.dump(train_set, train_file, ensure_ascii=False, indent=4)

        print("验证集和训练集已成功分离并保存。")
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except json.JSONDecodeError:
        print(f"错误: 无法解析 {file_path} 中的JSON数据。")
    except ValueError as ve:
        print(f"错误: {ve}")


# 使用示例
file_path = 'ICD-Coding-train.json'
split_dataset(file_path)