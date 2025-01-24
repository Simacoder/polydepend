import os
import tempfile
from analyzers.python_analyzer import analyze_python_dependencies

def test_analyze_python_dependencies():
    # Create a temporary requirements.txt file
    with tempfile.TemporaryDirectory() as temp_dir:
        req_file = os.path.join(temp_dir, 'requirements.txt')
        with open(req_file, 'w') as file:
            file.write("flask==2.1.0\nrequests==2.26.0\n")

        # Analyze dependencies
        dependencies = analyze_python_dependencies(temp_dir)
        assert dependencies == ['flask==2.1.0', 'requests==2.26.0']
