import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

def ingest_pdf():
    for env_var in [PDF_PATH, DATABASE_URL, PG_VECTOR_COLLECTION_NAME]:
        if not env_var:
            raise RuntimeError(f"Environment variable {env_var} is not set.")

    document = PyPDFLoader(PDF_PATH).load()
    
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    ).split_documents(document)

    if not splits:
        raise SystemExit(0)

    enriched = []
    for split in splits:
        metadata = {}
        for k, v in split.metadata.items():
            if v not in ("", None):
                metadata[k] = v
        new_document = Document(
            page_content=split.page_content,
            metadata=metadata
        )
        enriched.append(new_document)

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)
    
if __name__ == "__main__":
    ingest_pdf()