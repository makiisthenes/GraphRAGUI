# GraphRAG Experimental Solicitor GPT

This repository contains an experimental Retrieval-Augmented Generation (RAG) system using Microsoft's GraphRAG technology. The app provides structured analysis of relational queries and is demonstrated through a user-friendly Streamlit interface.

## Overview

GraphRAG enhances AI accuracy and reduces hallucinations by leveraging structured relational queries across unstructured data. This setup is ideal for scenarios requiring deep, interconnected data insights.

## Requirements

- Python 3.8 or higher
- pip

## Installation

Clone this repository:

```bash
git clone <your_repository_url>
cd GraphRAGServer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure you have the following installed:

```bash
pip install gunicorn flask graphrag streamlit
```

## Initial Setup

Create your input directory and initialize GraphRAG:

```bash
mkdir ./output_dir/input
# Place your text files into this directory

# Initialize GraphRAG
graphrag init --root ./output_dir
```

## Indexing Data

Run the indexing pipeline to prepare your data for queries:

```bash
graphrag index --root ./output_dir
```

## Running the Application

Launch the Streamlit app:

```bash
streamlit run app.py
```

Access the app through your browser at `http://localhost:8501`.

## Querying via CLI

You can also perform queries directly via CLI:

```bash
graphrag query --root ./nucourt --method global --query "Your query here"
```

## Graph Visualization

For visualization of your GraphRAG structure, see:

- [Microsoft GraphRAG Visualization Guide](https://microsoft.github.io/graphrag/visualization_guide/)

## Project Structure

```
GraphRAGServer/
├── export/
├── lib/
├── nucourt/
├── save_folder/
├── static/
├── view_pages/
│   ├── add_files.py
│   ├── chat.py
│   ├── context.py
│   └── graph_viewer.py
├── .dist.env
├── .env
├── Dockerfile
├── GraphRAGWrapper.py
├── app.py
├── requirements.txt
└── utils.py
```

## Additional Resources

This could have potential as a GraphRAG MVP, offering flexibility across multiple use-cases.

- [Microsoft GraphRAG Global Search Example](https://microsoft.github.io/graphrag/examples_notebooks/global_search/#perform-global-search)
- [Microsoft GraphRAG Visualization Guide](https://microsoft.github.io/graphrag/visualization_guide/)
- [Microsoft GraphRAG GitHub Repository](https://github.com/microsoft/graphrag)
- [GraphRAG Research Paper (arXiv)](https://arxiv.org/pdf/2404.16130)


## Contributions

Feedback and contributions are very welcome!

