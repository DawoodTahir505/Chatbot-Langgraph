import streamlit as st
from chatbotbackend import chatbot
from langchain_core.messages import HumanMessage

# st session state dict




message_history = []



config = {"configurable": {"thread_id": "thread-1"}}




if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])




message_history = []



user_input = st.chat_input("Type here...")

if user_input:

    st.session_state['message_history'].append({'role' : 'user', 'content' : user_input})
    with st.chat_message("user"):
        st.text(user_input)


    # response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)
    # ai_message = response['messages'][-1].content

    # ai_message = st.session_state['message_history'].append({'role' : 'assistant', 'content' : ai_message})
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk for message_chunk, metadata in chatbot.stream(
            {'messages':[HumanMessage(content=user_input)]}, 
            config={'configurable': {'thread_id': 'thread-1'}},
            stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role' : 'assistant', 'content' : ai_message})
        



