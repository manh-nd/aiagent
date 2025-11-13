import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_cwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_cwd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ["python3", abs_file_path] + args
        result = subprocess.run(
            command, 
            timeout=30,
            capture_output=True,
            text=True, 
            cwd=working_directory
        )
        
        return f"""
STDOUT: {result.stdout}
STDERR: {result.stderr}
Exit Code: {"Process exited with code " + str(result.returncode) if result.returncode != 0 else "0"}
{"No output produced." if not result.stdout and not result.stderr else ""}
"""
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python script.",
            ),
        },
        required=["file_path"],
    ),
)