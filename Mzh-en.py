import json

# 定义中文名称到编码的映射
chinese_to_code = {
    "微血管性心绞痛": "I20.800x007",
    "急性非ST段抬高型心肌梗死": "I21.401",
    "甲状腺结节": "E04.101",
    "甲状腺囊肿": "E04.102",
    "2型糖尿病": "E11.900",
    "糖尿病": "E14.900x001",
    "高同型半胱氨酸血症": "E72.101",
    "高脂血症": "E78.500",
    "低钾血症": "E87.600",
    "高血压病1级（高危）": "I10.x00x023",
    "高血压病1级（极高危）": "I10.x00x024",
    "高血压病2级（高危）": "I10.x00x027",
    "高血压病2级（极高危）": "I10.x00x028",
    "高血压病3级（高危）": "I10.x00x031",
    "高血压病3级（极高危）": "I10.x00x032",
    "不稳定型心绞痛": "I20.000",
    "冠状动脉粥样硬化": "I25.102",
    "冠状动脉粥样硬化性心脏病": "I25.103",
    "陈旧性心肌梗死": "I25.200",
    "心包积液": "I31.800x004",
    "心脏瓣膜病": "I38.x01",
    "心房颤动": "I48.x01",
    "阵发性心房颤动": "I48.x02",
    "房性期前收缩[房性早搏]": "I49.100x001",
    "频发性房性期前收缩": "I49.100x002",
    "频发性室性期前收缩": "I49.300x001",
    "室性期前收缩": "I49.300x002",
    "偶发房室性期前收缩": "I49.400x002",
    "频发性期前收缩": "I49.400x003",
    "心律失常": "I49.900",
    "心功能Ⅱ级(NYHA分级)": "I50.900x007",
    "心功能III级(NYHA分级)": "I50.900x008",
    "心功能IV级(NYHA分级)": "I50.900x010",
    "KillipII级": "I50.900x014",
    "KillipIII级": "I50.900x015",
    "KillipIV级": "I50.900x016",
    "慢性心功能不全急性加重": "I50.900x018",
    "急性心力衰竭": "I50.907",
    "脑梗死": "I63.900",
    "脑动脉粥样硬化": "I67.200x011",
    "陈旧性脑梗死": "I69.300x002",
    "下肢动脉粥样硬化": "I70.203",
    "颈动脉硬化": "I70.806",
    "肺炎": "J18.900",
    "肺部感染": "J98.414",
    "脂肪肝": "K76.000",
    "肝囊肿": "K76.807",
    "肾功能不全": "N19.x00x002",
    "单纯性肾囊肿": "N28.101",
    "冠状动脉肌桥": "Q24.501",
    "头晕": "R42.x00x004",
    "肺诊断性影像异常": "R91.x00x003",
    "青光眼术后": "Z54.000x033",
    "冠状动脉支架植入后状态": "Z95.501",
    "乳腺术后": "Z98.800x612"
}

try:
    # 读取 JSON 文件
    with open('MTTE-3E.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 遍历每个数据项，替换预测结果中的中文名称为编码
    for item in data:
        prediction = item.get('预测结果', '')
        # 查找对应的编码
        code = chinese_to_code.get(prediction.strip(), prediction.strip())
        item['预测结果'] = code

    # 将处理后的数据保存到新的 JSON 文件
    with open('MTTE-3EF.json', 'w', encoding='utf-8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent=4)

    print("中文名称已成功替换为编码，并保存到 output.json 文件中。")
except FileNotFoundError:
    print("未找到指定的 JSON 文件，请检查文件路径。")
except json.JSONDecodeError:
    print("JSON 文件格式错误，请检查文件内容。")
