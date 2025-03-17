import streamlit as st
import bcrypt

def hash_password(password: str) -> str:
    """
    Gera um hash da senha fornecida.
    
    Args:
        password (str): Senha em texto plano.
    
    Returns:
        str: Hash da senha.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    
    Args:
        password (str): Senha em texto plano.
        hashed_password (str): Hash da senha armazenado.
    
    Returns:
        bool: True se a senha corresponder, False caso contrário.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def load_css(file_path: str) -> None:
    """
    Carrega um arquivo CSS e aplica o estilo à interface do Streamlit.
    
    Args:
        file_path (str): Caminho para o arquivo CSS.
    """
    try:
        with open(file_path, "r") as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo CSS não encontrado: {file_path}")
    except Exception as e:
        st.error(f"Erro ao carregar CSS: {e}")