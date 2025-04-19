from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

def match_resume_to_jd(resume_text, jd_text):
    # Encode the resume and JD using BERT tokenizer
    inputs = tokenizer(resume_text, jd_text, return_tensors='pt', padding=True, truncation=True, max_length=512)

    # Get the model's output
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the logits (output before activation)
    logits = outputs.logits

    # Convert logits to probabilities using softmax
    probabilities = torch.nn.functional.softmax(logits, dim=-1)

    # Return the probability of matching (classification task, assuming the model is binary classification)
    match_score = probabilities[0][1].item()  # Get the score for the "match" class (index 1)
    
    return match_score
