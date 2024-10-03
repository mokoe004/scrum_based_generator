import getpass
import os, json
from typing import List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field

model = ChatGoogleGenerativeAI(
    model = "gemini-1.5-pro", 
    api_key=os.environ.get("GOOGLE_API_KEY")
    )

# from langchain_core.messages import HumanMessage, SystemMessage
# messages = [
#     SystemMessage(content="Translate the following from English into Italian"),
#     HumanMessage(content="hi!"),
# ]

# Pydantic
class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )
parser = JsonOutputParser(pydantic_object = Joke)

class PersonaModel(BaseModel):
    """Represents a persona with personal and professional details."""

    name: str = Field(description="The full name of the persona")
    age: int = Field(description="The age of the persona in years")
    occupation: str = Field(description="The job title or profession of the persona")
    background: str = Field(description="The background story or history of the persona")
    motivation: str = Field(description="What drives or motivates the persona")
    goal: str = Field(description="The main goal the persona wants to achieve")

# Definiere ein Modell, das eine Liste von PersonaModel-Objekten enthält
class PersonaListModel(BaseModel):
    """A list of personas, each representing an individual with specific characteristics."""

    personas: List[PersonaModel] = Field(description="A list of persona objects")

parser = JsonOutputParser(pydantic_object = PersonaListModel)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
#Chain the model and parser together
chain = prompt | model | parser
#print(chain.invoke(messages))

output = chain.invoke({"query": "Generate example personas for a marketing campaign"})
print(output)
#print(chain.invoke("Tell me a joke about cats"))


#model = model.with_structured_output(PersonaListModel)
#out = model.invoke("Generate example personas for a marketing campaign")
#print(out.tool_calls)
#output = chain.invoke("Generate example personas for a marketing campaign")
#print(output)
#print(json.loads(output))