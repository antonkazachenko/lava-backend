import pandas as pd
import torch
import sqlite3
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --------------------
# Configuration
# --------------------
sample_size = 100  # Number of CSV entries to process

# --------------------
# Load Data and Mapping
# --------------------
df = pd.read_csv('./website_classification.csv')

# Mapping: topic text → numeric index (0-based, 24 topics)
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
# Reverse mapping: numeric index → topic text
reverse_mapping = {v: k for k, v in mapping.items()}

# --------------------
# Load the Classifier
# --------------------
tokenizer = AutoTokenizer.from_pretrained("WebOrganizer/TopicClassifier")
model = AutoModelForSequenceClassification.from_pretrained(
    "WebOrganizer/TopicClassifier",
    trust_remote_code=True,
    use_memory_efficient_attention=False
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

# --------------------
# Prepare the Sample Data
# --------------------
# Randomly sample 100 entries from the CSV.
sample_df = df.sample(n=sample_size, random_state=42).copy()

# Use the 'cleaned_website_text' field as the classifier input.
sample_df["Sample_Text"] = sample_df["cleaned_website_text"]

# --------------------
# Run the Classifier to Get Predictions
# --------------------
with torch.no_grad():
    inputs = tokenizer(
        sample_df["Sample_Text"].tolist(),
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512  # Adjust max_length as needed for your data
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model(**inputs)
    preds = outputs.logits.softmax(dim=-1).argmax(dim=-1).cpu().tolist()

# Convert numeric predictions to topic text using our reverse mapping.
sample_df["Predicted_Label"] = [reverse_mapping.get(p, "Unknown") for p in preds]

# --------------------
# Insert Data into SQLite Database
# --------------------
# Connect (or create) the SQLite DB file called "db.sqlite3".
conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

# Drop the table if it already exists and create a new one to store the data.
cur.execute("DROP TABLE IF EXISTS topics")
cur.execute("""
    CREATE TABLE topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website_url TEXT,
        cleaned_website_text TEXT,
        topic TEXT
    )
""")

# Insert each record (website_url, cleaned_website_text, and predicted topic) into the database.
for index, row in sample_df.iterrows():
    cur.execute(
        "INSERT INTO topics (website_url, cleaned_website_text, topic) VALUES (?, ?, ?)",
        (row['website_url'], row['cleaned_website_text'], row['Predicted_Label'])
    )

conn.commit()
conn.close()

print("Inserted 100 entries with website_url, cleaned_website_text, and predicted topic into the SQLite database 'db.sqlite3' in table 'topics'.")
