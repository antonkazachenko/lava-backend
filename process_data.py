import pandas as pd
from transformers import pipeline
import torch

print("Starting local data processing with a new, compatible model...")

# --------------------
# Configuration
# --------------------
sample_size = 100

# --------------------
# Load Data and Define Topics
# --------------------
print("Loading CSV and defining candidate topics...")
try:
    df = pd.read_csv('./website_classification.csv')
except FileNotFoundError:
    print("Error: website_classification.csv not found.")
    exit()

# The candidate labels for our new classifier
candidate_labels = [
    "Adult", "Art & Design", "Software Development", "Crime & Law",
    "Education & Jobs", "Hardware", "Entertainment", "Social Life",
    "Fashion & Beauty", "Finance & Business", "Food & Dining",
    "Games", "Health", "History", "Home & Hobbies",
    "Industrial", "Literature", "Politics", "Religion",
    "Science & Technology", "Software", "Sports & Fitness",
    "Transportation", "Travel",
]

# --------------------
# Load the Classifier Pipeline
# --------------------
print("Loading a CPU-friendly zero-shot classification model (this may take a moment)...")
# This pipeline is designed for this exact task and works reliably on CPUs.
# It does not require 'trust_remote_code=True' or 'xformers'.
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# --------------------
# Prepare and Classify Sample Data
# --------------------
print(f"Preparing and classifying {sample_size} samples...")
sample_df = df.sample(n=sample_size, random_state=42).copy()
# Ensure there are no empty text entries, which can cause issues
sample_df.dropna(subset=['cleaned_website_text'], inplace=True)
texts_to_classify = sample_df["cleaned_website_text"].tolist()

# The pipeline handles tokenization and prediction in one step.
# It returns a list of dictionaries for each text.
print(f"Running classification on {len(texts_to_classify)} valid text entries...")
predictions = classifier(texts_to_classify, candidate_labels)

# Extract the top-scoring label for each prediction.
sample_df["Predicted_Label"] = [pred['labels'][0] for pred in predictions]

# --------------------
# Save Results to CSV
# --------------------
print("Saving results to predicted_topics.csv...")
output_df = sample_df[['website_url', 'cleaned_website_text', 'Predicted_Label']]
output_df.to_csv('predicted_topics.csv', index=False)

print("\nFinished! The file 'predicted_topics.csv' has been created successfully.")