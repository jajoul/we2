import os

# Find all .py and .html files, excluding the venv directory
files_to_process = []
for root, dirs, files in os.walk("."):
    if 'venv' in dirs:
        dirs.remove('venv')
    for name in files:
        if name.endswith(('.py', '.html')):
            files_to_process.append(os.path.join(root, name))

# Create the command
command = f"pybabel extract -o locale/django.po {' '.join(files_to_process)}"

# Run the command
os.system(command)
