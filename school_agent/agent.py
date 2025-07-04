from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_community.agent_toolkits import GmailToolkit 
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

# Load secrets
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
database_url = os.getenv("DATABASE_URL")

# Set up Google credentials
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)

# Set up LLM
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

# Connect to PostgreSQL
db = SQLDatabase.from_uri(database_url)

# Initialize Gmail and SQL toolkits
google_toolkit = GmailToolkit(api_resource=api_resource)
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = google_toolkit.get_tools() + sql_toolkit.get_tools()

# Create agent with memory saver
memory = MemorySaver()
config = {"configurable": {"thread_id": "abc123"}}
agent = create_react_agent(llm, tools, checkpointer=memory)

# Execute query using the agent
def execute_query(query: str):
    try:
        input_message = {"role": "user", "content": query}
        response = agent.invoke({"messages": [input_message]}, config=config)

        for message in response["messages"]:
            message.pretty_print()
        return response["messages"][-1]
    except Exception as e:
        return {"error": str(e)}
