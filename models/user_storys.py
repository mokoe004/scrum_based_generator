from typing import List
from pydantic import BaseModel, Field


class UserStoryModel(BaseModel):
    """Represents a user story with a persona, goal, and benefit."""

    title: str = Field(description="The title of the user story")
    story: str = Field(
        description="The detailed user story in the format 'As a [Persona], I want to [Goal], so that [Benefit].'"
    )


class EpicModel(BaseModel):
    """Represents an epic containing a set of user stories."""

    name: str = Field(description="The name of the epic")
    description: str = Field(description="A brief description of the epic")
    business_value: str = Field(description="The business value or impact of the epic")
    user_stories: List[UserStoryModel] = Field(
        description="A list of user stories associated with this epic"
    )


class EpicListModel(BaseModel):
    """Represents a list of epics."""

    epics: List[EpicModel] = Field(
        description="A list of epics, each containing user stories"
    )


class PersonaModel(BaseModel):
    """Represents a persona with personal and professional details."""

    name: str = Field(description="The full name of the persona")
    age: int = Field(description="The age of the persona in years")
    occupation: str = Field(description="The job title or profession of the persona")
    background: str = Field(
        description="The background story or history of the persona"
    )
    motivation: str = Field(description="What drives or motivates the persona")
    goal: str = Field(description="The main goal the persona wants to achieve")


class PersonaListModel(BaseModel):
    """A list of personas, each representing an individual with specific characteristics."""

    personas: List[PersonaModel] = Field(description="A list of persona objects")
