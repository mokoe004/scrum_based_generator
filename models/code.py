from pydantic import BaseModel, Field

class PackageModel(BaseModel):
    """Base model for a code project."""

    controllers: dict = Field(description="Controllers of the project.")
    models: dict = Field(description="Models of the project.")
    views: dict = Field(description="Views of the project.")
    database: dict = Field(description="Database of the project.")
    public: dict = Field(description="Public files of the project, categorized by type (e.g., css, js).")
    routes: dict = Field(description="Routes of the project.")
    root_files: dict[str, str] = Field(description="Files located at the root of the project.")

class TestsModel(BaseModel):
    """Base model for tests of a code project."""

    unit_tests: dict = Field(description="Unit tests of the project.")
    integration_tests: dict = Field(description="Integration tests of the project.")