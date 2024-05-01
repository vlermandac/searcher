from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import StorageContext
from IPython.display import Markdown, display
from pyvis.network import Network
import logging
import os
import sys
from dotenv import load_dotenv


class KnowledgeGraphProcessor:
    def __init__(self):
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        load_dotenv()
        self.OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))
        self.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
        Settings.llm = self.llm
        Settings.chunk_size = 512
        self.documents = SimpleDirectoryReader(
            "../data/processed_files/").load_data()
        self.graph_store = SimpleGraphStore()
        self.storage_context = StorageContext.from_defaults(
            graph_store=self.graph_store)
        self.index = KnowledgeGraphIndex.from_documents(
            self.documents,
            max_triplets_per_chunk=2,
            storage_context=self.storage_context,
        )

    def query_summary(self):
        query_engine = self.index.as_query_engine(
            include_text=True,
            response_mode="tree_summarize",
            embedding_mode="hybrid",
            similarity_top_k=5,
        )
        response = query_engine.query("Make a summary of the story")
        display(Markdown(f"{response}"))

    def display_graph(self):
        g = self.index.get_networkx_graph()
        net = Network(notebook=True, cdn_resources="in_line", directed=True)
        net.from_nx(g)
        net.show("example.html")
