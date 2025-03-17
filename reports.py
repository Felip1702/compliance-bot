import streamlit as st
from utils import load_css
import pandas as pd
import random

def reports_app():
    load_css("styles.css")  # Ensure consistent styling

    st.markdown(
        """
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <i class="fas fa-chart-bar" style="font-size: 36px; color: #FF4B45; margin-right: 15px;"></i>
            <h2 style="color: #424242; font-size: 28px;">Relatórios de Uso</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    report_type = st.radio("Selecione o Tipo de Relatório:",
                         ["Atividade do Usuário", "Tópicos e Palavras-chave", "Documentos Acessados", "Satisfação do Usuário", "Consultas Não Resolvidas"],horizontal=True)


    # --- Conditionally Display Report Content ---
    if report_type is not None:
        if report_type == "Atividade do Usuário":
            df = get_mockup_user_activity()
            display_styled_dataframe(df, "Atividade do Usuário")
        elif report_type == "Tópicos e Palavras-chave":
            df = get_mockup_topics_keywords()
            display_styled_dataframe(df, "Tópicos e Palavras-chave")
        elif report_type == "Documentos Acessados":
            df = get_mockup_popular_documents()
            display_styled_dataframe(df, "Documentos Acessados")
        elif report_type == "Satisfação do Usuário":
            df = get_mockup_user_satisfaction()
            display_styled_dataframe(df, "Satisfação do Usuário")
        elif report_type == "Consultas Não Resolvidas":
            df = get_mockup_unresolved_queries()
            display_styled_dataframe(df, "Consultas Não Resolvidas")

def display_styled_dataframe(df, title):
    """Displays the mockup analysis results."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-top: 30px; margin-bottom: 15px;">
            <i class="fas fa-table" style="font-size: 24px; color: #FF4B45; margin-right: 10px;"></i>
            <h3 style="color: #424242; font-size: 22px; margin-bottom: 0;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Create HTML table
    html_table = f"""
    <style>
        .dataframe {{width: 100%; border-collapse: collapse; border: 1px solid #e0e0e0; margin-bottom: 20px;}}
        .dataframe th, .dataframe td {{padding: 10px; text-align: left; border-bottom: 1px solid #e0e0e0;}}
        .dataframe th {{background-color: #FF4B45; color: white; font-weight: bold;}}
        .dataframe tr:nth-child(even) {{background-color: #f9f9f9;}}
    </style>
    <table class="dataframe">
        <thead>
            <tr>
                <th></th>
                {''.join(f'<th>{col}</th>' for col in df.columns)}
            </tr>
        </thead>
        <tbody>
            {''.join(f'<tr><th>{i}</th>' + ''.join(f'<td>{value}</td>' for value in row.values.tolist()) + '</tr>' for i, row in df.iterrows())}
        </tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

def get_mockup_user_activity():
    data = {
        "Usuário": [f"Usuário {i}" for i in range(1, 6)],
        "Número de Consultas": [random.randint(10, 50) for _ in range(5)],
        "Data da Última Consulta": [f"2024-02-{random.randint(10, 28)}" for _ in range(5)],
        "Tempo Médio da Sessão (min)": [random.randint(5, 30) for _ in range(5)],
    }
    return pd.DataFrame(data)

def get_mockup_topics_keywords():
    data = {
        "Tópico": ["Férias", "Horas Extras", "Rescisão Contratual", "Adicional Noturno", "FGTS"],
        "Número de Consultas": [random.randint(10, 50) for _ in range(5)],
        "Palavras-chave": ["descanso, abono", "extra, jornada", "demissão, aviso", "noturno, adicional", "saque, multa"],
        "Exemplo de Perguntas": [
            "Como calcular minhas férias?",
            "Quais os direitos sobre horas extras?",
            "Como funciona a rescisão contratual?",
            "Qual o valor do adicional noturno?",
            "Como sacar o FGTS?"
        ]
    }
    return pd.DataFrame(data)

def get_mockup_popular_documents():
    data = {
        "Documento": [f"Documento {i}" for i in range(1, 6)],
        "Número de Acessos": [random.randint(5, 20) for _ in range(5)],
        "Região": ["Sul", "Sudeste", "Nordeste", "Centro-Oeste", "Norte"],
        "Data do Primeiro Acesso": [f"2023-{random.randint(1, 12)}-01" for _ in range(5)],
        "Data do Último Acesso": [f"2024-02-{random.randint(10, 28)}" for _ in range(5)],
    }
    return pd.DataFrame(data)

def get_mockup_user_satisfaction():
    data = {
        "Usuário": [f"Usuário {i}" for i in range(1, 6)],
        "Avaliação (1-5)": [random.randint(1, 5) for _ in range(5)],
        "Comentários": [
            "Muito útil!",
            "Poderia ser mais preciso.",
            "Excelente ferramenta.",
            "Faltou informação sobre...",
            "Recomendo!"
        ],
        "Data da Avaliação": [f"2024-02-{random.randint(10, 28)}" for _ in range(5)],
    }
    return pd.DataFrame(data)

def get_mockup_unresolved_queries():
    data = {
        "Consulta": [
            "Como abono pecuniário influencia no IR?",
            "O que acontece se eu faltar ao trabalho?",
            "Como funciona o banco de horas?",
            "Quais os direitos do jovem aprendiz?",
            "Como declarar horas extras no IR?"
        ],
        "Data da Consulta": [f"2024-02-{random.randint(10, 28)}" for _ in range(5)],
        "Motivo": [
            "Informação não encontrada na base de dados.",
            "Consulta fora do escopo de conhecimento.",
            "Consulta ambígua.",
            "Requer análise jurídica específica.",
            "Termos não reconhecidos."
        ],
    }
    return pd.DataFrame(data)

def get_mockup_lawsuit_data():
    """Retorna dados de mockup para os relatórios da análise trabalhista."""
    data = {
        "Nome do relatório": ["Análises por Categoria", "Risco por Setor", "Custos Totais"],
        "Data de criação": ["2024-01-01", "2024-01-01", "2024-01-01"],
        "Termos buscados": ["indenização, dano moral", "setor financeiro", "todos"],
        "Tribunal": ["Todos", "Todos", "Todos"],
        "Período": ["2023", "2023", "2023"],
        "Centro de custo": ["Todos", "Todos", "Todos"]
    }
    return pd.DataFrame(data)