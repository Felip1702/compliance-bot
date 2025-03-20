import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import hashlib
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a chave da API da OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("A chave da API da OpenAI não foi configurada no arquivo .env.")

# Caminho fixo para a pasta de embeddings
EMBEDDINGS_DIR = os.path.abspath("./embeddings_store")

# Create region folders
REGIONS = ["South America", "Europe", "Asia", "North America"]
for region in REGIONS:
    region_path = os.path.join(EMBEDDINGS_DIR, region)
    os.makedirs(region_path, exist_ok=True) # Ensure region folder exists.

def process_pdf(pdf, chat_id, region):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Processing PDF: {pdf.name} for chat ID: {chat_id} in Region: {region}")

    # Extrair texto do PDF
    try:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return None, None, None

    # Dividir o texto em chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text=text)

    # Gerar nome único para o armazenamento
    pdf_id = hashlib.md5(f"{pdf.name}_{chat_id}".encode()).hexdigest()

    # Determine the save path based on the region
    region_path = os.path.join(EMBEDDINGS_DIR, region)  # Get the correct region folder
    save_path = os.path.join(region_path, f"{pdf_id}_faiss_index")

    # Gerar embeddings
    vectorstore = None
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
        vectorstore.save_local(save_path)
        logging.info(f"Embeddings saved successfully for PDF ID: {pdf_id} to: {save_path}")
    except Exception as e:
        logging.error(f"Error generating or saving embeddings for PDF ID: {pdf_id}: {e}")
        # Handle embedding failure. Return None for vectorstore, and consider other error handling.
        return pdf_id, chunks, None

    return pdf_id, chunks, vectorstore