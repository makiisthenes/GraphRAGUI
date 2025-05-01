# This function will be used to run the GraphRAG query and return the response to the user,

import networkx as nx
import pandas as pd
import tiktoken
import os
from graphrag.query.context_builder.conversation_history import ConversationRole, ConversationTurn, ConversationHistory
from graphrag.query.indexer_adapters import (
	read_indexer_communities,
	read_indexer_entities,
	read_indexer_reports,
)
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.global_search.community_context import (
	GlobalCommunityContext,
)
from graphrag.query.structured_search.global_search.search import GlobalSearch
from dotenv import load_dotenv
from enum import Enum

# Load environmental variables
load_dotenv()


class SearchType(Enum):
	GLOBAL = "global"
	LOCAL = "local"


# Load the GraphRAG API key and LLM model
api_key = os.environ["GRAPHRAG_API_KEY"]
llm_model = os.environ["GRAPHRAG_LLM_MODEL"]

llm = ChatOpenAI(
	api_key=api_key,
	model=llm_model,
	api_type=OpenaiApiType.OpenAI,  # OpenaiApiType.OpenAI or OpenaiApiType.AzureOpenAI
	max_retries=20,
)
token_encoder = tiktoken.encoding_for_model(llm_model)
# parquet files generated from indexing pipeline
INPUT_DIR = "nucourt/input"
OUTPUT_DIR = "nucourt/output"
COMMUNITY_TABLE = "create_final_communities"
COMMUNITY_REPORT_TABLE = "create_final_community_reports"
ENTITY_TABLE = "create_final_nodes"
ENTITY_EMBEDDING_TABLE = "create_final_entities"
# community level in the Leiden community hierarchy from which we will load the community reports
# higher value means we use reports from more fine-grained communities (at the cost of higher computation cost)
COMMUNITY_LEVEL = 2

context_builder_params = {
	"use_community_summary": False,
	# False means using full community reports. True means using community short summaries.
	"shuffle_data": True,
	"include_community_rank": True,
	"min_community_rank": 0,
	"community_rank_name": "rank",
	"include_community_weight": True,
	"community_weight_name": "occurrence weight",
	"normalize_community_weight": True,
	"max_tokens": 12_000,
	"context_name": "Reports",
}

map_llm_params = {
	"max_tokens": 1000,
	"temperature": 0.0,
	"response_format": {"type": "json_object"},
}

reduce_llm_params = {
	"max_tokens": 2000,
	"temperature": 0.0,
}


class GraphRAGWrapper:
	def __init__(self):
		self.community_df = pd.read_parquet(f"{OUTPUT_DIR}/{COMMUNITY_TABLE}.parquet")
		self.entity_df = pd.read_parquet(f"{OUTPUT_DIR}/{ENTITY_TABLE}.parquet")
		self.report_df = pd.read_parquet(f"{OUTPUT_DIR}/{COMMUNITY_REPORT_TABLE}.parquet")
		self.entity_embedding_df = pd.read_parquet(f"{OUTPUT_DIR}/{ENTITY_EMBEDDING_TABLE}.parquet")
		self.communities = read_indexer_communities(self.community_df, self.entity_df, self.report_df)
		self.reports = read_indexer_reports(self.report_df, self.entity_df, COMMUNITY_LEVEL)
		self.entities = read_indexer_entities(self.entity_df, self.entity_embedding_df, COMMUNITY_LEVEL)
		self.context_builder = GlobalCommunityContext(
			community_reports=self.reports,
			communities=self.communities,
			entities=self.entities,  # default to None if you don't want to use community weights for ranking
			token_encoder=token_encoder,
		)
		# Initialise a conversation history...
		self.conversation_history = ConversationHistory()

	def query(self, prompt: str, search_type: SearchType = SearchType.GLOBAL):
		search_engine = None
		if search_type == SearchType.GLOBAL:
			search_engine = GlobalSearch(
				llm=llm,
				context_builder=self.context_builder,
				token_encoder=token_encoder,
				max_data_tokens=50_000,
				map_llm_params=map_llm_params,
				reduce_llm_params=reduce_llm_params,
				allow_general_knowledge=True,
				json_mode=True,
				context_builder_params=context_builder_params,
				concurrent_coroutines=32,
				response_type="multiple paragraphs",
				# free form text describing the response type and format, can be anything, e.g. prioritized list, single paragraph, multiple paragraphs, multiple-page report
			)
		else:
			raise NotImplementedError("Local search is not implemented yet.")

		result = search_engine.search(
			query=prompt,
			conversation_history=self.conversation_history,
		)
		# Add turn to search engine,
		self.conversation_history.add_turn(role=ConversationRole.USER, content=prompt)

		self.conversation_history.add_turn(role=ConversationRole.ASSISTANT, content=result.response)

		context = []
		for index, context_elem in enumerate(result.context_text):
			if index == 0: continue
			rows= context_elem.split('\r')
			for row in rows:
				elements = row.replace("\n", "").split("|")
				if len(elements) < 4:
					continue
				if elements[0] == "id" or elements[2] == "occurrence weight":
					continue
				context.append({
					"id": elements[0],
					"title": elements[1],
					"occurrence_weight": elements[2],
					"content": elements[3],
					"rank": elements[4],
				})

		return {
			"output": result.response,
			"context": context,
		}

	def __del__(self):
		# print("Object is being destroyed and resources are being released.")
		# Save the history of the conversation to a file...
		pass


	def get_knowledge_graph(self):
		return nx.read_graphml(f"{OUTPUT_DIR}/graph.graphml")