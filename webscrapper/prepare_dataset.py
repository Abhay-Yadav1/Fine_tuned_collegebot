import csv
import json
import random

INPUT_FILE = './data/raw/output_cleaned.csv'
TRAIN_FILE = './data/processed/train.jsonl'
VAL_FILE   = './data/processed/val.jsonl'

# This is the system prompt your fine-tuned model will always receive
# It tells the model what role it plays — keep it short and specific
SYSTEM_PROMPT = "You are a helpful assistant that answers questions about the RTI Online Portal of the Government of India."

def format_as_chat(question, answer):
    # Mistral-7B-Instruct expects the "messages" format —
    # a list of role/content dicts: system → user → assistant
    # This is what SFTTrainer will use during training
    return {
        "messages": [
            {"role": "system",  "content": SYSTEM_PROMPT},
            {"role": "user",    "content": question},
            {"role": "assistant", "content": answer}
        ]
    }

# Step 1 — Read cleaned CSV into a list of formatted chat objects
all_pairs = []

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)  # columns are now "question" and "answer" (from cleaner.py)
    for row in reader:
        chat_obj = format_as_chat(row['question'], row['answer'])
        all_pairs.append(chat_obj)

print(f"Total pairs loaded: {len(all_pairs)}")

# Step 2 — Shuffle so train/val split is random, not ordered by topic
# Set a seed so your split is reproducible — same result every time you run it
random.seed(42)
random.shuffle(all_pairs)

# Step 3 — Split: 85% train, 15% val
# With 27 pairs: 23 train, 4 val
split_index = int(len(all_pairs) * 0.85)
train_data = all_pairs[:split_index]
val_data   = all_pairs[split_index:]

print(f"Train size: {len(train_data)}, Val size: {len(val_data)}")

# Step 4 — Write each split to its own JSONL file
# JSONL = one JSON object per line (not a JSON array)
# This is the format HuggingFace datasets.load_dataset() expects by default

def write_jsonl(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for obj in data:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
            # ensure_ascii=False keeps Hindi/special chars readable if any exist

write_jsonl(train_data, TRAIN_FILE)
write_jsonl(val_data,   VAL_FILE)

print(f"Saved train → {TRAIN_FILE}")
print(f"Saved val   → {VAL_FILE}")

# Step 5 — Sanity check: print one training example in full
# Read it back from file so you verify the file itself is correct, not just the variable
print("\n--- Sample training example (read back from file) ---")
with open(TRAIN_FILE, 'r', encoding='utf-8') as f:
    first_line = f.readline()
    print(json.dumps(json.loads(first_line), indent=2, ensure_ascii=False))