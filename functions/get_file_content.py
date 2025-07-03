import os

def get_file_content(working_directory, file_path=None):

    if file_path == None:
        return "Error: no file inputed"
    else:
        full_file_path = os.path.join(working_directory, file_path)

    abs_file_path = os.path.abspath(full_file_path)
    abs_working_dir = os.path.abspath(working_directory)

    if abs_file_path.startswith(abs_working_dir):
        if os.path.isfile(abs_file_path):

            with open(abs_file_path, "r") as f:
                file_content = f.read()
            
            if len(file_content) > 10000:
                return f"{file_content}[...File \"{file_path}\" truncated at 10000 characters]"
            else:
                return file_content

        else:
            return f"Error: File not found or is not a regular file: \"{file_path}\""

    else:
        return f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory"
    