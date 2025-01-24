import subprocess

def fetch_python_dependencies(dependencies):
    """ Install Python dependencies"""
    for dep in dependencies:
        subprocess.run(['pip', 'install', dep])