import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory: str, file_path: str):
    abs_cwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_cwd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read(MAX_CHARS)  # Read up to 10,000 characters
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                content += f'[...[File "{file_path}" truncated at {MAX_CHARS} characters]'
            return f'Content of "{file_path}":\n{content}'
    except Exception as e:
        return f'Error: Unable to read file "{file_path}": {str(e)}'
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)