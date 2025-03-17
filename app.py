# app.py
import streamlit as st
from streamlit_option_menu import option_menu

# Configuração da página (deve ser a primeira chamada do Streamlit)
st.set_page_config(
    page_title="Compliance Buddy Bot",
    page_icon="🤖",
    layout="wide",
)

# Agora importe outros módulos e funções
from chat import chatbot_app
from utils import load_css
from database import create_documents_table
from auth import login, signin
from documents import documents_app
from dashboard import dashboard_app # import dashboard module
from lawsuits import lawsuits_app
from reports import reports_app # import reports module

# Carregar CSS personalizado
load_css("styles.css")


# Função principal do aplicativo
def main():
    # Criar tabela de documentos (se não existir)
    create_documents_table()

    # Inicializar estado da sessão
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.show_signin = False
        st.session_state.chats = {}  # Inicializar chats
        st.session_state.current_chat = None  # Inicializar current_chat

    # Verificar se o usuário está autenticado
    if not st.session_state.get("user_id"):
        if st.session_state.get("show_signin"):
            signin()
        else:
            login()
        return  # Impede a execução do restante do código até que o usuário se autentique

    # Menu lateral
    with st.sidebar:
        # Menu Title
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <i class="fas fa-desktop" style="font-size: 24px; color: #424242; margin-right: 8px;"></i>
                <span style="font-size: 20px; font-weight: 500; color: #424242;">Main Menu</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Horizontal Line Separator
        st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)


        menu_option = option_menu(
            menu_title=None,  # No main title, menu is the title already
            options=["Home", "Gestão de Documentos", "Chat", "Análise Trabalhista", "Relatórios", "Ajustes"],
             icons=['house-fill', 'cloud-upload-fill', "chat-fill", "briefcase-fill", "file-earmark-bar-graph", 'gear-fill'],  # Icons from bootstrap
            menu_icon=None,  # No main menu icon
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {
                    "color": "#F0F2F6",
                    "font-size": "18px",
                    "margin-right": "8px",
                  },
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin":"0px",
                    "--hover-color": "#FF4B45",
                    "color":"#424242",
                },
                "nav-link-selected": {"background-color": "#FF4B45", "color": "white",}
            },
            orientation="vertical"

        )
    
    if menu_option == "Home":
       dashboard_app()
    elif menu_option == "Chat":
        chatbot_app()
    elif menu_option == "Gestão de Documentos":
        documents_app()
    elif menu_option == "Análise Trabalhista":
        lawsuits_app()
    elif menu_option == "Relatórios":
        reports_app()
    elif menu_option == "Ajustes":
        st.write("Settings page")

if __name__ == '__main__':
    main()