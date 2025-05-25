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
tokenizer = AutoTokenizer.from_pretrained("/usr/local/share/LLMs/Qwen2.5-7B-Instruct-1M/Qwen/Qwen2.5-7B-Instruct-1M")
model = AutoModelForSequenceClassification.from_pretrained(
    "/usr/local/share/LLMs/Qwen2.5-7B-Instruct-1M/Qwen/Qwen2.5-7B-Instruct-1M",
    num_labels=5  # 自定义风险等级数量（0-4）
)

train_data = load_from_disk("/home/chenpusheng/CCLT8/train_data/gemini/code/分类/train_data")

def tokenize(examples):
    instruction_ids = tokenizer(examples["input"],  padding="max_length",truncation=True,max_length=1024)
    return {
        "input_ids": instruction_ids["input_ids"],
        "attention_mask": instruction_ids["attention_mask"],
        "label": int(examples["output"])
}
train_data = train_data.map(tokenize, remove_columns=train_data.column_names,num_proc=4)


lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=False, # 训练模式
    r=8, # Lora 秩
    lora_alpha=16, # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.1# Dropout 比例
)
model = get_peft_model(model, lora_config)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    logging_steps=100,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    num_train_epochs=3,
    warmup_ratio=0.2,
    save_strategy="epoch",
    logging_dir='./logs',
    gradient_checkpointing=True,
    bf16=True
)
#train
trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
    )
trainer.train()