from dotenv import load_dotenv

from langchain_community.tools import DuckDuckGoSearchResults


load_dotenv()

tool = DuckDuckGoSearchResults()

print(tool.invoke("lenskart"))