from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI


from decouple import Config
config = Config(".env")
openai_api_key = config("OPENAI_API_KEY")

graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="your_password")

# graph.query(
#     """
# MERGE (m:Movie {name:"Top Gun", runtime: 120})
# WITH m
# UNWIND ["Tom Cruise", "Val Kilmer", "Anthony Edwards", "Meg Ryan"] AS actor
# MERGE (a:Actor {name:actor})
# MERGE (a)-[:ACTED_IN]->(m)
# """
# )

graph.query(
    """
    MERGE (m:Movie {name:"Top Gun", runtime: 120})
    WITH m
    UNWIND [
      {name: "Tom Cruise", gender: "Male"},
      {name: "Val Kilmer", gender: "Male"},
      {name: "Anthony Edwards", gender: "Male"},
      {name: "Meg Ryan", gender: "Female"}
    ] AS actorData
    MERGE (a:Actor {name: actorData.name})
    SET a.gender = actorData.gender
    MERGE (a)-[:ACTED_IN]->(m)
    """
)

graph.refresh_schema()

print(graph.schema)

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0,  openai_api_key=openai_api_key),
    graph=graph, 
    verbose=True,
    allow_dangerous_requests=True
)

# chain.invoke({"query": "Who played in Top Gun?"})
# chain.invoke({"query": "What is the gender of Meg Ryan"})
# chain.invoke({"query": "Who is a female in Top Gun ?"}) # not working

chain2 = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0,  openai_api_key=openai_api_key),
    graph=graph, 
    verbose=True,
    allow_dangerous_requests=True,
    return_intermediate_steps=True
)

result2 = chain2.invoke({"query": "Hown many people played in Top Gun?"})
print(f"Intermediate steps: {result2['intermediate_steps']}")
print(f"Final answer: {result2['result']}")

# Add examples in the Cypher generation prompt

from langchain_core.prompts.prompt import PromptTemplate

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Examples: Here are a few examples of generated Cypher statements for particular questions:
# How many people played in Top Gun?
MATCH (m:Movie {{name:"Top Gun"}})<-[:ACTED_IN]-()
RETURN count(*) AS numberOfActors

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

chain3 = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0,  openai_api_key=openai_api_key),
    graph=graph, 
    verbose=True,
    allow_dangerous_requests=True,
    cypher_prompt=CYPHER_GENERATION_PROMPT,
)

result3 = chain3.invoke({"query": "How many people played in Top Gun?"})
print(f"Final answer: {result3['result']}")