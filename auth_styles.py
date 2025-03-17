def get_auth_styles():
    """
    Retorna o CSS personalizado para a tela de autenticação (login e criação de conta).
    """
    return """
    <style>
    /* Estilo para o formulário de login */
    div.stForm {
        background-color: #F0F2F6 !important;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        width: 400px !important; /* Reduzir o tamanho do formulário */
        margin: 20px auto !important; /* Centralizar o formulário */
    }
    /* Estilo para os inputs */
    div.stTextInput input, div.stTextInput input:focus {
        background-color: #FFFFFF !important;
        border: 1px solid #ccc !important;
        border-radius: 5px !important;
        width: 100% !important; /* Ajustar largura dos inputs */
        padding: 8px !important; /* Add some padding */
    }
     /* Estilo para o campo de senha */
    div.stTextInput[data-testid="stTextInput"] {
        width: 100% !important; /* Garantir que o campo de senha tenha a mesma largura */
    }
    /* Estilo para os botões */
    div.stButton button {
        border: none !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        width: 100% !important; /* Ajustar largura dos botões */
        margin-top: 10px !important; /* Add some spacing */
    }
    /* Estilo específico para o botão "Entrar" */
    div.stButton button[data-testid="baseButton-primaryFormSubmit"] {
        background-color: #FF4B45 !important;
        color: white !important;
    }
     /* Estilo para o botão "Criar Conta" */
    div.stButton button[data-testid="baseButton-secondaryFormSubmit"] {
        background-color: transparent !important;
        color: #FF4B45 !important;
        border: 1px solid #FF4B45 !important;
    }
    /* Estilo para o ícone e título dentro do formulário */
    .form-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .form-header i {
        font-size: 48px;
        color: #FF4B45;
    }
    .form-header h1 {
        font-size: 24px;
        color: #1a1a1a; /* Cor do título */
        margin-top: 10px;
    }
    </style>
    """