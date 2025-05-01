import streamlit as st
import os
from pathlib import Path


def view_context_files():
	st.title("Context Files Viewer")
	st.markdown("These are all the files that are being used as context...")

	# Get input directory path
	input_dir = Path("./nucourt/input")

	if not input_dir.exists():
		st.error(f"Directory not found: {input_dir}")
		return

	# List files
	files = list(input_dir.glob('*'))

	for file in files:
		with st.expander(f"📄 {file.name}", expanded=False):
			try:
				first_line = file.read_text(encoding='utf-8').split('\n')[0]
				st.text(first_line)
			except Exception as e:
				st.error(f"Error reading file: {str(e)}")



view_context_files()