# from flask import Flask, render_template, request, jsonify
# from groq import Groq
# from PyPDF2 import PdfReader

# app = Flask(__name__)

# # Groq API Key
# groq_client = Groq(api_key="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")  # Replace with your actual key

# # PDF Path
# pdf_path = r"C:\PythonProjects\chat with me\doc\cloud_security_policy.pdf"   # PDF placed in 'doc' folder

# # Extract PDF text
# def extract_pdf_text(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = ''
#     for page in reader.pages:
#         content = page.extract_text()
#         if content:
#             text += content
#     return text

# pdf_content = extract_pdf_text(pdf_path)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json['message']
    
#     prompt = f"""
# You are an AI assistant named 'Chat With Me'.
# Answer the user's question **strictly only** using the following PDF content.
# If the answer is not found in this content, respond with: "Sorry, not in PDF."

# PDF Content:
# {pdf_content}

# User Question: {user_input}
# """

#     response = groq_client.chat.completions.create(
#         messages=[{"role": "user", "content": prompt}],
#         model="meta-llama/llama-4-scout-17b-16e-instruct"  # Or your Groq model name
#     )

#     return jsonify({'reply': response.choices[0].message.content})

# if __name__ == '__main__':
#     app.run(debug=True)












#  for descriptive answer :- 









from flask import Flask, render_template, request, jsonify
from groq import Groq
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

# Groq API client
groq_client = Groq(api_key=os.getenv("API_KEY"))  # Replace with your Groq key

# PDF path and text extraction
pdf_path = "C:\PythonProjects\chat with me\doc\cloud_security_policy.pdf"  # Your actual PDF file
def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

pdf_content = extract_pdf_text(pdf_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    # Improved prompt for detailed answers
    prompt = f"""
You are 'Chat With Me', an expert AI chatbot assistant.

Your task is to answer ONLY from the PDF content given below.
**Always provide very detailed, descriptive, and well-explained answers.** 
Explain concepts clearly, give examples if possible, and elaborate wherever needed.

If the answer cannot be found in the PDF, reply politely: "Sorry, this information is not available in the provided PDF."

PDF Content:
{pdf_content}

User's Question: {user_input}
"""

    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95
    )

    reply = response.choices[0].message.content
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
