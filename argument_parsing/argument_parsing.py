import sys
import argparse

def get_arg_from_sys_argv():
    args = sys.argv
    return get_prompt(args)

def get_prompt(argv):
    if len(argv) < 2:
        raise ValueError("program should have minimum 2 arguments, with the second being the prompt")
    return argv[1]

def check_verbose_flag():
    argv = sys.argv
    if len(argv) < 3:
        return False 
    return argv[2] == "--verbose"

###### argument parser for flags #####

def parse_flags():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", 
                        action="store_true",
                        help="determines whether or not program is run in verbose mode")
    args = parser.parse_args()

    is_verbose = False

    if args.verbose == True:
        print("program has started in verbose mode")
        is_verbose = True
    return {
        "is_verbose": is_verbose
    }