# AI-Powered Resume Screening System

This is a web application that uses AI to screen resumes and match them to a job description (JD). It takes a resume (in PDF format) and a job description, and uses **Natural Language Processing (NLP)** to calculate a match score based on the relevance of the resume to the job description.

## Features
- Upload resumes (PDF format)
- Paste job description (JD)
- AI-based matching and score calculation

## Technologies Used
- **Flask**: Python web framework
- **scikit-learn**: Machine learning library for vectorization and cosine similarity
- **PyMuPDF**: PDF text extraction library
- **HTML/CSS**: Frontend for file upload and input

## Installation & Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/resume-screener.git
    cd resume-screener
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:
    ```bash
    python main.py
    ```

5. Open your browser and navigate to `http://127.0.0.1:5000/` to start using the resume screener.

## Usage
- Upload a PDF resume file.
- Paste a job description into the text box.
- Click the "Match Resume" button to see the match score between the resume and the job description.
