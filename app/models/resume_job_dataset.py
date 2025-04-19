from torch.utils.data import Dataset
from transformers import BertTokenizer
import torch
class ResumeJobDataset(Dataset):
    def __init__(self, resumes, job_descriptions, labels, tokenizer, max_len):
        self.resumes = resumes
        self.job_descriptions = job_descriptions
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.resumes)

    def __getitem__(self, item):
        resume = self.resumes[item]
        job_description = self.job_descriptions[item]
        label = self.labels[item]

        encoding = self.tokenizer(
            resume, job_description,
            truncation=True,
            padding='max_length',
            max_length=self.max_len,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }
