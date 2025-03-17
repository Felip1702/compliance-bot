import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from database import get_total_document_count, get_total_chat_count

def dashboard_app():
    """
    Displays the main dashboard showing usage metrics with cards and charts.
    """

    if st.session_state.user_id:
        # Center the header
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <h1>Dashboard</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Separator and Chatbot section header
        st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display: flex; justify-content: left;">
                <h3>Chatbot</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        total_documents = get_total_document_count(st.session_state.user_id)
        total_chats = get_total_chat_count(st.session_state.user_id)

        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                st.markdown(
                   f"""
                       <div style="display: flex; flex-direction: column; align-items: center; border-radius: 10px; background-color: white; padding: 20px; border: 1px solid #e0e0e0;">
                            <div style="background-color: #ffe5e5; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                                 <i class="fas fa-file-pdf" style="font-size: 30px; color: #FF4B45;"></i>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 18px; color:#424242;">Total Documentos</div>
                                <div style="font-size: 24px; font-weight: bold; color:#424242;">{total_documents}</div>
                            </div>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col2:
            with st.container():
                st.markdown(
                   f"""
                       <div style="display: flex; flex-direction: column; align-items: center; border-radius: 10px; background-color: white; padding: 20px; border: 1px solid #e0e0e0;">
                            <div style="background-color: #ffe5e5; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                                 <i class="fas fa-comment-dots" style="font-size: 30px; color: #FF4B45;"></i>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 18px; color:#424242;">Total Chats</div>
                                <div style="font-size: 24px; font-weight: bold; color:#424242;">{total_chats}</div>
                            </div>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )
       
       # Mock data for chart
        document_analysis_data = {
            "days": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
            "documents": [10, 18, 15, 22, 27, 30, 25]
         }
        df_documents = pd.DataFrame(document_analysis_data)

        question_types_data = {
            "types": ["Políticas e Regulamentos Internos", "Treinamentos e Certificações", "Denúncias e Ética", "Regulamentações Externas", "Aprovações e Processos Internos"],
             "values": [35, 25, 15, 10, 15],
        }
        df_questions = pd.DataFrame(question_types_data)
        colors = ['#FF4B45','#ff8585', '#ffb2b2', '#ffe5e5', '#ffe5e5']
        
        # Create a container for the plots so they don't take the entire with
        with st.container():
            col_chart_1, col_chart_2 = st.columns(2)
            with col_chart_1:
                 # Line chart
                 fig_line = go.Figure(data=[go.Scatter(
                    x=df_documents["days"],
                    y=df_documents["documents"],
                    mode="lines",
                    line=dict(color="#FF4B45"),
                    fill="tonexty",
                    fillcolor="rgba(255, 75, 69, 0.1)"
                )])
                
                 fig_line.update_layout(
                  title="Documentos Analisados por Dia",
                  plot_bgcolor="rgba(0,0,0,0)",
                  paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color='#424242'),
                    xaxis=dict(gridcolor='#e0e0e0'),
                    yaxis=dict(gridcolor='#e0e0e0'),
                     
                 )
                 
                 st.plotly_chart(fig_line, use_container_width=True)
            
            with col_chart_2:
                # Doughnut chart
                fig_donut = go.Figure(data=[go.Pie(
                   labels=df_questions["types"],
                   values=df_questions["values"],
                   hole=0.4,
                   marker_colors = colors,
                   textinfo='percent', # Show Percent info inside the graph
                   insidetextorientation='radial' # Set the percent directiom
                )])
                
                fig_donut.update_layout(
                     title="Distribuição de Tipos de Perguntas",
                     plot_bgcolor="rgba(0,0,0,0)",
                     paper_bgcolor="rgba(0,0,0,0)",
                      showlegend=True,
                    font=dict(color='#424242'),
                )
                st.plotly_chart(fig_donut, use_container_width=True)

        # --- Labor Lawsuit Analysis Section ---
        st.markdown("<hr style='margin-top: 30px; margin-bottom: 15px; border: none; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display: flex; justify-content: left;">
                <h3>Analise Trabalhista</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        lawsuit_col1, lawsuit_col_2 = st.columns(2)

        # Mockup Data for Lawsuit Analysis Metrics
        total_lawsuits_analyzed = 50
        average_win_rate = 0.70  # 70%
        average_settlement_value = 35000  # R$ 35,000.00

        with lawsuit_col1:
            with st.container():
                st.markdown(
                   f"""
                       <div style="display: flex; flex-direction: column; align-items: center; border-radius: 10px; background-color: white; padding: 20px; border: 1px solid #e0e0e0;">
                            <div style="background-color: #ffe5e5; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                                 <i class="fas fa-balance-scale" style="font-size: 30px; color: #FF4B45;"></i>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 18px; color:#424242;">Processos Analisados</div>
                                <div style="font-size: 24px; font-weight: bold; color:#424242;">{total_lawsuits_analyzed}</div>
                            </div>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

        with lawsuit_col_2:
            with st.container():
                st.markdown(
                   f"""
                       <div style="display: flex; flex-direction: column; align-items: center; border-radius: 10px; background-color: white; padding: 20px; border: 1px solid #e0e0e0;">
                            <div style="background-color: #ffe5e5; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                                 <i class="fas fa-chart-line" style="font-size: 30px; color: #FF4B45;"></i>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 18px; color:#424242;">Taxa Média de Sucesso</div>
                                <div style="font-size: 24px; font-weight: bold; color:#424242;">{average_win_rate:.0%}</div>
                            </div>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Mock data for agreement suggestion
        agreement_suggestion = {
            "types": ["Excelentes", "Bons", "Médios", "Ruins", "Muito Ruins"],
             "values": [25, 30, 15, 10, 20],
        }
        df_agreement = pd.DataFrame(agreement_suggestion)

        with st.container():
            st.markdown(
                   f"""
                       <div style="display: flex; flex-direction: column; align-items: center; border-radius: 10px; background-color: white; padding: 20px; border: 1px solid #e0e0e0;">
                            <div style="text-align: center;">
                                <div style="font-size: 18px; color:#424242;">Sugestão Média de Acordo: R$ {average_settlement_value:,.2f}</div>
                            </div>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )
            # Doughnut chart
            fig_agreement = go.Figure(data=[go.Pie(
               labels=df_agreement["types"],
               values=df_agreement["values"],
               hole=0.4,
               marker_colors = colors,
               textinfo='percent', # Show Percent info inside the graph
               insidetextorientation='radial' # Set the percent directiom
            )])
            
            fig_agreement.update_layout(
                 title="Qualidade dos Processos",
                 plot_bgcolor="rgba(0,0,0,0)",
                 paper_bgcolor="rgba(0,0,0,0)",
                  showlegend=True,
                font=dict(color='#424242'),
            )
            st.plotly_chart(fig_agreement, use_container_width=True)
    
    else:
         st.warning("Usuário não está autenticado")


if __name__ == '__main__':
    # this code is just for testing purposes
    import os
    os.environ["OPENAI_API_KEY"] = "sk-"

    st.session_state.user_id = "test_user"
    dashboard_app()