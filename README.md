# Fine-Tuned RTI Assistant 🤖

A domain-specific chatbot fine-tuned on RTI (Right to Information) Online Portal FAQ data using QLoRA on Mistral-7B-Instruct. Built as a hands-on learning project to understand the end-to-end LLM fine-tuning pipeline.

---

## What This Project Does

Takes a general-purpose LLM (Mistral-7B-Instruct) that gives vague, hallucinated answers about RTI processes, and fine-tunes it using QLoRA so it answers questions accurately based on the actual RTI Online Portal FAQ content.

**Before fine-tuning** — asked "How do I make the payment for RTI fee?", the base model invents a generic 7-step process that doesn't match the actual portal.

**After fine-tuning** — the model correctly references the actual payment modes (SBI gateway, ATM-cum-Debit card, Master/Visa, UPI) from the real FAQ data.

---

## Pipeline Overview

```
RTI Online Portal (rtionline.gov.in)
        ↓
  webscrapper/scrapper.py       ← scrape 27 Q&A pairs with requests + BeautifulSoup
        ↓
  webscrapper/cleaner.py        ← fix spacing artifacts, br tag residue, whitespace
        ↓
  webscrapper/prepare_dataset.py ← convert to Mistral chat format JSONL, train/val split
        ↓
  notebooks/training.ipynb      ← QLoRA fine-tuning on Google Colab T4 GPU
        ↓
  output/lora_adapter/          ← trained LoRA adapter weights (~100MB)
        ↓
  output/finetuned_results.json ← post-training evaluation results
```

---

## Project Structure

```
Fine_tuned_collegebot/
├── data/
│   ├── raw/
│   │   ├── output.csv              # raw scraped Q&A pairs
│   │   └── output_cleaned.csv      # cleaned version
│   └── processed/
│       ├── train.jsonl             # 23 training examples
│       └── val.jsonl               # 4 validation examples
├── webscrapper/
│   ├── scrapper.py                 # scrapes RTI FAQ page
│   ├── cleaner.py                  # cleans raw CSV
│   └── prepare_dataset.py          # converts to JSONL chat format
├── notebooks/
│   └── training.ipynb              # full Colab training notebook
├── output/
│   ├── lora_adapter/               # saved LoRA adapter weights
│   ├── baseline_results.json       # base model answers before training
│   ├── finetuned_results.json      # fine-tuned model answers after training
│   └── checkpoints/                # per-epoch training checkpoints
├── .gitignore
└── README.md
```

---

## Tech Stack

| Component | Tool |
|---|---|
| Base Model | Mistral-7B-Instruct-v0.2 |
| Fine-tuning Method | QLoRA (4-bit quantization + LoRA) |
| Quantization | bitsandbytes (NF4, double quant) |
| LoRA Implementation | PEFT |
| Training Loop | TRL / SFTTrainer |
| Data Loading | HuggingFace Datasets |
| Scraping | requests + BeautifulSoup4 |
| Compute | Google Colab T4 GPU (15GB VRAM) |

---

## Training Details

| Parameter | Value |
|---|---|
| LoRA Rank (r) | 8 |
| LoRA Alpha | 16 |
| Target Modules | q_proj, k_proj, v_proj, o_proj |
| Dropout | 0.05 |
| Epochs | 5 |
| Batch Size | 1 (effective 4 with grad accumulation) |
| Learning Rate | 2e-4 |
| Max Sequence Length | 512 |
| Trainable Parameters | ~0.05% of total |

**Loss curve:**

| Epoch | Train Loss | Val Loss | Token Accuracy |
|---|---|---|---|
| 1 | 4.106 | 2.711 | 50.9% |
| 2 | 2.445 | 1.593 | 65.0% |
| 3 | 1.655 | 1.485 | 67.6% |
| 4 | 1.371 | 1.466 | 66.9% |
| 5 | 1.087 | 1.479 | 66.9% |

Mild overfitting visible after epoch 3 — expected with 23 training examples. Validation loss stabilized rather than diverging, indicating the adapter learned domain knowledge without catastrophic forgetting.

---

## Dataset

- **Source:** RTI Online Portal FAQ page — https://rtionline.gov.in/faq.php
- **Size:** 27 Q&A pairs (23 train / 4 validation)
- **Format:** Mistral chat format (system / user / assistant roles)
- **Topics covered:** Portal usage, fee payment, public authority selection, receipts, login, appeal process, OTP, payment failures

---

## Key Learnings

- QLoRA makes fine-tuning a 7B model feasible on a free T4 GPU by reducing memory from ~28GB to ~6GB
- LoRA adapters are tiny (~100MB) compared to full model weights (~14GB) — only the adapter needs to be saved and shared
- With very small datasets (< 50 examples), overfitting is expected — validation loss stabilizes around epoch 3
- JavaScript-rendered sites (like Passport Seva) cannot be scraped with requests + BeautifulSoup alone — always check View Page Source before choosing a scraping target
- The most time-consuming part of any fine-tuning project is data collection and cleaning, not the training itself

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/Abhay-Yadav1/Fine_tuned_collegebot.git
cd Fine_tuned_collegebot
```

**2. Set up environment**
```bash
python -m venv myenv
myenv\Scripts\activate   # Windows
pip install requests beautifulsoup4
```

**3. Re-scrape and rebuild dataset (optional)**
```bash
cd webscrapper
python scrapper.py
python cleaner.py
python prepare_dataset.py
```

**4. Run training**
Open `notebooks/training.ipynb` in Google Colab with a T4 GPU runtime and run all cells in order.

---

## Author

**Abhay Yadav** — Final Year B.Tech Student  
Built from scratch as a hands-on introduction to LLM fine-tuning with LoRA/QLoRA.