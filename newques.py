from flask import Flask, render_template, request, redirect, url_for, jsonify
from PyPDF2 import PdfReader
import json
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)

# Global state (You can use a better persistence solution, like a database)
pyq_responses = {}

def get_pdf_text(pdf_files):
    """Extract text from PDF files."""
    text = ""
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_pyqs(text):
    """Extract PYQs from text."""
    pyqs = re.split(r'(\d+)\. ', text)
    return pyqs

def process_pyqs(pyqs):
    """Process PYQs and extract subtopic and marks."""
    processed_pyqs = []
    for i in range(1, len(pyqs), 2):
        question = pyqs[i] + pyqs[i+1]
        # Generate responses using the QA chain
        chain = get_conversational_chain()
        response = chain.invoke(
            {
                "input_documents": [],  
                "question": "Extract subtopic and marks",  
                "context": question  
            },
            return_only_outputs=True
        )
        try:
            output_dict = json.loads(response["output_text"])
        except json.JSONDecodeError:
            print("Invalid JSON response:")
            print(response["output_text"])
            # Handle the error or skip this response
            continue
        processed_pyqs.append({
            "question": question,
            "subtopic": output_dict["subtopic"],
            "marks": output_dict["marks"]
        })
    return processed_pyqs

def get_conversational_chain():
    """Create a conversational QA chain."""
    prompt_template = """
    Consider context as PYQ and extract subtopic and marks.
    
    Context:
    {context}
    
    Inputs: 
    {question}
    
    Output should be a JSON dictionary with keys 'subtopic' and 'marks'.
    
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

@app.route('/')
def index():
    return render_template('newques.html', pyq_responses=pyq_responses)

@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("pdfs")
        if uploaded_files:
            text = get_pdf_text(uploaded_files)
            pyqs = extract_pyqs(text)
            processed_pyqs = process_pyqs(pyqs)
            pyq_responses["pyqs"] = processed_pyqs
            print(pyq_responses)  
            return jsonify({'status': 'Processed successfully'}), 200
    return redirect(url_for('index'))

@app.route('/clear', methods=['GET', 'POST'])
def clear_history():
    global pyq_responses
    pyq_responses = {}
    return redirect(url_for('index'))

@app.route('/get_pyq_responses', methods=['GET'])
def get_pyq_responses():
    return jsonify(pyq_responses)

if __name__ == '__main__':
    app.run(debug=True)