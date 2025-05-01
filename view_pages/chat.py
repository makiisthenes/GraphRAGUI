from datetime import datetime

import streamlit as st
from tinydb import TinyDB

from GraphRAGWrapper import GraphRAGWrapper
from utils import export_chat

# GraphRAG Chat needed...
# https://discuss.streamlit.io/t/persist-memory-and-answer/50405/2


# Initialize chat history
# db = TinyDB(st.text_input('Enter the filename for chat history:',
# 						  value=f'save_folder/chat_history_{datetime.now().strftime("%Y-%m-%d")}.json'))
# chat_history = db.table('chat_history')

st.title("GraphRAG Chat")
st.markdown("Developed by Michael, Research by Microsoft, https://arxiv.org/pdf/2404.16130")
st.markdown("Please wait for up to 1 minute for a response, and export the chat history to save it...")
st.markdown("-----")

with st.sidebar:
	# Give options for previous chats to load...
	st.header("Chat History List")

	st.markdown("----")
	st.header("Estimated Cost")
	st.text("Estimated cost per request: $0.33-$0.65")
	st.text(f"Total Request Made: {0}")

	st.markdown("----")
	st.header("Export Chat")
	export_format = st.selectbox("Select export format:", ["txt", "docx", "pdf"])
	if st.button("Export Chat"):
		if st.session_state.messages:
			try:
				filename = export_chat(st.session_state.messages, export_format)
				st.success(f"Chat exported successfully to {filename}")

				# Create download button
				with open(filename, 'rb') as f:
					st.download_button(
						label="Download Export",
						data=f,
						file_name=filename,
						mime=f"application/{export_format}"
					)
			except Exception as e:
				st.error(f"Export failed: {str(e)}")
		else:
			st.warning("No messages to export")
			st.warning("No messages to export")



# Initialize chat history and context or load chat...
if "messages" not in st.session_state:
	st.session_state.messages = []

if "context" not in st.session_state:
	st.session_state.context = []


# Initialise the GraphRAG Wrapper...
graphrag_client = GraphRAGWrapper()



# Main Chat UI...

with st.chat_message("system"):
	st.write("Welcome to Maki Solicitor GPT.")
	st.write("Make specific questions related to high level retrieval tasks, this is a research tool, not a general chatbot")


# Display chat messages from history on app rerun
for message in st.session_state.messages:
   with st.chat_message(message["role"]):
       st.markdown(message["content"])
       if message.get("context", False):
           for context in message["context"]:
               with st.expander(f"[{context['id']}] {context['title']} (Relevance: {float(context['occurrence_weight']):.2f}) Referenced Ground Truth Document ️🗃️", expanded=False):
                   st.markdown(context['content'])


prompt = st.chat_input("Please enter your prompt here:")

if prompt:
	with st.chat_message("user"):
		st.markdown(prompt)

	st.session_state.messages.append({"role": "user", "content": prompt})

	with st.spinner("Processing your request..."):
		response = graphrag_client.query(prompt)

	with st.chat_message("assistant"):
		st.markdown(response["output"])
		for context in response.get("context", []):
			with st.expander(
					f"[{context['id']}] {context['title']} (Relevance: {float(context['occurrence_weight']):.2f}) Referenced Ground Truth Document ️🗃️",
					expanded=False):
				st.markdown(context['content'])

	# Add output to chat history
	# Save to history
	st.session_state.messages.append({
		"role": "assistant",
		"content": response['output'],
		"context": response.get("context", [])
	})

