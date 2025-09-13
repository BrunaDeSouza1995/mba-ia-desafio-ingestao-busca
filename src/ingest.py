import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    if not PDF_PATH:
        raise RuntimeError("Environment variable PDF_PATH is not set.")
    
    document = PyPDFLoader(PDF_PATH).load()
    
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    ).split_documents(document)

    if not splits:
        raise SystemExit(0)

    for split in splits:
        print(split.page_content)
        print("*" * 10)
    print(len(splits))

if __name__ == "__main__":
    ingest_pdf()