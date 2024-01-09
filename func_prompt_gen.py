import os
import glob
import importlib.util
import inspect
import textwrap

def generate_config():
    config_content = "RAVEN_PROMPT = \\\n'''\n"

    # List all .py files in the 'modules' directory
    module_files = glob.glob('modules/*.py')

    for file_path in module_files:
        # Dynamically import the module
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Extract functions and their docstrings
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj):
                docstring = inspect.getdoc(obj)
                if docstring:
                    # Properly indent the docstring
                    indented_docstring = textwrap.indent(docstring, '    ')
                    config_content += f"Function:\ndef {name}:\n    \"\"\"\n{indented_docstring}\n    \"\"\"\n\n"

    # Append the line for User Query
    config_content += "User Query: {query}\n'''\n"

    # Write to config.py
    with open('config.py', 'w') as file:
        file.write(config_content)

if __name__ == "__main__":
    generate_config()