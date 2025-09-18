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

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

if not PINECONE_API_KEY or not GROQ_API_KEY:
    raise ValueError("PINECONE_API_KEY and GROQ_API_KEY must be set in environment variables or .env file")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

embeddings = download_hugging_face_embeddings()

if embeddings is None:
    print("Warning: Could not load embeddings model. The application will run in limited mode.")
    docsearch = None
else:
    index_name = "medicalchatbot"  # Using existing index name
    
    # Embed each chunk and upsert the embeddings into your Pinecone index.
    try:
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
    except Exception as e:
        print(f"Warning: Could not connect to Pinecone index: {e}")
        docsearch = None

if docsearch is not None:
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
else:
    retriever = None


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",  # HealthMate AI Model
    temperature=0.4,
    max_tokens=500
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)

if retriever is not None:
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
else:
    rag_chain = None


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/health")
def health_check():
    from datetime import datetime
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HealthMate AI Assistant"
    })


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    
    if rag_chain is not None:
        response = rag_chain.invoke({"input": msg})
        print("Response : ", response["answer"])
        return str(response["answer"])
    else:
        # Fallback response when RAG chain is not available
        fallback_response = f"I apologize, but I'm currently experiencing technical difficulties with my knowledge base. However, I can still help with general medical questions. You asked: '{msg}'. Please note that for specific medical advice, always consult with a healthcare professional."
        print("Fallback Response : ", fallback_response)
        return fallback_response




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
