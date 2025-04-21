import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Twea
sample_size = 50

df = pd.read_csv('./website_classification.csv')

mapping = {
    "Adult": 0,
    "Art & Design": 1,
    "Software Dev.": 2,
    "Crime & Law": 3,
    "Education & Jobs": 4,
    "Hardware": 5,
    "Entertainment": 6,
    "Social Life": 7,
    "Fashion & Beauty": 8,
    "Finance & Business": 9,
    "Food & Dining": 10,
    "Games": 11,
    "Health": 12,
    "History": 13,
    "Home & Hobbies": 14,
    "Industrial": 15,
    "Literature": 16,
    "Politics": 17,
    "Religion": 18,
    "Science & Tech.": 19,
    "Software": 20,
    "Sports & Fitness": 21,
    "Transportation": 22,
    "Travel": 23,
}

reverse_mapping = {v: k for k, v in mapping.items()}

tokenizer = AutoTokenizer.from_pretrained("WebOrganizer/TopicClassifier")
model = AutoModelForSequenceClassification.from_pretrained(
    "WebOrganizer/TopicClassifier",
    trust_remote_code=True,
    use_memory_efficient_attention=False
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

sample_df = df.sample(n=sample_size, random_state=42).copy()

sample_df["Sample_Text"] = sample_df.apply(
    lambda row: row['cleaned_website_text'],
    axis=1
)

with torch.no_grad():
    inputs = tokenizer(
        sample_df["Sample_Text"].tolist(),
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model(**inputs)
    preds = outputs.logits.softmax(dim=-1).argmax(dim=-1).cpu().tolist()

sample_df["Predicted_Label"] = [reverse_mapping.get(p, "Unknown") for p in preds]

print(sample_df[['website_url', 'Category', 'Predicted_Label', 'Sample_Text']])
