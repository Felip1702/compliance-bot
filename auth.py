import streamlit as st
import uuid
import logging
from database import save_user, authenticate_user
from utils import hash_password, check_password
from auth_styles import get_auth_styles  # Importar o CSS personalizado

def login():
    # Aplicar o CSS personalizado
    st.markdown(get_auth_styles(), unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        # Adicionar o ícone do robô e o título dentro do formulário
        st.markdown(
            """
            <div class="form-header">
                <i class="fas fa-robot"></i>
                <h1>Compliance Buddy Bot</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Campos de e-mail e senha
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")

        # Container para os botões
        col1, col2 = st.columns([1, 1])
        with col1:
            # Botão "Entrar"
            submit_button = st.form_submit_button("Entrar", type="primary", use_container_width=True)
        with col2:
            # Botão "Criar Conta"
            create_account_button = st.form_submit_button("Criar Conta", type="secondary", use_container_width=True)

        if submit_button:
            user = authenticate_user(email, password)
            if user:
                st.session_state.user_id = user["user_id"]
                st.session_state.user_name = user["name"]
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
        
        if create_account_button:
            st.session_state.show_signin = True
            st.rerun()

def signin():
    # Aplicar o CSS personalizado
    st.markdown(get_auth_styles(), unsafe_allow_html=True)

    st.title("Criar Conta")
    name = st.text_input("Nome")
    email = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirmar Senha", type="password")
    
    if st.button("Cadastrar"):
        if password != confirm_password:
            st.error("As senhas não coincidem.")
        elif len(password) < 8 or not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
            st.error("A senha deve ter pelo menos 8 caracteres, uma letra maiúscula e um número.")
        else:
            try:
                user_id = str(uuid.uuid4())  # Gerar um ID único para o usuário
                password_hash = hash_password(password)
                save_user(user_id, name, email, password_hash)
                st.success("Conta criada com sucesso! Faça login para continuar.")
                st.session_state.show_signin = False
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao cadastrar usuário: {e}")
                logging.error(f"Erro ao cadastrar usuário: {e}")  # Log do erro
    
    if st.button("Voltar para Login"):
        st.session_state.show_signin = False
        st.rerun()