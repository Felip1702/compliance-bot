import sqlite3
import logging
import uuid
import json
import os
from typing import Optional, Dict, List
from utils import check_password

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Caminho para o banco de dados
DATABASE_PATH = "compliance_bot.db"

# Verificar se o banco de dados existe
if not os.path.exists(DATABASE_PATH):
    raise FileNotFoundError(f"Banco de dados não encontrado em {DATABASE_PATH}.")

# Função para conectar ao banco de dados
def get_db_connection():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

def create_documents_table():
    """
    Cria a tabela 'documents' no banco de dados, se ela não existir.
    """
    conn = None  # Initialize conn to None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                pdf_name TEXT NOT NULL,
                pdf_size INTEGER NOT NULL,
                upload_date TEXT NOT NULL,
                region TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        conn.commit()
        logging.info("Tabela 'documents' criada ou já existente.")
    except Exception as e:
        logging.error(f"Erro ao criar tabela 'documents': {e}")
        raise e
    finally:
        if conn:
            conn.close()

def save_document(document_id: str, user_id: str, pdf_name: str, pdf_size: int, region: str, category: str) -> None:
    """
    Salva os metadados de um documento no banco de dados.

    Args:
        document_id (str): ID único do documento.
        user_id (str): ID do usuário que carregou o documento.
        pdf_name (str): Nome do arquivo PDF.
        pdf_size (int): Tamanho do arquivo em bytes.
        region (str): Região do documento.
        category (str): Categoria do documento (Políticas ou Procedimentos).
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO documents (document_id, user_id, pdf_name, pdf_size, upload_date, region, category)
            VALUES (?, ?, ?, ?, datetime('now'), ?, ?)
        ''', (document_id, user_id, pdf_name, pdf_size, region, category))
        conn.commit()
        logging.info(f"Documento {pdf_name} salvo com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar documento: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def get_user_documents(user_id: str) -> List[Dict]:
    """
    Retorna todos os documentos carregados por um usuário.

    Args:
        user_id (str): ID do usuário.

    Returns:
        List[Dict]: Lista de documentos com metadados.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM documents WHERE user_id = ?', (user_id,))
        documents = cursor.fetchall()
        return [dict(document) for document in documents]
    except Exception as e:
        logging.error(f"Erro ao carregar documentos: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def delete_document(document_id: str) -> None:
    """
    Exclui um documento do banco de dados.

    Args:
        document_id (str): ID do documento a ser excluído.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM documents WHERE document_id = ?', (document_id,))
        conn.commit()
        logging.info(f"Documento {document_id} excluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao excluir documento: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def save_user(user_id: str, name: str, email: str, password_hash: str) -> None:
    """
    Salva um novo usuário no banco de dados.

    Args:
        user_id (str): ID único do usuário.
        name (str): Nome do usuário.
        email (str): E-mail do usuário.
        password_hash (str): Hash da senha do usuário.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (user_id, name, email, password_hash)
            VALUES (?, ?, ?, ?)
        ''', (user_id, name, email, password_hash))
        conn.commit()
        
        logging.info(f"Usuário {email} salvo com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar usuário: {e}")
        raise e
    finally:
        if conn:
            conn.close()

# Função para autenticar um usuário
def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """
    Autentica um usuário com base no e-mail e senha fornecidos.
    
    Args:
        email (str): E-mail do usuário.
        password (str): Senha em texto plano fornecida pelo usuário.
    
    Returns:
        Optional[Dict]: Dados do usuário se autenticado, None caso contrário.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user and check_password(password, user["password_hash"]):  # Verificar a senha
            return {
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"]
            }
        return None
    except Exception as e:
        logging.error(f"Erro ao autenticar usuário: {e}")
        raise e
    finally:
        if conn:
            conn.close()

# Função para carregar os chats de um usuário
def load_chats(user_id: str) -> Dict[str, Dict]:
    """
    Carrega os chats de um usuário do banco de dados.
    
    Args:
        user_id (str): ID do usuário.
    
    Returns:
        Dict[str, Dict]: Dicionário com os chats do usuário.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Carregar chats do usuário
        cursor.execute('SELECT * FROM chats WHERE user_id = ?', (user_id,))
        chats = cursor.fetchall()
        
        # Estrutura para armazenar os dados dos chats
        chat_data = {}
        for chat in chats:
            chat_id = chat["chat_id"]
            chat_data[chat_id] = {
                "id": chat_id,
                "pdf_name": chat["pdf_name"],
                "messages": [],
                "vectorstore": None,
            }
            
            # Carregar PDFs associados ao chat
            cursor.execute('SELECT * FROM pdfs WHERE chat_id = ?', (chat_id,))
            pdfs = cursor.fetchall()
            if pdfs:
                pdf = pdfs[0]
                chat_data[chat_id]["pdf_name"] = pdf["pdf_name"]
                chat_data[chat_id]["vectorstore"] = pdf["embeddings"]  # Aqui você pode carregar o FAISS se necessário
            
            # Carregar mensagens do chat
            cursor.execute('SELECT * FROM messages WHERE chat_id = ? ORDER BY timestamp', (chat_id,))
            messages = cursor.fetchall()
            for message in messages:
                chat_data[chat_id]["messages"].append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        return chat_data
    except Exception as e:
        logging.error(f"Erro ao carregar chats: {e}")
        raise e
    finally:
        if conn:
            conn.close()

# Função para criar um novo chat
def create_new_chat(user_id: str, pdf_name: Optional[str] = None) -> str:
    """
    Cria um novo chat no banco de dados.
    
    Args:
        user_id (str): ID do usuário.
        pdf_name (Optional[str]): Nome do PDF associado ao chat.
    
    Returns:
        str: ID do chat criado.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        chat_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO chats (chat_id, user_id, pdf_name, created_at)
            VALUES (?, ?, ?, datetime('now'))
        ''', (chat_id, user_id, pdf_name))
        conn.commit()
        
        logging.info(f"Chat {chat_id} criado com sucesso.")
        return chat_id
    except Exception as e:
        logging.error(f"Erro ao criar chat: {e}")
        raise e
    finally:
        if conn:
            conn.close()

# Função para excluir um chat
def delete_chat(chat_id: str) -> None:
    """
    Exclui um chat e todos os dados associados (PDFs, mensagens).
    
    Args:
        chat_id (str): ID do chat a ser excluído.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Excluir chat, PDFs e mensagens associados
        cursor.execute('DELETE FROM chats WHERE chat_id = ?', (chat_id,))
        cursor.execute('DELETE FROM pdfs WHERE chat_id = ?', (chat_id,))
        cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        conn.commit()
        
        logging.info(f"Chat {chat_id} excluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao excluir chat: {e}")
        raise e
    finally:
        if conn:
            conn.close()

# Função para salvar um PDF no banco de dados
def save_pdf(pdf_id: str, chat_id: str, pdf_name: str, text_chunks: List[str], embeddings: bytes) -> None:
    """
    Salva um PDF no banco de dados.
    
    Args:
        pdf_id (str): ID único do PDF.
        chat_id (str): ID do chat associado.
        pdf_name (str): Nome do PDF.
        text_chunks (List[str]): Lista de chunks de texto do PDF.
        embeddings (bytes): Embeddings serializados do PDF.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pdfs (pdf_id, chat_id, pdf_name, text_chunks, embeddings)
            VALUES (?, ?, ?, ?, ?)
        ''', (pdf_id, chat_id, pdf_name, json.dumps(text_chunks), embeddings))
        conn.commit()
        
        logging.info(f"PDF {pdf_name} salvo com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar PDF: {e}")
        raise e
    finally:
        if conn:
            conn.close()

# Função para salvar uma mensagem no banco de dados
def save_message(chat_id: str, role: str, content: str) -> None:
    """
    Salva uma mensagem no banco de dados.
    
    Args:
        chat_id (str): ID do chat associado.
        role (str): Papel da mensagem (user/assistant).
        content (str): Conteúdo da mensagem.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        message_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO messages (message_id, chat_id, role, content, timestamp)
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (message_id, chat_id, role, content))
        conn.commit()
        
        logging.info(f"Mensagem salva com sucesso no chat {chat_id}.")
    except Exception as e:
        logging.error(f"Erro ao salvar mensagem: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def get_total_document_count(user_id: str) -> int:
    """
    Retorna o número total de documentos carregados por um usuário.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM documents WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        logging.error(f"Erro ao obter contagem de documentos: {e}")
        raise e
    finally:
        if conn:
            conn.close()


def get_total_chat_count(user_id: str) -> int:
    """
    Retorna o número total de chats criados por um usuário.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM chats WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        logging.error(f"Erro ao obter contagem de chats: {e}")
        raise e
    finally:
        if conn:
            conn.close()