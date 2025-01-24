from .resolver_engine import resolve_dependencies

def resolve_project_dependencies(dependencies):
    """
    Resolve conflicts in a project's dependencies.
    Args:
        dependencies (list): A list of dependencies with potential conflicts.
    Returns:
        dict: A dictionary of resolved dependencies (name: version).
    """
    return resolve_dependencies(dependencies)
