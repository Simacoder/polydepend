import json
import os

def analyze_js_dependencies(project_path):
    """
    Analyze JavaScript dependencies by parsing package.json.
    Args:
        project_path (str): Path to the JavaScript project.
    Returns:
        list: A list of dependencies with their versions.
    """
    package_json_path = os.path.join(project_path, 'package.json')
    
    if not os.path.exists(package_json_path):
        raise FileNotFoundError(f"No package.json found in {project_path}")

    with open(package_json_path, 'r') as file:
        package_data = json.load(file)
    
    dependencies = package_data.get('dependencies', {})
    dev_dependencies = package_data.get('devDependencies', {})
    
    # Combine dependencies and devDependencies
    all_dependencies = {**dependencies, **dev_dependencies}
    
    return [f"{name}@{version}" for name, version in all_dependencies.items()]

if __name__ == "__main__":
    # Test the function
    test_path = "/path/to/your/javascript/project"
    try:
        deps = analyze_js_dependencies(test_path)
        print("Dependencies found:", deps)
    except FileNotFoundError as e:
        print(e)
