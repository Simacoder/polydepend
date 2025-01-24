from .python_analyzer import analyze_python_dependencies
from .js_analyzer import analyze_js_dependencies

def analyze_dependencies(project_path, language):
    """
    Analyze dependencies for the specified project and language.
    Args:
        project_path (str): Path to the project.
        language (str): Language of the project (e.g., 'python', 'javascript').
    Returns:
        list: A list of dependencies for the project.
    """
    if language == 'python':
        return analyze_python_dependencies(project_path)
    elif language == 'javascript':
        return analyze_js_dependencies(project_path)
    else:
        raise ValueError(f"Unsupported language: {language}")
