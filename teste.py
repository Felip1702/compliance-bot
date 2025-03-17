from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

# Texto de exemplo
texts = ["Este é um exemplo de texto.", "Outro exemplo de texto."]

# Gerar embeddings
embeddings = OpenAIEmbeddings(openai_api_key="sua_chave_api_openai")
vectorstore = FAISS.from_texts(texts, embedding=embeddings)

# Salvar embeddings
save_path = "./test_faiss_index"
os.makedirs(save_path, exist_ok=True)
vectorstore.save_local(save_path)

# Verificar se os arquivos foram criados
if os.path.exists(os.path.join(save_path, "index.faiss")) and os.path.exists(os.path.join(save_path, "index.pkl")):
    print("Arquivos index.faiss e index.pkl foram criados com sucesso.")
else:
    print("Erro: Arquivos index.faiss e index.pkl NÃO foram criados.")