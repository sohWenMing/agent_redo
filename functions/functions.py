import os
from enum import Enum
import subprocess
from google.genai import types
class CheckIsSafeType(Enum):
    DIR = "dir"
    WRITEFILE = "file"
    EXEC = "exec"


class PathToIsSafe():
    def __init__(self, path, is_safe, error=None):
        self.path = path 
        self.is_safe = is_safe
        self.error = error



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
    if not is_file_result.is_file:
        return str(is_file_result.error)
    return __read_file_num_bytes(path_to_is_safe.path)

def write_file(working_directory, file_path, content):
    path_to_is_safe = __check_path_safe(working_directory, file_path, checkType=CheckIsSafeType.WRITEFILE)
    if not path_to_is_safe.is_safe:
        return str(path_to_is_safe.error)
    
    complete_path = path_to_is_safe.path
    
    if os.path.exists(complete_path):
        return __try_write_file(complete_path, content)
    
    else:
        file_path_dirname = os.path.dirname(file_path)
        if file_path_dirname != "":
            # if there was actually a prefix dirname, before the actual file 
            full_dir_path = os.path.join(os.path.abspath(working_directory), file_path_dirname)
            if not os.path.exists(full_dir_path):
                # only create the directory if the path does not already exist, if not will throw error
                os.makedirs(os.path.dirname(full_dir_path))
        return __try_write_file(complete_path, content)


def run_python_file(working_directory, file_path, args):

    try:
        path_to_is_safe = __check_path_safe(working_directory, file_path, checkType=CheckIsSafeType.EXEC)

        if not path_to_is_safe.is_safe:
            return str(path_to_is_safe.error)
        if not os.path.exists(path_to_is_safe.path):
            return f'Error: File "{file_path}" not found.'
        if not str.endswith(file_path, ".py"):
            return f'Error:"{file_path} is not a Python file.'
        
        return __run_subprocess_get_output(path_to_is_safe.path)

    except Exception as e:
        return f"Error: executing Python file: {e}"

def completed_process_get_return_string(completed_process, returned_stdout, returned_stderr):
    returned_string = ""
    returned_string += f'STDOUT: {returned_stdout}\n'
    returned_string += f'STDERR: {returned_stderr}\n'

    if completed_process.returncode != 0:
        returned_string += f'Process exited with code {completed_process.returncode}'
        
    if (returned_stdout == "" or returned_stdout == None) and (returned_stderr == "" or returned_stderr == None):
        returned_string += "No output produced"
    return returned_string

    # try:
    #     sub
    # except Exception as e:
    #     return f'Error: executing Python file: {e}'
call_func_name_to_func = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call_part, verbose=False):
    try:
        if verbose:
                print(f"Calling function: function name: {function_call_part.name} args: ({function_call_part.args})")
        else:
                print(f"Calling function: function name: {function_call_part.name}")

        function_name = function_call_part.name 

        if call_func_name_to_func.get(function_name) == None:
            key_val_dict = __create_from_function_content_key_val("error",f"Unknown function: {function_name}")
            return __create_from_function_content(function_name, **key_val_dict)
        elif call_func_name_to_func.get(function_name) == run_python_file:

            result = call_func_name_to_func.get(function_name)("./calculator", 
                                                               function_call_part.args.get("file_path"),
                                                               function_call_part.args.get("args", []))
        else:
            result = call_func_name_to_func.get(function_name)("./calculator", **function_call_part.args)
        key_val_dict = __create_from_function_content_key_val("result",result)
        return __create_from_function_content(function_name, **key_val_dict)
    except Exception as e:
        return __create_from_function_content("unexpected error", **__create_from_function_content_key_val("error", e)
)

########### Private functions ###########
def __run_subprocess_get_output(args):
        completed_process = subprocess.run(args, capture_output=True, timeout=30)

        # args can either be a single string, or a list of strings

        returned_stdout = completed_process.stdout
        returned_stderr = completed_process.stderr

        returned_string = completed_process_get_return_string(completed_process, returned_stdout, returned_stderr)
        return returned_string
        
def __check_path_safe(working_directory, file_path_and_args, checkType=CheckIsSafeType.DIR):

    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        # this will build out an absolute path, starting from /

        if file_path_and_args == None:
            return PathToIsSafe(work_dir_abs_path, True)
        
        if type(file_path_and_args) == str:
            file_path = file_path_and_args
        else:
            file_path = get_file_path_from_file_path_and_args(file_path_and_args)

        if file_path_and_args != None:
            full_path = os.path.join(working_directory, file_path)
            # joins the paths, if there are redundancies will remove
        else:
            full_path = working_directory

        full_abs_path = os.path.abspath(full_path)

        if not full_abs_path.startswith(work_dir_abs_path):
            if checkType==CheckIsSafeType.DIR:
                raise ValueError(f'Error: Cannot list "{file_path_and_args}" as it is outside the permitted working directory')
            elif checkType==CheckIsSafeType.WRITEFILE:
                raise ValueError(f'Error: Cannot write to "{file_path_and_args}" as it is outside the permitted working directory')
            elif checkType==CheckIsSafeType.EXEC:
                raise ValueError(f'Error: Cannot execute "{file_path_and_args}" as it is outside the permitted working directory')
        return PathToIsSafe(full_abs_path, True)

    except Exception as e:
        return PathToIsSafe("", False, e)

def get_file_path_from_file_path_and_args(file_path_and_args):
    file_path = ""
        # init the file path, before evaulation of whether file_path_and_args was a list of a string
    if type(file_path_and_args) == str:
        file_path = file_path_and_args

    elif type(file_path_and_args) == list:
        if len(file_path_and_args) < 1:
            raise ValueError("file_path_and_args passed into __check_path_safe cannot be an empty list")
        file_path = file_path_and_args[0]
        if type(file_path) != str:
            raise TypeError(
                    f'evaluated file_path from from file_path_and_args 0 is of wrong type\n' + 
                    f'type passed in: "{type(file_path_and_args)}"'
                    )
    else:
        raise TypeError(
                f'file_path_and_args passed into __check_path_safe should only be string or list\n' + 
                f'type passed in: "{type(file_path_and_args)}"'
            )
        
    return file_path

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
        def __init__(self, path, is_file, error=None):
            self.path = path 
            self.is_file = is_file
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
        

def __try_write_file(path, content):
    try:
        if os.path.exists(path):
            is_file = __check_is_file(path)
            if not is_file.is_file:
                return str(is_file.error)
        with open(path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error:  {e}'

def __create_from_function_content(function_name, response_key, response_val):
    return types.Content(
        role = "tool",
        parts = [
            types.Part.from_function_response(
                name = function_name,
                response={response_key: response_val}
            )
        ],
    )

def __create_from_function_content_key_val(key, val):
    return {
        "response_key": key,
        "response_val": val
    }