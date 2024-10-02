from flask import Flask, render_template, request, redirect, url_for, jsonify
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json

app = Flask(__name__)

# Global state (You can use a better persistence solution, like a database)
history = []
generated = ["Hello! Ask me anything about 🤗"]
past = ["Hey! 👋"]

def get_pdf_text(pdf_files):
    text = ""
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    consider context as syllabus and generate questions and subtopic based on inputs, provide it in python dictionary form , if pdf not provided just say"PDF unavailable", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    inputs: 
    {question}
    
    output should be python dictionary containing question no, question, mark, subtopic for each section
    

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input_chain(user_question, history):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(user_question)

    chain = get_conversational_chain()
    user_question=f"""
        Section no: 1;
        Question Type: Answer the following;
        Number of Questions: 6;
        Marks per Question: 2;
        Section no: 2;
        Question Type: Answer the following;
        Number of Questions: 4;
        Marks per Question: 5;
        """
    response = chain.invoke(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    history.append((user_question, response["output_text"]))
    return response["output_text"]

@app.route('/')
def index():
    return render_template('index2.html', generated=generated, past=past, zip=zip)


@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("pdfs")
        if uploaded_files:
            raw_text = get_pdf_text(uploaded_files)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            return jsonify({'status': 'Processed successfully'}), 200
    return redirect(url_for('index'))

@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.form.get('question')
    if user_question:
        response = user_input_chain(user_question, history)
        past.append(user_question)
        generated.append(response)
    try:
        result_dict = json.loads(response)  # Parse the JSON string into a dictionary
    except json.JSONDecodeError:
        result_dict = {}

    return render_template('result.html', result=result_dict)  # Pass the parsed result to the template

@app.route('/clear', methods=['POST'])
def clear_history():
    global history, generated, past
    history.clear()
    generated = ["Hello! Ask me anything about 🤗"]
    past = ["Hey! 👋"]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
