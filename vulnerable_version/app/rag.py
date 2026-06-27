from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = "vectordb"
COLLECTION_NAME = "business_data"

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def get_vectorstore():
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def load_and_chunk_file(file_path: str, chunk_size: int = 200, chunk_overlap: int = 20):
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(docs)


def ingest_file(business_id: str, file_path: str):
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    chunks = load_and_chunk_file(file_path)
    for i, chunk in enumerate(chunks):
        chunk.metadata["business_id"] = business_id
        chunk.metadata["source_file"] = Path(file_path).name
        chunk.metadata["chunk_id"] = f"{business_id}_{Path(file_path).stem}_{i}"

    db = get_vectorstore()
    ids = [chunk.metadata["chunk_id"] for chunk in chunks]
    db.add_documents(chunks, ids=ids)

    return {
        "business_id": business_id,
        "file_path": file_path,
        "chunks_added": len(chunks),
    }


def get_retriever(business_id: str, k: int = 3):
    db = get_vectorstore()
    return db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": {"business_id": business_id},
        },
    )


def retrieve_docs(business_id: str, question: str, k: int = 3):
    retriever = get_retriever(business_id, k=k)
    docs = retriever.invoke(question)
    return docs
