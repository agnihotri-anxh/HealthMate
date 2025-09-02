# Personal Medical AI Assistant

A medical chatbot powered by Groq's Llama 3.1 8B model with Pinecone vector database for intelligent medical information retrieval.
<img width="1705" height="898" alt="image" src="https://github.com/user-attachments/assets/661b29dd-9334-438c-8fb5-e300f1b98949" />


## 🚀 Features

- **AI-Powered Medical Assistant** - Uses Groq's Llama 3.1 8B model
- **RAG (Retrieval-Augmented Generation)** - Accesses medical knowledge from PDF documents
- **Vector Database** - Pinecone for efficient document search and retrieval
- **Modern Web Interface** - Clean, responsive chat interface
- **Real-time Responses** - Instant medical information and answers

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI Model**: Groq (Llama 3.1 8B)
- **Vector Database**: Pinecone
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Frontend**: HTML, CSS, JavaScript
- **Document Processing**: LangChain, PyPDF

## 📋 Prerequisites

- Python 3.8+
- Pinecone API key
- Groq API key
- Medical PDF documents

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd End-to-end-Medical-Chatbot-Generative-AI-main
```

### Step 2: Create Virtual Environment
```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Keys

Create a `.env` file in the root directory:
```ini
PINECONE_API_KEY=your_pinecone_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

**Get your API keys:**
- **Pinecone**: [Pinecone Console](https://app.pinecone.io/)
- **Groq**: [Groq Console](https://console.groq.com/)

### Step 5: Prepare Medical Documents

Place your medical PDF files in the `Data/` folder. The system will process these documents and create embeddings.

### Step 6: Upload Documents to Pinecone
```bash
python store_index.py
```

This script will:
- Process your PDF documents
- Split them into text chunks
- Generate embeddings
- Upload to Pinecone vector database

### Step 7: Run the Application
```bash
python app.py
```

The chatbot will be available at: `http://localhost:8080`

## 📁 Project Structure

```
├── app.py                 # Main Flask application
├── store_index.py         # Document processing and Pinecone upload
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── Data/                 # Place your medical PDFs here
├── src/
│   ├── helper.py         # Document processing functions
│   └── prompt.py         # AI system prompts
├── templates/
│   └── chat.html         # Chat interface
└── static/
    └── style.css         # Styling
```

## 🔧 How It Works

1. **Document Processing**: PDFs are loaded and split into chunks
2. **Embedding Generation**: Text chunks are converted to 384-dimensional vectors
3. **Vector Storage**: Embeddings are stored in Pinecone database
4. **Query Processing**: User questions are converted to embeddings
5. **Similarity Search**: Pinecone finds most relevant document chunks
6. **AI Response**: Groq model generates answers using retrieved context

## 🎯 Usage

1. Open the web interface
2. Type your medical question
3. The AI will search through your medical documents
4. Get accurate, context-aware responses

## ⚠️ Important Notes

- **Not Medical Advice**: This is for educational purposes only
- **Document Quality**: Better documents = better responses
- **API Limits**: Be aware of Groq and Pinecone usage limits
- **Data Privacy**: Your documents are processed and stored in Pinecone

## 🐛 Troubleshooting

### Common Issues

**"Invalid API Key" Error**
- Verify your API keys are correct
- Check that `.env` file exists and is properly formatted
- Ensure no extra spaces in API keys

**"Index Already Exists" Error**
- This is normal if you've run the script before
- The script will handle existing indexes automatically

**No Documents Found**
- Ensure PDF files are in the `Data/` folder
- Check file permissions and format

**Import Errors**
- Make sure you're in the correct conda environment
- Run `pip install -r requirements.txt` again

### Environment Variables Not Loading
If using Jupyter notebooks, add this at the beginning:
```python
import os
from dotenv import load_dotenv
load_dotenv()
```

## 🔄 Updating Documents

To add new medical documents:
1. Place new PDFs in `Data/` folder
2. Run `python store_index.py` again
3. New documents will be added to existing index

## 📊 Monitoring

- **Pinecone Dashboard**: Check document count and usage
- **Console Logs**: Monitor processing and upload progress
- **API Usage**: Track Groq and Pinecone API consumption

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your API keys and environment setup
3. Check Pinecone and Groq service status
4. Review console logs for error messages

## 🎉 Success Indicators

Your setup is working when:
- ✅ `python store_index.py` runs without errors
- ✅ Pinecone dashboard shows document records > 0
- ✅ `python app.py` starts successfully
- ✅ Web interface loads at localhost:8080
- ✅ Chatbot responds to medical questions
