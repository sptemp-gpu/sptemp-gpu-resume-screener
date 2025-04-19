from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from app.models.bert_model import predict_match  # Import the prediction function
import fitz  # PyMuPDF for PDF text extraction
from docx import Document

app = Flask(__name__)

# Set up a directory for uploaded files (make sure the folder exists)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for the resume upload
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from a PDF file using PyMuPDF
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ''
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # load each page
        text += page.get_text()  # extract text from page
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text

# Route for the home page, render the form for users to upload their resume and job description
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Route for handling file uploads and processing the resume and job description
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'resume' not in request.files:
        return "No file part", 400
    
    file = request.files['resume']
    job_description = request.form['jd']
    
    # If the user does not select a file, browser also submits an empty part without a filename
    if file.filename == '':
        return "No selected file", 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and save it to the upload folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from the uploaded resume
        if filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:  # For .txt files, just read the text
            with open(file_path, 'r') as f:
                resume_text = f.read()
        
        # Use the predict_match function to get the result
        result = predict_match(resume_text, job_description)
        
        # Determine the message based on prediction result
        message = "✅ Match Found!" if result == 1 else "❌ Not a Match"
        
        # Return the result to the user
        return render_template("result.html", message=message)

    return "Invalid file type. Please upload a PDF, DOCX, or TXT file.", 400

if __name__ == "__main__":
    app.run(debug=True)
