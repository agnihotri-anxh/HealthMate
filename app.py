from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
import gc

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

if not PINECONE_API_KEY or not GROQ_API_KEY:
    raise ValueError("PINECONE_API_KEY and GROQ_API_KEY must be set in environment variables or .env file")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize components lazily to save memory
embeddings = None
docsearch = None
retriever = None
llm = None
rag_chain = None
index_name = "medicalchatbot"

def initialize_components():
    global embeddings, docsearch, retriever, llm, rag_chain
    if embeddings is None:
        print("Loading embeddings model...")
        embeddings = download_hugging_face_embeddings()
        gc.collect()
    
    if docsearch is None:
        print("Initializing Pinecone connection...")
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":2})  # Reduced from 3 to 2
        gc.collect()
        
    if llm is None:
        print("Initializing Groq LLM...")
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama3-8b-8192",
            temperature=0.4,
            max_tokens=300  # Reduced from 500 to 300
        )
        gc.collect()
        
    if rag_chain is None:
        print("Creating RAG chain...")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        print("Components initialized successfully!")
        gc.collect()


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/health")
def health_check():
    from datetime import datetime
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Medical AI Assistant"
    })


@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        print(f"Received message: {msg}")
        
        # Initialize components on first request
        initialize_components()
        
        # Clear memory before processing
        gc.collect()
        
        response = rag_chain.invoke({"input": msg})
        answer = response["answer"]
        
        # Clear memory after processing
        gc.collect()
        
        print(f"Response: {answer}")
        return str(answer)
    except Exception as e:
        print(f"Error in chat: {e}")
        return "Sorry, I encountered an error. Please try again.", 500




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
