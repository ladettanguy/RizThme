import os
import importlib

PREFIX = '!'

# Set up a dictionary with key, value = Command's name, function's command
commands = {}
os.chdir(f"{os.path.split(__file__)[0]}")
list_file = os.listdir('.')
list_file.remove('__init__.py')
list_file.remove('__pycache__')
for filename in list_file:
    module_name = filename.split('.')[0]
    cmd_file = importlib.import_module(f'commands.{module_name}')
    cmd = getattr(cmd_file, module_name)
    commands[module_name] = cmd
os.chdir('..')
