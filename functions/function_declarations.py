from google.genai import types 

def declare_genai_function(name, description, parameters):
    return types.FunctionDeclaration(
        name=name,
        description=description,
        parameters = parameters

        #parameters should take in a type genai.types.Schema, which it self can be defined as an object through genai.type.Object
    )

schema_get_files_info = declare_genai_function("get_files_info",
                                               "Lists files in the specified directory along with their sizes," +
                                               " constrained to the working directory.",
                                               types.Schema(
                                                   type=types.Type.OBJECT,
                                                   properties={
                                                       "directory": types.Schema(
                                                           type=types.Type.STRING,
                                                           description="The directory to list files from, " +
                                                           "relative to the working directory. " + 
                                                           "If not provided, lists files in the working directory itself."
                                                       )
                                                   }
                                               ))
"""
In this examples of a function declaration: 
1. We have declared the name of the function as get_files_info
2. The description has been declared, which lets the LLM know what the function does, so that it can decide whether it should
    be calling the function or not based on the prompt
3. We've declared the PARAMETERS of of the function as types.Schema
    we've set that the PARAMETERS type is of types.Type.OBJECT - this is based of an ENUM of types from the SDK

        We then set the properties of the parameters to be a json like structure

        properties = {
            "directory (string)": <the description we've listed above> 
        }
"""
schema_get_file_content = declare_genai_function("get_file_content",
                                               "Read file content",
                                               types.Schema(
                                                   type=types.Type.OBJECT,
                                                   properties={
                                                       "file_path": types.Schema(
                                                           type=types.Type.STRING,
                                                           description="The file from which to read information" 
                                                       )
                                                   }
                                               ))

schema_run_python_file = declare_genai_function("run_python_file",
                                               "Execute the code within a python file",
                                               types.Schema(
                                                   type=types.Type.OBJECT,
                                                   properties={
                                                       "file_path": types.Schema(
                                                           type=types.Type.STRING,
                                                           description="The file that contains the code which needs to be executed" 
                                                       ),
                                                       "args": types.Schema(
                                                           type=types.Type.ARRAY,
                                                           items=types.Schema(type=types.Type.STRING),
                                                           description="The optional arguments that can be passed when running a python file"
                                                       )
                                                   }
                                               ))
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file
    ]
)