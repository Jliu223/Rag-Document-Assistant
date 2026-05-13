# RAG Document Assistant

<<<<<<< HEAD
A Retrieval-Augmented Generation (RAG) application that lets users upload PDFs, classify the document type, and ask natural language questions about the document.

## Features

- Upload and parse PDF files
- Classify uploaded documents with a PyTorch text classifier
- Chunk document text for retrieval
- Generate vector embeddings with SentenceTransformers
- Store and search document chunks with ChromaDB
- Generate grounded answers using the OpenAI API
- View retrieved source chunks used for each answer
=======
A Retrieval-Augmented Generation (RAG) application that allows users to upload PDFs and ask natural language questions about their documents.

## Features

- PDF upload and parsing
- Semantic text chunking
- Vector embeddings using SentenceTransformers
- ChromaDB vector search
- OpenAI-powered question answering
- Streamlit frontend
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a

## Tech Stack

- Python
- Streamlit
<<<<<<< HEAD
- PyTorch
- scikit-learn
- OpenAI API
- ChromaDB
- SentenceTransformers
- pypdf

## Project Structure

```text
rag-document-assistant/
├── app.py
├── classifier.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── training_data.json
└── models/
    └── document_classifier.pth
```

## Run Locally

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
$env:OPENAI_API_KEY="your_api_key_here"
```

Run the app:

```bash
streamlit run app.py
```

## How It Works

1. The user uploads a PDF.
2. The app extracts text from the PDF.
3. A PyTorch classifier predicts the document type.
4. The text is split into chunks.
5. SentenceTransformer embeddings are generated for each chunk.
6. ChromaDB retrieves the most relevant chunks for a user question.
7. The OpenAI API generates an answer using the retrieved context.

## Future Improvements

- Add multi-PDF support
- Add page-level citations
- Save persistent vector databases
- Add chat history
- Improve classifier training data
- Deploy the app online
=======
- OpenAI API
- ChromaDB
- SentenceTransformers

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Future Improvements

- Multi-document support
- Persistent vector database
- Page citations
- Chat history memory
- Improved UI/UX
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a
