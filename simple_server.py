# pip install gunicorn
# flask
# graphrag
import os, flask

# Alot of it is just CLI aspects so is easy to test and understand...

# This is GraphRAG, if you cannot answer using this, we are not able to answer anything...
# https://microsoft.github.io/graphrag/get_started/


# md ".\ragtest\input"
# wget "https://www.gutenberg.org/cache/epub/24022/pg24022.txt" -O ".\ragtest\input\book.txt"
# graphrag init --root ./ragtest


# Run Pipeline,

# graphrag index --root ./ragtest


# Query Engine (Global)
# graphrag query --root ./nucourt --method global --query "What are the top themes in this story?"


# Query Engine (Local)
# graphrag query \
# --root ./ragtest \
# --method local \
# --query "Who is Scrooge and what are his main relationships?"


# Visualisation of Graph,
# https://microsoft.github.io/graphrag/visualization_guide/


from flask import Flask, jsonify
import subprocess
import re

app = Flask(__name__)


def extract_response(output):
    """Extract text after 'SUCCESS:' from command output"""
    success_match = re.search(r'SUCCESS:(.*)', output, re.DOTALL)
    if success_match:
        return success_match.group(1).strip()
    return None


def run_graphrag_query():
    """Execute graphrag query command and extract response"""
    cmd = ['graphrag', 'query', '--root', './nucourt', '--method', 'global',
           '--query', "Please mention the list out the events in chronological order"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            response = extract_response(result.stdout)
            if response:
                return {"success": True, "response": response}
        return {"success": False, "error": "No SUCCESS message found in output"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.route('/run', methods=['GET'])
def run_endpoint():
    result = run_graphrag_query()
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)