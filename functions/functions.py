import os
from config import agent_config

def get_files_info(working_directory, directory=None):
    path_to_is_safe = __check_path_safe(working_directory, directory)

    if not path_to_is_safe.is_safe:
        return str(path_to_is_safe.error)
        
    is_dir = __check_is_dir(path_to_is_safe.path)
    if not is_dir:
        return f'Error: "{directory}" is not a directory'

    else:
        return __list_dir_entries(path_to_is_safe.path)

def get_file_content(working_directory, file_path):
    path_to_is_safe = __check_path_safe(working_directory, file_path)

    if not path_to_is_safe.is_safe:
        return str(path_to_is_safe.error)
    
    is_file_result = __check_is_file(path_to_is_safe.path)
    if not is_file_result.is_safe:
        return str(is_file_result.error)
    return __read_file_num_bytes(path_to_is_safe.path, num_bytes=agent_config.max_chars)

 
########### Private functions ###########
def __check_path_safe(working_directory, directory):
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

def __check_is_dir(path):
    if not os.path.isdir(path):
        return False
    return True
   
def __list_dir_entries(path):
    entries = os.listdir(path)
    return_string = "Results for current directory:\n"
    for entry in entries:
        full_path = os.path.join(path, entry)
        return_string += __map_entry(full_path)
    return return_string

def __map_entry(entry):
    is_dir = os.path.isdir(entry)
    file_size = os.path.getsize(entry)
    base_name = os.path.basename(entry)
    return f"{base_name}: file_size={file_size}, is_dir={is_dir}\n"

def __check_is_file(file_path):
    class IsFileResult():
        def __init__(self, path, is_safe, error=None):
            self.path = path 
            self.is_safe = is_safe
            self.error = error
    try:
        if os.path.isfile(file_path):
            return IsFileResult(
                file_path,
                True, 
                None
            )
        else:
            raise ValueError( f'Error: File not found or is not a regular file: "{os.path.basename(file_path)}"')
        
    except Exception as e:
        return IsFileResult(
            None,
            False,
            ValueError(e),
        )

def __read_file_num_bytes(file_path, num_bytes=10000, mode="r"):
    try:
        with open(file_path, mode) as file:
            data = file.read()
            if len(data) > num_bytes:
                truc_data = data[:num_bytes]
                return str(f'{truc_data}[...File "{file_path}" truncated at {num_bytes} characters]')
            else:
                return str(data)
    except Exception as e:
        return f'Error: "{e}"'
        



