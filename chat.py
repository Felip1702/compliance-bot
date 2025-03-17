import streamlit as st
import uuid
import logging
import os
from database import (
    load_chats, create_new_chat, delete_chat, save_message, get_user_documents
)
from pdf_processing import process_pdf
from auth import login, signin
from utils import load_css
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage  # Importar HumanMessage e AIMessage
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# Importações para adicionar memória ao chatbot
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated, TypedDict

# Caminho fixo para a pasta de embeddings
EMBEDDINGS_DIR = os.path.abspath("./embeddings_store")

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Definir o estado da conversa
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Criar uma instância do MemorySaver para salvar o estado da conversa
memory = MemorySaver()

# Função principal do chatbot
def chatbot_app():
    # Verificar se o usuário está autenticado
    if not st.session_state.get("user_id"):
        if st.session_state.get("show_signin"):
            signin()
        else:
            login()
        return

    # Carregar chats do usuário
    if "chats" not in st.session_state or not st.session_state.chats:
        st.session_state.chats = load_chats(st.session_state.user_id)

    # Configuração do thread_id para manter o contexto
    thread_id = st.session_state.get("current_chat", "default_thread")

    # Configuração do estado inicial
    if "state" not in st.session_state:
        st.session_state.state = {}  # Dicionário para armazenar o estado de cada chat

    # Sidebar
    with st.sidebar:
        st.title(f'🤖 Olá, {st.session_state.user_name}!')
        st.markdown('''''')

        # Botão para criar novo chat
        if st.button("➕ Novo Chat"):
            chat_id = create_new_chat(st.session_state.user_id)
            st.session_state.current_chat = chat_id
            st.session_state.chats[chat_id] = {
                "id": chat_id,
                "messages": [],
                "region_selected": None,
            }
            st.session_state.state[chat_id] = {"messages": []}  # Reiniciar o estado da conversa
            st.rerun()

        # Lista de chats
        st.subheader("Histórico de Chats")
        for chat_id, chat_data in st.session_state.chats.items():
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"💬 Chat {chat_id[:8]}", key=f"chat_{chat_id}"):
                    st.session_state.current_chat = chat_id
                    st.rerun()
            with col2:
                if st.button("❌", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)
                    del st.session_state.chats[chat_id]
                    if st.session_state.current_chat == chat_id:
                        st.session_state.current_chat = None
                    st.rerun()

        # Botão para sair
        if st.button("Sair"):
            st.session_state.clear()
            st.rerun()

    # Área principal
    if st.session_state.current_chat is not None:
        current_chat_data = st.session_state.chats.get(st.session_state.current_chat)
        if not current_chat_data:
            st.error("Chat não encontrado. Por favor, crie um novo chat.")
            return

        st.header(f"Chat {st.session_state.current_chat[:8]}")

        # Region Selection Logic (mantenha a lógica existente)
        if current_chat_data["region_selected"] is None:
            region_options = {
                "1": "Asia",
                "2": "Europe",
                "3": "North America",
                "4": "South America",
            }
            region_prompt = (
                "Qual região você quer consultar? Digite apenas o número da região:\n"
                "1) Asia\n"
                "2) Europe\n"
                "3) North America\n"
                "4) South America"
            )

            with st.chat_message("assistant"):
                st.write(region_prompt)

            if region_choice := st.chat_input("Digite o número da região desejada:"):
                if region_choice in region_options:
                    current_chat_data["region_selected"] = region_options[region_choice]
                    st.session_state.chats[st.session_state.current_chat] = current_chat_data
                    st.rerun()  # Refresh to load embeddings
                else:
                    st.error("Opção inválida. Por favor, digite um número entre 1 e 4.")
            else:
                st.stop()  # Stop if no choice is made.

        selected_region = current_chat_data["region_selected"]

        # Load the FAISS index for the selected region (mantenha a lógica existente)
        region_path = os.path.join(EMBEDDINGS_DIR, selected_region)
        combined_vectorstore = None
        for root, dirs, files in os.walk(region_path):
            for dir_name in dirs:
                save_path = os.path.join(root, dir_name)
                logging.info(f"Tentando carregar embeddings do diretório: {save_path}")
                if os.path.exists(save_path):
                    try:
                        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
                        vectorstore = FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
                        if combined_vectorstore is None:
                            combined_vectorstore = vectorstore
                        else:
                            combined_vectorstore.merge_from(vectorstore)
                        logging.info(f"Embeddings carregados com sucesso do diretório: {save_path}")
                    except Exception as e:
                        logging.error(f"Erro ao carregar embeddings do diretório {save_path}: {e}")
                        st.error(f"Erro ao carregar embeddings do diretório {save_path}: {e}")
                else:
                    logging.warning(f"Diretório não encontrado: {save_path}")
                    st.warning(f"Diretório não encontrado: {save_path}")

        if combined_vectorstore is None:
            st.warning(f"Nenhum documento carregado para a região {selected_region}. Por favor, carregue documentos no módulo de gestão.")
            return

        # Obter o estado do chat atual
        current_chat_id = st.session_state.current_chat
        if current_chat_id not in st.session_state.state:
            st.session_state.state[current_chat_id] = {"messages": []}

        # Usar o estado do chat atual
        chat_state = st.session_state.state[current_chat_id]

        # Exibir histórico de mensagens
        for message in chat_state["messages"]:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)

        # Interação com o chatbot
        if prompt := st.chat_input("Pergunte-me qualquer coisa sobre os documentos..."):
            # Exibir a pergunta do usuário
            with st.chat_message("user"):
                st.markdown(prompt)

            # Adicionar a pergunta do usuário ao estado *antes* da resposta do chatbot
            chat_state["messages"].append(HumanMessage(content=prompt))

            # Executar o grafo com o estado atual
            config = {"configurable": {"thread_id": current_chat_id}}
            
            # Get all docs retrieved
            retriever = combined_vectorstore.as_retriever()
            retrieved_docs = retriever.invoke(prompt)

            # Get content of the docs
            content = "\n".join([doc.page_content for doc in retrieved_docs])
            context = content[:4000]  # Limitar o tamanho do contexto

            # Initialize references before the loop
            references = ""
            unique_references = set()  # Use a set to store unique references

            events = graph.stream(
                {"messages": chat_state["messages"]},  # Usar TODAS as mensagens para o contexto
                config,
                stream_mode="values",
            )

            # Processar eventos e obter resposta do chatbot
            full_response = ""
            for event in events:
                if "messages" in event:
                    ai_message = event["messages"][-1]  # pegar a última mensagem do assistente
                    full_response = ai_message.content

            # Getting the reference based on the docs:
            for doc in retrieved_docs:
                pdf_name = doc.metadata.get('pdf_name', 'Nome Desconhecido')
                page_number = doc.metadata.get('page_number', 'Seção Desconhecida')  # Use get()

                # Construct the reference string
                ref = f"\n**Referência:** {pdf_name}, Pag:{page_number}"  # BOLD here!

                # Check this to prevent duplicates.
                if ref not in unique_references:
                    unique_references.add(ref)
                    references += ref

            full_response += f"\n{references}"  # Add new references

            # Adicionar a resposta do chatbot ao estado
            chat_state["messages"].append(AIMessage(content=full_response))
            st.session_state.state[current_chat_id] = chat_state  # Atualizar o estado da sessão

            # Exibir a resposta do chatbot
            with st.chat_message("assistant"):
                st.markdown(full_response)

    else:
        st.info("Nenhum chat selecionado. Crie um novo chat ou selecione um existente.")

# Configuração do grafo com checkpointing
graph_builder = StateGraph(State)

def chatbot(state: State):
    # Obter a última mensagem do usuário
    user_message = state["messages"][-1].content

    # Escolher modelo com base na complexidade da consulta
    model_name = "gpt-4" if len(user_message.split()) >= 5 else "gpt-3.5-turbo"
    llm = ChatOpenAI(temperature=0.0, model_name=model_name)

    # Gerar resposta com base no contexto
    response = llm.invoke(state["messages"])
    return {"messages": [AIMessage(content=response.content)]}  # Retornar uma AIMessage

graph_builder.add_node("chatbot", chatbot)

# Remova a referência à 'tool' e ajuste o ToolNode
tool_node = ToolNode(tools=[])  # Sem ferramentas externas
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=memory)

# Inicialização do Streamlit
if __name__ == '__main__':
    chatbot_app()