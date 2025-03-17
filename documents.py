import streamlit as st
import uuid
import os
from database import save_document, get_user_documents, delete_document
from pdf_processing import process_pdf

def documents_app():
    # Region options
    region_options = ["South America", "Europe", "Asia", "North America"]

    # Document categories
    document_categories = ["Políticas", "Procedimentos"]

    # Initialize session state for file, region, and category
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "selected_region" not in st.session_state:
        st.session_state.selected_region = None
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None

    # File uploader
    uploaded_file = st.file_uploader(
        "Selecione um PDF", type="pdf"
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        # Button to trigger upload and processing
        upload_button_disabled = uploaded_file is None or st.session_state.selected_region is None or st.session_state.selected_category is None
        if st.button("Carregar novo documento", disabled=upload_button_disabled):
            st.session_state.uploaded_file = uploaded_file
            if st.session_state.uploaded_file:
                document_id = str(uuid.uuid4())
                pdf_name = st.session_state.uploaded_file.name
                pdf_size = st.session_state.uploaded_file.size

                # Processar o PDF e salvar metadados
                with st.spinner(f"Processando {pdf_name}..."):
                    try:
                        # Passar a região e a categoria para o process_pdf
                        pdf_id, chunks, vectorstore = process_pdf(st.session_state.uploaded_file, document_id, st.session_state.selected_region)

                        # Salvar metadados no banco de dados, incluindo a categoria
                        save_document(
                            document_id, 
                            st.session_state.user_id, 
                            pdf_name, 
                            pdf_size, 
                            st.session_state.selected_region, 
                            st.session_state.selected_category  # Novo argumento: categoria
                        )

                        if vectorstore:
                            st.success(f"Documento {pdf_name} carregado com sucesso!")
                        else:
                            st.warning(f"Documento {pdf_name} salvo, mas embeddings não foram gerados. Algumas funcionalidades podem estar limitadas.")

                        # Limpar o arquivo e as seleções após o upload
                        st.session_state.uploaded_file = None
                        st.session_state.selected_region = None
                        st.session_state.selected_category = None
                        st.rerun()

                    except Exception as e:
                        st.error(f"Erro ao processar {pdf_name}: {e}")

    with col2:
        # Region selection
        if uploaded_file:
            st.session_state.selected_region = st.selectbox(
                f"Selecione a região para {uploaded_file.name}",
                region_options,
                key="region_select"
            )

            # Category selection
            st.session_state.selected_category = st.selectbox(
                f"Selecione a categoria para {uploaded_file.name}",
                document_categories,
                key="category_select"
            )

    # Dentro da função documents_app(), antes de listar os documentos
    st.subheader("Selecione uma Categoria")

    # Criar dois cards lado a lado
    col1, col2 = st.columns(2)

    with col1:
        # Card para "Políticas"
        st.markdown(
            f"""
            <div style="
                background-color: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
            ">
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #ffe5e5;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    margin: 0 auto 10px auto;
                ">
                    <i class="fas fa-balance-scale" style="font-size: 24px; color: #FF4B45;"></i>
                </div>
                <div style="font-size: 18px; color: #424242; font-weight: 400;">Políticas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Acessar Políticas", key="politicas_button"):
            st.session_state.selected_category = "Políticas"
            st.rerun()

    with col2:
        # Card para "Procedimentos"
        st.markdown(
            f"""
            <div style="
                background-color: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
            ">
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #ffe5e5;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    margin: 0 auto 10px auto;
                ">
                    <i class="fas fa-chart-line" style="font-size: 24px; color: #FF4B45;"></i>
                </div>
                <div style="font-size: 18px; color: #424242; font-weight: 400;">Procedimentos</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Acessar Procedimentos", key="procedimentos_button"):
            st.session_state.selected_category = "Procedimentos"
            st.rerun()

    # Exibir documentos filtrados por categoria (abaixo dos botões)
    if st.session_state.get("selected_category"):
        st.subheader(f"Documentos de {st.session_state.selected_category}")
        documents = get_user_documents(st.session_state.user_id)
        
        # Filtrar documentos pela categoria selecionada
        filtered_documents = [doc for doc in documents if doc.get("category") == st.session_state.selected_category]
        
        if filtered_documents:
            for document in filtered_documents:
                # Card para cada documento
                col1, col2 = st.columns([4, 1]) # Add column for the button

                with col1:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #ffffff;
                            border: 1px solid #e0e0e0;
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 10px;
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        ">
                            <div style="display: flex; align-items: center;">
                                <div style="
                                    background-color: #ffe5e5;
                                    border-radius: 10px;
                                    padding: 10px;
                                    margin-right: 15px;
                                ">
                                    <i class="fas fa-file-pdf" style="font-size: 24px; color: #FF4B45;"></i>
                                </div>
                                <div>
                                    <div style="font-size: 16px; font-weight: bold; color: #424242;">{document['pdf_name']}</div>
                                    <div style="font-size: 14px; color: #757575;">Tamanho: {document['pdf_size']} bytes</div>
                                    <div style="font-size: 14px; color: #757575;">Data de Upload: {document['upload_date']}</div>
                                    <div style="font-size: 14px; color: #757575;">Região: {document['region']}</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col2:
                    # Buttom to exclude docs, with a delete action
                    if st.button("Excluir", key=f"delete_{document['document_id']}"):
                         delete_document(document['document_id'])
                         st.rerun()

        else:
            st.info(f"Nenhum documento encontrado na categoria {st.session_state.selected_category}.")