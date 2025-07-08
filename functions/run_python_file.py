import os
import subprocess

def run_python_file(working_directory, file_path):

    temp_file_path = os.path.join(working_directory, file_path)

    abs_file_path = os.path.abspath(temp_file_path)
    abs_working_file_path = os.path.abspath(working_directory)

    if abs_file_path.startswith(abs_working_file_path):
        
        if os.path.exists(abs_file_path):

            if abs_file_path[-3:] == '.py':

                try:
                    run_code = subprocess.run(["uv", "run", abs_file_path],
                                              timeout = 30,
                                              capture_output=True)
                    if run_code.stdout != '' and run_code.stderr != '':
                    
                        if run_code.returncode == 0:
                            return f"STDOUT: {run_code.stdout}\nSTDERR: {run_code.stderr}"

                        else:
                            return f"Process exited with code {run_code.returncode}"

                    else:
                        return "No output produced."
                
                except Exception as e:
                    return f"Error: executing Python file: {e}"

            else:
                return f"Error: \"{file_path}\" is not a Python file."

        else:
            return f"Error: File \"{file_path}\" not found."

    else:
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    