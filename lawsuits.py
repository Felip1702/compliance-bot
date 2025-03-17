import streamlit as st
import uuid
import os
from utils import load_css  # Assuming you have utils.py
import base64
import time
import random

def lawsuits_app():
    load_css("styles.css")  # Ensure consistent styling
    st.markdown(
        """
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <i class="fas fa-balance-scale" style="font-size: 36px; color: #FF4B45; margin-right: 15px;"></i>
            <h2 style="color: #424242; font-size: 28px;">Análise de Processos Trabalhistas</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    
    # File Uploader
    uploaded_file = st.file_uploader(
        "Selecione um Arquivo de Processo (PDF)", type="pdf"
    )

    if uploaded_file:
        if st.button("Analisar Processo", type="primary"):  # Streamlit button styling
            # Simulate analysis and results
            with st.spinner("Analisando o Processo..."):
                time.sleep(4) # Wait some seconds
                st.session_state.mock_analysis_results = simulate_lawsuit_analysis()
                st.session_state.show_results = True
                st.success("Análise Concluída!")
                st.rerun()

        # Conditionally Display mockup analysis results
        if st.session_state.show_results:
            display_mock_results(st.session_state.mock_analysis_results, uploaded_file.name)
    else:
        st.info("Por favor, selecione um arquivo PDF para análise.")


def simulate_lawsuit_analysis():
    """Simulates the analysis of a labor lawsuit and returns mockup results."""
    chance_de_ganho = f"{random.randint(50, 95)}%"
    valor_pedido = f"R$ {random.randint(10000, 100000):,.2f}".replace(",", ".")
    valor_sugerido_acordo = f"R$ {random.randint(5000, 40000):,.2f}".replace(",", ".")
    custos_estimados = f"R$ {random.randint(1000, 8000):,.2f}".replace(",", ".")

    riscos_options = [
        ["Condenação em horas extras", "Dificuldade na comprovação da jornada de trabalho", "Falta de registro adequado do ponto"],
        ["Adicional de Insalubridade", "Ausência de laudo técnico favorável", "Não fornecimento de EPIs adequados"],
        ["Dano moral", "Assédio moral comprovado", "Ofensa à honra do trabalhador"],
        ["Reversão da justa causa", "Falta de provas da falta grave", "Desproporcionalidade da punição"],
        ["Reconhecimento de vínculo empregatício", "Subordinação comprovada", "Onerosidade do trabalho"],
    ]

    # Select one list of riscos_options
    selected_riscos = random.choice(riscos_options)
    fundamentacao = [
        f"Baseado em casos similares, a chance de ganho é {chance_de_ganho} devido à robustez das provas apresentadas.",
        f"O valor pedido está alinhado com a média das indenizações concedidas em casos semelhantes.",
        "A realização de um acordo extrajudicial pode evitar custos processuais e acelerar a resolução do conflito."
    ]

    return {
        "chance_de_ganho": chance_de_ganho,
        "valor_pedido": valor_pedido,
        "melhor_estrategia": random.choice(["Realizar acordo extrajudicial", "Seguir com o litígio"]),
        "valor_sugerido_acordo": valor_sugerido_acordo,
        "custos_estimados": custos_estimados,
        "principais_riscos": selected_riscos,
        "fundamentacao": fundamentacao,
    }


def display_mock_results(results, filename):
    """Displays the mockup analysis results."""
    st.markdown(
        """
        <div style="display: flex; align-items: center; margin-top: 30px; margin-bottom: 15px;">
            <i class="fas fa-chart-bar" style="font-size: 24px; color: #FF4B45; margin-right: 10px;"></i>
            <h3 style="color: #424242; font-size: 22px; margin-bottom: 0;">Resultados da Análise</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <i class="fas fa-trophy" style="font-size: 20px; color: #FF4B45; margin-right: 8px;"></i>
                <span style="font-weight: bold; color: #424242;">Chance de Ganho:</span> {results['chance_de_ganho'] if 'chance_de_ganho' in results else "Valor não informado"}
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <i class="fas fa-money-bill-wave" style="font-size: 20px; color: #FF4B45; margin-right: 8px;"></i>
                <span style="font-weight: bold; color: #424242;">Valor Estimado do Pedido:</span> {results['valor_pedido'] if 'valor_pedido' in results else "Valor não informado"}
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <i class="fas fa-exclamation-triangle" style="font-size: 20px; color: #FF4B45; margin-right: 8px;"></i>
                <span style="font-weight: bold; color: #424242;">Custos Estimados:</span> {results['custos_estimados'] if 'custos_estimados' in results else "R$5.000"}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <i class="fas fa-handshake" style="font-size: 20px; color: #FF4B45; margin-right: 8px;"></i>
                <span style="font-weight: bold; color: #424242;">Melhor Estratégia:</span> {results['melhor_estrategia'] if 'melhor_estrategia' in results else "Valor não informado"}
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <i class="fas fa-comments-dollar" style="font-size: 20px; color: #FF4B45; margin-right: 8px;"></i>
                <span style="font-weight: bold; color: #424242;">Valor Sugerido para Acordo:</span> {results['valor_sugerido_acordo'] if 'valor_sugerido_acordo' in results else "Valor não informado"}
            </div>
        """, unsafe_allow_html=True)

        riscos_str = ", ".join(results['principais_riscos']) if "principais_riscos" in results else "Valor não informado"
        st.markdown(f"""
            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <i class="fas fa-shield-alt" style="font-size: 20px; color: #FF4B45; margin-right: 8px;"></i>
                <span style="font-weight: bold; color: #424242;">Principais Riscos:</span> {riscos_str}
            </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="display: flex; align-items: center; margin-top: 20px; margin-bottom: 10px;">
            <i class="fas fa-file-alt" style="font-size: 24px; color: #FF4B45; margin-right: 10px;"></i>
            <h4 style="color: #424242; font-size: 20px; margin-bottom: 0;">Fundamentação:</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item in results.get('fundamentacao', []):
        st.markdown(f"""<div style="background-color: #f9f9f9; border-radius: 5px; padding: 10px; margin-bottom: 5px;">
            <i class="fas fa-arrow-right" style="font-size: 14px; color: #FF4B45; margin-right: 5px;"></i> {item}</div>""", unsafe_allow_html=True)

    # Action Buttons - Added margin-top for spacing
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    col_actions_1, col_actions_2 = st.columns(2)
    with col_actions_1:
        # Mockup: Generates a string with all results
        analysis_string = f"""
            Resultados da Análise do Processo: {filename}

            Chance de Ganho: {results.get('chance_de_ganho', 'N/A')}
            Valor Estimado do Pedido: {results.get('valor_pedido', 'N/A')}
            Melhor Estratégia: {results.get('melhor_estrategia', 'N/A')}
            Valor Sugerido para Acordo: {results.get('valor_sugerido_acordo', 'N/A')}
            Custos Estimados: {results.get('custos_estimados', 'N/A')}
            Principais Riscos: {', '.join(results['principais_riscos']) if "principais_riscos" in results else "Valor não informado"}

            Fundamentação:
            {chr(10).join([f'- {item}' for item in results.get('fundamentacao', [])])}
        """

        # Encode to Base64
        b64 = base64.b64encode(analysis_string.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" style="text-decoration:none !important; color: white !important; background-color: #FF4B45; padding: 0.5em 1em; border-radius: 0.3em;" download="analise_{filename}.txt"><i class="fas fa-download" style="margin-right: 0.5em;"></i>Baixar Análise</a>'

        st.markdown(href, unsafe_allow_html=True)

    with col_actions_2:
        st.button("Enviar Análise por Email", disabled=True)