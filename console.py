#!/usr/bin/python

from os import system
from error_code_table import error_decode as edecode
from sys import exit

cls = lambda: system('cls')
clear = lambda: system('clear')

def clr():
    """Use in console command handlers to clear the screen, if needed."""
    cls()
    clear()

def grab_command(help_string, function_command_dict):
    """Prompt a user for a command, given a dict defining commands and their corresponding handler function"""
    while True:
        # Prompt user for input and store it.
        full_command = input("> ")


        args = full_command.split(" ")
        cmd = args.pop(0)
        
        # Handle the special case of the help command, as it doesn't need to call any external functions
        if (cmd.lower() == "help"):
            print(help_string)
            continue
        
        if (cmd.lower() == "exit"):
            print("Goodbye!")
            exit(0)

        if not function_command_dict.get(cmd.lower(), False):
            print("Invalid action!")
            continue
        
        
        return_code = function_command_dict[cmd.lower()](args)
        if not return_code[0]:
            print("Invalid action: {}".format(edecode[return_code[1]]))
        return
