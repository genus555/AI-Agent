import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def pass_dir_contents_to_print(dir):
    dir_contents = os.listdir(dir)
    print_lines = []
    for content in dir_contents:
        print_lines.append(print_contents(dir, content))
    return '\n'.join(print_lines)

def print_contents(dir_path, dir_content):
    content_path = os.path.join(dir_path, dir_content)
    content_size = os.path.getsize(content_path)
    is_dir = os.path.isdir(content_path)
    return f"{dir_content}: file_size={content_size} bytes, is_dir={is_dir}"

def get_files_info(working_directory, directory=None):

    if directory != None:
        file_path = os.path.join(working_directory, directory)
    else:
        file_path = working_directory
    
    abs_file_path = os.path.abspath(file_path)
    abs_working_dir = os.path.abspath(working_directory)
    if abs_file_path.startswith(abs_working_dir):
        
        if os.path.isdir(abs_file_path):
            output = pass_dir_contents_to_print(abs_file_path)
            return output
        
        else:
            return f"Error: \"{directory}\" is not a directory"
    
    else:
        return f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory"
    