import os

def get_files_info(working_directory, directory=None):
    path_to_is_safe = check_dir_safe(working_directory, directory)

    if not path_to_is_safe.is_safe:
        return str(path_to_is_safe.error)
        
    is_dir = check_is_dir(path_to_is_safe.path)
    if not is_dir:
        return f'Error: "{directory}" is not a directory'

    else:
        return list_dir_entries(path_to_is_safe.path)

"""
if the directory is outside the current working directory, then it should throw an error (but as a string, so the LLM can read it)
"""

def check_dir_safe(working_directory, directory):
    class PathToIsSafe():
        def __init__(self, path, is_safe, error=None):
            self.path = path 
            self.is_safe = is_safe
            self.error = error

    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        # this will build out an absolute path, starting from /

        if directory != None:
            full_path = os.path.join(working_directory, directory)
            # joins the paths, if there are redundancies will remove
        else:
            full_path = working_directory

        full_abs_path = os.path.abspath(full_path)

        if not full_abs_path.startswith(work_dir_abs_path):
           raise ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return PathToIsSafe(full_abs_path, True)

    except Exception as e:
        return PathToIsSafe("", False, e)

def check_is_dir(path):
    if not os.path.isdir(path):
        return False
    return True
   
def list_dir_entries(path):
    entries = os.listdir(path)
    return_string = "Results for current directory:\n"
    for entry in entries:
        full_path = os.path.join(path, entry)
        return_string += map_entry(full_path)
    return return_string

def map_entry(entry):
    is_dir = os.path.isdir(entry)
    file_size = os.path.getsize(entry)
    base_name = os.path.basename(entry)
    return f"{base_name}: file_size={file_size}, is_dir={is_dir}\n"




