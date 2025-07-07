import os

def write_file(working_directory, file_path, content):

    temp_file_path = os.path.join(working_directory, file_path)

    abs_file_path = os.path.abspath(temp_file_path)
    abs_working_dir = os.path.abspath(working_directory)

    if abs_file_path.startswith(abs_working_dir):
        
        with open(abs_file_path, "w") as f:
            f.write(content)
        
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"

    else:
        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"