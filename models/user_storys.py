from pydantic import BaseModel, Field, RootModel
from typing import List

class PersonaModel(BaseModel):
    """Represents a persona with personal and professional details."""

    name: str = Field(description="The full name of the persona")
    age: int = Field(description="The age of the persona in years")
    occupation: str = Field(description="The job title or profession of the persona")
    background: str = Field(description="The background story or history of the persona")
    motivation: str = Field(description="What drives or motivates the persona")
    goal: str = Field(description="The main goal the persona wants to achieve")

class PersonaListModel(BaseModel):
    """Represents a list of personas."""

    personas: List[PersonaModel] = Field(
        description="A list of personas, each containing a name, age, occupation, background, motivation, and goal"
    )

class UserStoryModel(BaseModel):
    """Represents a user story with a title, persona, and a story containing of a goal, and a benefit."""

    title: str = Field(description="A short title of the story")
    story: str = Field(
        description="The detailed user story in the format 'As a [persona], I want to [Goal], so that [Benefit].'"
    )
    persona: PersonaModel = Field(description="The persona associated with the story")
class UserStoryListModel(BaseModel):
    """Represents a list of user stories."""

    user_stories: List[UserStoryModel] = Field(
        description="A list of user stories, each containing a title, story, and persona"
    )

class AcceptanceCriteriaModel(BaseModel):
    """Represents a list of acceptance criteria for a user story."""

    acceptance_criteria: List[str] = Field(
        description="A list of acceptance criteria for a user story"
    )

class TasksModel(BaseModel):
    """Represents a list of tasks for a user story."""

    tasks: List[str] = Field(description="A list of tasks for a user story")

class EpicModel(BaseModel):
    """Represents an epic containing a set of user_stories."""

    name: str = Field(description="The name of the epic")
    description: str = Field(description="A brief description of the epic")
    business_value: str = Field(description="The business_value or impact of the epic")
class EpicListModel(BaseModel):
    """Represents a list of epics."""

    epics: List[EpicModel] = Field(
        description="A list of epics, each containing a name, description, and business_value"
    )

