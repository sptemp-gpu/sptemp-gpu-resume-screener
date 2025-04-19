from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the model and tokenizer
model_path = "app/models/bert_resume_matcher"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

def predict_match(resume_text, job_desc):
    inputs = tokenizer(resume_text, job_desc, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class  # 0 or 1 (0 = No Match, 1 = Match)
