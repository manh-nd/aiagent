import os
from google.genai import types

def get_files_info(working_directory: str, directory="."):
    abs_cwd = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_path.startswith(abs_cwd):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        items = os.listdir(abs_path)
        files_info = []
        for item in items:
            item_path = os.path.join(abs_path, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            files_info.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        
        content =  "\n".join(files_info)

        if abs_path == abs_cwd:
            return f"Result for current directory:\n{content}"
        else:
            return f"Result for '{directory}' directory:\n{content}"

    except Exception as e:
        return f'Error: Unable to list directory "{directory}": {str(e)}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Defaults to '.' (current working directory).",
            ),
        },
    ),
)

