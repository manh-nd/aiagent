import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str):
    abs_cwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_cwd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        dir_name = os.path.dirname(abs_file_path)
        os.makedirs(dir_name, exist_ok=True)

        with open(abs_file_path, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Unable to write to file "{file_path}": {str(e)}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)