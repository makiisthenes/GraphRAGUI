# GraphRAG Webapp
import traceback, time, requests, pathlib, os, sys
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st


# Load environmental variables...
load_dotenv()
CURRENT_DIR = pathlib.Path(__file__).parent.resolve()


# Set config of website...
st.set_page_config(
	page_title="GraphRAG Experimental Solicitor GPT",
	page_icon="🧊",
	layout="wide",
	initial_sidebar_state="expanded",
)

# Set logo.
st.logo(str(os.path.join(CURRENT_DIR, "static",  "logo-dark.png")), link="https://sellin.one")


def main_app():
	st.header("GraphRAG Experimental Solicitor GPT")
	st.markdown("Developed by Michael P, experimental RAG systems based on Microsoft GraphRag Nov 2024.")
	st.markdown("----")


pg = st.navigation({
	"Start":
		[
			st.Page(main_app, title="Home", icon="🏠", url_path="/"),
		],
	"Chat": [
		st.Page("view_pages/chat.py", title="Chat", icon="💬", url_path="/chat"),
		st.Page("view_pages/add_files.py", title="Add New Files", icon="📁", url_path="/add_files"),
	],
	"Insights": [
		st.Page("view_pages/graph_viewer.py", title="Graph Viewer", icon="📊", url_path="/graph"),
		st.Page("view_pages/context.py", title="Context Documents", icon="📚", url_path="/context"),
	]
})
# Page Navigation



# Run the application.
try:
	pg.run()
except Exception as e:
	error_details = traceback.format_exc()
	st.error(f"MAIN APP: An error occurred: {str(e)} \n {error_details}")