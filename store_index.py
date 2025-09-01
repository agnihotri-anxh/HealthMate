from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data=load_pdf_file(data='Data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalchatbot"  # Using existing index name


# Check if index already exists, if not create it
try:
    pc.create_index(
        name=index_name,
        dimension=384, 
        metric="cosine", 
        spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        ) 
    )
    print(f"Created new Pinecone index: {index_name}")
except Exception as e:
    if "ALREADY_EXISTS" in str(e):
        print(f"Index {index_name} already exists, proceeding with document upload...")
    else:
        print(f"Error creating index: {e}")
        raise e

# Embed each chunk and upsert the embeddings into your Pinecone index.
print(f"Uploading {len(text_chunks)} document chunks to Pinecone...")
try:
    docsearch = PineconeVectorStore.from_documents(
        documents=text_chunks,
        index_name=index_name,
        embedding=embeddings, 
    )
    print(f"Successfully uploaded {len(text_chunks)} chunks to Pinecone index '{index_name}'")
    print("Your HealthMate AI Assistant is now ready to use!")
except Exception as e:
    print(f"Error uploading documents: {e}")
    raise e
