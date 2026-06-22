import csv
import re

# Read from raw folder, write to raw folder as cleaned version
INPUT_FILE = './data/raw/output.csv'
OUTPUT_FILE = './data/raw/output_cleaned.csv'

def clean_text(text):
    # Fix words running together after <br/> removal e.g. "only.In case" → "only. In case"
    text = re.sub(r'\.([A-Z])', r'. \1', text)

    # Fix multiple spaces into single space e.g. "RTI  request" → "RTI request"
    text = re.sub(r' +', ' ', text)

    # Remove leftover \r characters (Windows line ending artifacts)
    text = text.replace('\r', '')

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

cleaned_pairs = []

# Open and read the raw CSV
with open(INPUT_FILE, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)  # DictReader uses first row ("Key","Value") as column names automatically

    for row in reader:
        question = clean_text(row['Key'])
        answer = clean_text(row['Value'])

        # Skip any row where question or answer ended up empty after cleaning
        if question and answer:
            cleaned_pairs.append({'question': question, 'answer': answer})

# Write cleaned data to new CSV
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['question', 'answer'])
    writer.writeheader()
    writer.writerows(cleaned_pairs)

print(f"Done. {len(cleaned_pairs)} clean pairs saved to {OUTPUT_FILE}")

# Quick sanity check — print first 2 cleaned answers so you can visually verify
for pair in cleaned_pairs[:2]:
    print("\nQ:", pair['question'])
    print("A:", pair['answer'])