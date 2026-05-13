# app.py
<<<<<<< HEAD
# Retrieval-Augmented Document Assistant with PyTorch Document Classification
=======
# Retrieval-Augmented Document Assistant
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a
# Run with: streamlit run app.py

import os
import tempfile
<<<<<<< HEAD
from typing import List
=======
from typing import List, Tuple
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a

import chromadb
import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

<<<<<<< HEAD
from classifier import train_classifier, predict_document_type


st.set_page_config(page_title="RAG Document Assistant", page_icon="📄", layout="wide")

st.title("📄 RAG Document Assistant")
st.write("Upload a PDF, classify its document type, and ask questions grounded in its content.")


# -----------------------------
# Load models
# -----------------------------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_document_classifier():
    # Trains from data/training_data.json if no saved model exists yet.
    return train_classifier()


embedding_model = load_embedding_model()
classifier_bundle = load_document_classifier()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
=======

# -----------------------------
# App setup
# -----------------------------
st.set_page_config(page_title="RAG Document Assistant", page_icon="📄", layout="wide")
st.title("📄 RAG Document Assistant")
st.write("Upload a PDF, ask questions, and get answers grounded in your document.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a


# -----------------------------
# Helper functions
# -----------------------------
def extract_pdf_text(uploaded_file) -> str:
    """Extract text from an uploaded PDF file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    reader = PdfReader(temp_path)
    text_parts = []

    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        if page_text.strip():
            text_parts.append(f"\n[Page {page_num}]\n{page_text}")

    os.remove(temp_path)
    return "\n".join(text_parts)


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
<<<<<<< HEAD

        if chunk:
            chunks.append(chunk)

=======
        if chunk:
            chunks.append(chunk)
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a
        start += chunk_size - overlap

    return chunks


def create_vector_store(chunks: List[str]):
    """Create an in-memory ChromaDB collection from text chunks."""
    chroma_client = chromadb.Client()

<<<<<<< HEAD
=======
    # Delete old collection if it exists during reruns
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a
    try:
        chroma_client.delete_collection("documents")
    except Exception:
        pass

    collection = chroma_client.create_collection(name="documents")
    embeddings = embedding_model.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

    return collection


def retrieve_context(collection, question: str, top_k: int = 4) -> List[str]:
    """Retrieve the most relevant chunks for a question."""
    question_embedding = embedding_model.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )

    return results["documents"][0]


def generate_answer(question: str, context_chunks: List[str]) -> str:
<<<<<<< HEAD
    """Generate an answer using retrieved context."""
    context = "\n\n---\n\n".join(context_chunks)

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "You are a helpful document assistant. Answer using only the provided context. "
            "If the answer is not in the context, say the document does not provide enough information. "
=======
    """Generate an answer using the retrieved context."""
    context = "\n\n---\n\n".join(context_chunks)

    response = client.responses.create(
        model="gpt-5.2",
        instructions=(
            "You are a helpful document assistant. Answer using only the provided context. "
            "If the answer is not in the context, say that the document does not provide enough information. "
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a
            "Be clear and concise."
        ),
        input=f"Context:\n{context}\n\nQuestion: {question}",
    )

    return response.output_text


# -----------------------------
<<<<<<< HEAD
# Session state
=======
# Streamlit UI
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a
# -----------------------------
if "collection" not in st.session_state:
    st.session_state.collection = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

<<<<<<< HEAD
if "document_text" not in st.session_state:
    st.session_state.document_text = ""


# -----------------------------
# Streamlit UI
# -----------------------------
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading, classifying, and indexing document..."):
        text = extract_pdf_text(uploaded_file)

        if not text.strip():
            st.error("Could not extract text from this PDF. Try another PDF with selectable text.")
            st.stop()

        predicted_type = predict_document_type(text, classifier_bundle)
=======
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading and indexing document..."):
        text = extract_pdf_text(uploaded_file)
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a
        chunks = chunk_text(text)
        collection = create_vector_store(chunks)

        st.session_state.collection = collection
        st.session_state.chunks = chunks
<<<<<<< HEAD
        st.session_state.document_text = text

    st.success(f"Indexed {len(chunks)} chunks from {uploaded_file.name}")
    st.info(f"Predicted document type: **{predicted_type}**")
=======

    st.success(f"Indexed {len(chunks)} chunks from {uploaded_file.name}")
>>>>>>> 568ab55a1f0b21c55ce232ecbcf01409cc68248a

question = st.text_input("Ask a question about your document")

if st.button("Ask"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Missing OPENAI_API_KEY. Add it to your environment variables first.")
    elif st.session_state.collection is None:
        st.warning("Upload a PDF first.")
    elif not question.strip():
        st.warning("Type a question first.")
    else:
        with st.spinner("Retrieving relevant context and generating answer..."):
            context_chunks = retrieve_context(st.session_state.collection, question)
            answer = generate_answer(question, context_chunks)

        st.subheader("Answer")
        st.write(answer)

        with st.expander("Retrieved source chunks"):
            for i, chunk in enumerate(context_chunks, start=1):
                st.markdown(f"**Chunk {i}**")
                st.write(chunk[:1200] + ("..." if len(chunk) > 1200 else ""))
