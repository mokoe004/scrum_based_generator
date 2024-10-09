from pydantic import BaseModel, Field, model_validator

# class Item(BaseModel):
#     """"""

#     directory: dict = Field(description="Subdirectory of the project.")
#     file: str = Field(description="File of the project. e.g. 'main.py'")

#     @model_validator
#     def check_either_directory_or_file(cls, values):
#         directory, file = values.get('directory'), values.get('file')
#         if directory and file:
#             raise ValueError("Either 'directory' or 'file' must be specified.")
#         if not directory and not file:
#             raise ValueError("Either 'directory' or 'file' must be specified.")
#         return values


# class PackageDesignModel(BaseModel):

#     directory: dict = Field(None, description="Subdirectory of the project.")
#     file: File = Field(str, description="File of the project.  ")

class CodeModel(BaseModel):
    """Base model for a code project."""

    project: dict = Field(description="The project with all classes and generates files. Structure like package_design.")