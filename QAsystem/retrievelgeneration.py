from haystack.utils import Secret
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.retrievers.pinecone import (
    PineconeEmbeddingRetriever,
)
from haystack_integrations.components.generators.google_ai import GoogleAIGeminiGenerator
from haystack import Pipeline
import os
from dotenv import load_dotenv
from QAsystem.utils import pinecone_config
prompt_template = """You are a **Hotel's Virtual Assistant**. Your task is to answer the user's query based on the provided context. Follow these guidelines:

1. **Refine the Output**:
   - Extract only the relevant information from the context.
   - Structure and organize the answer in a clear and concise manner.
   - Format the text for better understanding and also use bulletpoints and consider bolding the letters if needed.

2. **Response Format**:
   - If the context contains the answer, provide it in a structured format (e.g., bullet points or short paragraphs).
   - If the context does not include an answer, reply with: "I don't know."

3. **Tone**:
   - Maintain a professional and friendly tone, as expected from a hotel receptionist.

4. **Query**:
   - User Query: {{query}}

5. **Context**:
   - Documents:
     {% for doc in documents %}
       {{ doc.content }}
     {% endfor %}

6. **Answer**:
   - Provide the refined and structured answer here.
"""

load_dotenv()
gemini_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = gemini_key

def get_result(query: str):
    query_pipeline = Pipeline()

    query_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder())
    query_pipeline.add_component("retriever", PineconeEmbeddingRetriever(document_store=pinecone_config()))
    query_pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
    query_pipeline.add_component("llm",GoogleAIGeminiGenerator(model="gemini-2.0-flash"))

    query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    query_pipeline.connect("retriever.documents", "prompt_builder.documents")
    query_pipeline.connect("prompt_builder", "llm")

    query = query

    results = query_pipeline.run(
        {
            "text_embedder": {"text": query},
            "prompt_builder": {"query": query},
        }
    )

    return results['llm']['replies'][0]

if __name__ == "__main__":
    #loading the environment variable
    '''load_dotenv()
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
    
    print("Import Successfully")'''
    
    result=get_result("What are the services the hotel offering?")
    print(result)