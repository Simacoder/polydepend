import os
import pytest
import tempfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from analyzer import (
    PythonDependencyAnalyzer,
    JavaScriptDependencyAnalyzer,
    JavaDependencyAnalyzer,
    RustDependencyAnalyzer
)

def create_test_project(language):
    """
    Create a temporary test project directory for different languages.
    """
    temp_dir = tempfile.mkdtemp()
    
    if language == 'python':
        # Create requirements.txt
        with open(os.path.join(temp_dir, 'requirements.txt'), 'w') as f:
            f.write('requests==2.26.0\npytest==6.2.5\n')
        
        # Create a sample Python file
        with open(os.path.join(temp_dir, 'test_module.py'), 'w') as f:
            f.write('import os\nimport json\n')
    
    elif language == 'javascript':
        # Create package.json
        with open(os.path.join(temp_dir, 'package.json'), 'w') as f:
            f.write('''{
                "dependencies": {
                    "lodash": "^4.17.21",
                    "axios": "^0.21.1"
                }
            }''')
        
        # Create a sample JS file
        with open(os.path.join(temp_dir, 'test_module.js'), 'w') as f:
            f.write('import fs from "fs";\nimport path from "path";\n')
    
    elif language == 'java':
        # Create pom.xml
        with open(os.path.join(temp_dir, 'pom.xml'), 'w') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
            <project>
                <dependencies>
                    <dependency>
                        <groupId>junit</groupId>
                        <artifactId>junit</artifactId>
                        <version>4.13.2</version>
                    </dependency>
                </dependencies>
            </project>''')
        
        # Create a sample Java file
        with open(os.path.join(temp_dir, 'TestModule.java'), 'w') as f:
            f.write('import java.util.List;\nimport java.io.File;\n')
    
    elif language == 'rust':
        # Create Cargo.toml
        with open(os.path.join(temp_dir, 'Cargo.toml'), 'w') as f:
            f.write('''[package]
            name = "test-project"
            version = "0.1.0"

            [dependencies]
            serde = "1.0"
            tokio = "1.0"''')
        
        # Create a sample Rust file
        with open(os.path.join(temp_dir, 'main.rs'), 'w') as f:
            f.write('use std::fs;\nuse std::path::Path;\n')
    
    return temp_dir

@pytest.mark.parametrize("language,analyzer_class", [
    ('python', PythonDependencyAnalyzer),
    ('javascript', JavaScriptDependencyAnalyzer),
    ('java', JavaDependencyAnalyzer),
    ('rust', RustDependencyAnalyzer)
])
def test_dependency_analysis(language, analyzer_class):
    """
    Test dependency analysis for different languages.
    """
    # Create a temporary test project
    project_path = create_test_project(language)
    
    # Initialize analyzer
    analyzer = analyzer_class()
    
    try:
        # Perform dependency analysis
        result = analyzer.analyze_dependencies(project_path)
        
        # Basic assertions
        assert 'dependencies' in result
        assert 'conflicts' in result
        
        # Check that dependencies were found
        assert len(result['dependencies']) > 0
    finally:
        # Clean up temporary directory
        import shutil
        shutil.rmtree(project_path)

def test_multi_language_conflict_detection():
    """
    Test conflict detection across multiple language configurations.
    """
    # Create test projects
    project_paths = {
        'python': create_test_project('python'),
        'javascript': create_test_project('javascript'),
        'java': create_test_project('java'),
        'rust': create_test_project('rust')
    }
    
    analyzers = {
        'python': PythonDependencyAnalyzer(),
        'javascript': JavaScriptDependencyAnalyzer(),
        'java': JavaDependencyAnalyzer(),
        'rust': RustDependencyAnalyzer()
    }
    
    try:
        for lang, path in project_paths.items():
            result = analyzers[lang].analyze_dependencies(path)
            
            # Verify conflict detection mechanism works
            assert 'conflicts' in result
            
            # Optional: print conflicts for manual inspection
            if result['conflicts']:
                print(f"{lang.upper()} Conflicts: {result['conflicts']}")
    finally:
        # Clean up temporary directories
        import shutil
        for path in project_paths.values():
            shutil.rmtree(path)