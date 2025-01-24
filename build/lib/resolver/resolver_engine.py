def resolve_dependencies(dependencies):
    """
        Resolve dependence conflict and return unified list
    """
    resolved = {}
    for dep in dependencies:
        names, version = dep.split('==')
        if name not in resolved or resolved[name] < version:
            resolved[name] = version
    return resolved