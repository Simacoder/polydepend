import os
import re

def analyze_python_dependencies(project_path):
    """ Analyze Python dependencies """
    req_file = os.path.join(project_path, 'requirements.txt')
    if not os.path.exists(req_file):
        return []
    with open(req_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]