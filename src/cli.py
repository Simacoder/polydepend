import argparse
from analyzers.python_analyzer import analyze_python_dependencies
from resolver.resolver_engine import resolve_dependencies
from fetcher.fetcher import fetch_python_dependencies

def main():
    parser = argparse.ArgumentParser(description="PolyDepend - A Dependency Manager")
    parser.add_argument('path', help="Path to the project")
    args = parser.parse_args()

    # Analyze
    dependencies = analyze_python_dependencies(args.path)
    print("Dependencies found:", dependencies)

    # Resolve
    resolved = resolve_dependencies(dependencies)
    print("Resolved dependencies:", resolved)

    # Fetch
    fetch_python_dependencies(resolved.values())
    print("Dependencies installed successfully.")

if __name__ == '__main__':
    main()
