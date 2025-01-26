import os
import json
import re
from typing import List, Dict, Any

from base_analyzer import BaseAnalyzer

class JavaScriptDependencyAnalyzer(BaseAnalyzer):
    def analyze_dependencies(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze JavaScript project dependencies.
        
        Args:
            project_path (str): Path to the JavaScript project
        
        Returns:
            Dict[str, Any]: Comprehensive dependency analysis
        """
        dependencies = self._find_dependencies(project_path)
        conflicts = self.detect_conflicts(dependencies)
        
        return {
            'dependencies': dependencies,
            'conflicts': conflicts
        }
    
    def _find_dependencies(self, project_path: str) -> List[Dict[str, Any]]:
        """
        Find dependencies by scanning package.json and import statements.
        """
        dependencies = []
        
        # Check package.json
        package_json_path = os.path.join(project_path, 'package.json')
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                try:
                    package_data = json.load(f)
                    
                    # Collect dependencies from different sections
                    dependency_types = [
                        'dependencies', 
                        'devDependencies', 
                        'peerDependencies', 
                        'optionalDependencies'
                    ]
                    
                    for dep_type in dependency_types:
                        if dep_type in package_data:
                            for name, version in package_data[dep_type].items():
                                dependencies.append({
                                    'name': name,
                                    'version': version,
                                    'type': dep_type,
                                    'source': package_json_path
                                })
                except json.JSONDecodeError:
                    pass
        
        # Scan source files for imports
        imported_modules = self._scan_imports(project_path)
        dependencies.extend(imported_modules)
        
        return dependencies
    
    def _scan_imports(self, project_path: str) -> List[Dict[str, Any]]:
        """
        Scan JavaScript source files for imported modules.
        """
        imported_modules = []
        
        # Extensions to scan
        extensions = ['.js', '.jsx', '.ts', '.tsx']
        
        for root, _, files in os.walk(project_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        # Regex for different import styles
                        import_patterns = [
                            r'import\s+(?:[\w\*]+\s+from\s+)?[\'"]([^\'"\n]+)[\'"]',
                            r'require\([\'"]([^\'"\n]+)[\'"]\)'
                        ]
                        
                        for pattern in import_patterns:
                            matches = re.findall(pattern, content)
                            for module in matches:
                                # Ignore relative imports
                                if not module.startswith('.'):
                                    imported_modules.append({
                                        'name': module,
                                        'source': file_path,
                                        'type': 'import'
                                    })
        
        return imported_modules
    
    def detect_conflicts(self, dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential dependency conflicts.
        
        Args:
            dependencies (List[Dict[str, Any]]): List of dependencies to check
        
        Returns:
            List[Dict[str, Any]]: List of detected dependency conflicts
        """
        conflicts = []
        dependency_map = {}
        
        for dep in dependencies:
            name = dep['name']
            
            if name in dependency_map:
                existing_dep = dependency_map[name]
                
                # Check for version conflicts
                if 'version' in dep and 'version' in existing_dep:
                    if dep['version'] != existing_dep['version']:
                        conflicts.append({
                            'name': name,
                            'existing_version': existing_dep['version'],
                            'conflicting_version': dep['version'],
                            'existing_source': existing_dep['source'],
                            'conflicting_source': dep['source']
                        })
            else:
                dependency_map[name] = dep
        
        return conflicts