import os
from search import search_prompt
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

def main():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )
    query = "Qual o faturamento da Empresa SuperTechIABrazil?"
    context = store.similarity_search_with_score(query, k=10)
    chain = search_prompt(context=context, question=query)  

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    model = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    result = model.invoke(chain)
    print(result.content)

if __name__ == "__main__":
    main()