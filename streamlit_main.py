import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Examen", page_icon="🤖")
st.title("🤖 Chatbot con LangChain")
st.markdown("Chatbox de examen construido con LangChain + Streamlit.")

model_name = st.selectbox(
    "Elige el modelo:",
    [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],
    index=0
)

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

if st.button("Limpiar chat"):
    st.session_state.mensajes = []

# Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# Renderizar historial existente
for msg in st.session_state.mensajes:

    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")

slider = st.slider(label="Temperatura", min_value=0.1, max_value=1.0, value=0.7)

if pregunta:
    chat_model.temperature = slider
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)