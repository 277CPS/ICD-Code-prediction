import numpy as np
from datasets import load_from_disk
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from transformers import (
    AutoTokenizer, 
    TrainingArguments,
    Trainer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding
)
from transformers import AutoConfig
from peft import (
    PeftModel,
    LoraConfig,
    TaskType,
    get_peft_model,
)
from datasets import load_from_disk
import pandas as pd
from torch.utils.data import DataLoader
import torch
from tqdm import tqdm
tokenizer = AutoTokenizer.from_pretrained("/gemini/pretrain3/qwen")

model = AutoModelForSequenceClassification.from_pretrained("/gemini/code/分类/results/checkpoint-2400", num_labels=5)
model = PeftModel.from_pretrained(model, model_id="/gemini/code/分类/results/checkpoint-2400")
test_data = load_from_disk("/gemini/code/分类/test_data")
def tokenize(examples):
    instruction_ids = tokenizer(examples["input"],  padding="max_length",truncation=True,max_length=2048)
    return {
        "input_ids": instruction_ids["input_ids"],
        "attention_mask": instruction_ids["attention_mask"]
}
tokenizer.pad_token = tokenizer.eos_token
test_data = test_data.map(tokenize, remove_columns=test_data.column_names,num_proc=4)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer, padding=True)
test_dataloader = DataLoader(test_data, batch_size=1, collate_fn = data_collator)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
predictions = []

# 推理
with torch.no_grad():
    for batch in tqdm(test_dataloader):
        # 将数据移动到设备
        batch = {k: v.to(device) for k, v in batch.items()}
        
        # 获取模型输出
        outputs = model(**batch)
        
        # 获取预测结果（最高概率的类别）
        preds = outputs.logits.argmax(-1).cpu().numpy()
        predictions.extend(preds)
        print(preds)
df = pd.DataFrame(predictions, columns=['Predictions'])
df.to_csv('predictions.csv', index=False)