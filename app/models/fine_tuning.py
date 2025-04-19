import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import Trainer, TrainingArguments, BertForSequenceClassification, BertTokenizer
from app.models.resume_job_dataset import ResumeJobDataset

# Load dataset (assuming a CSV with columns 'resume', 'job_description', 'label')
data = pd.read_csv('data/raw_data/resumes_jobs.csv')

# Split dataset into features (resumes, job_descriptions) and labels
resumes = data['resume'].tolist()
job_descriptions = data['job_description'].tolist()
labels = data['label'].tolist()

# Split the dataset into training and evaluation sets (80% training, 20% evaluation)
train_resumes, eval_resumes, train_jobs, eval_jobs, train_labels, eval_labels = train_test_split(
    resumes, job_descriptions, labels, test_size=0.2, random_state=42
)

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Create training and evaluation datasets
train_dataset = ResumeJobDataset(train_resumes, train_jobs, train_labels, tokenizer, max_len=512)
eval_dataset = ResumeJobDataset(eval_resumes, eval_jobs, eval_labels, tokenizer, max_len=512)

# Load the pre-trained model for sequence classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

# Fine-tune the model
trainer.train()

# Evaluate the model
eval_results = trainer.evaluate()
print("Evaluation Results:", eval_results)

# Save the trained model and tokenizer
model.save_pretrained("./finetuned_bert")
tokenizer.save_pretrained("./finetuned_bert")

# Optionally, save evaluation results to a file
with open('eval_results.txt', 'w') as f:
    f.write(str(eval_results))
