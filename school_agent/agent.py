from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Load secrets
openai_api_key = os.getenv("OPENAI_API_KEY")
database_url = os.getenv("DATABASE_URL")

# Set up LLM
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

# Connect to PostgreSQL
db = SQLDatabase.from_uri(database_url)

# Set up SQL agent
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True
)

# Example function to use the agent
def ask_sql_agent(question: str):
    return agent_executor.run(question)
