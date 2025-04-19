from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the fine-tuned model and tokenizer
model_path = './finetuned_bert'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)
model.eval()  # Set model to evaluation mode for inference

def predict_match(resume, job_description):
    """
    Predicts whether a resume matches a job description using the fine-tuned BERT model.
    Returns:
        1 for match, 0 for no match.
    """
    # Tokenize the inputs
    inputs = tokenizer(
        resume,
        job_description,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    # Disable gradient calculation for inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get logits and convert to probabilities
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    prediction = torch.argmax(probabilities, dim=-1).item()

    return prediction
