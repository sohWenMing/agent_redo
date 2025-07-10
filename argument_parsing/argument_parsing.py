import sys

def get_arg_from_sys_argv():
    args = sys.argv
    return get_argument(args)

def get_argument(argv):
    if len(argv) < 2:
        raise ValueError("program should have minimum 2 arguments, with the second being the prompt")
    return argv[1]



