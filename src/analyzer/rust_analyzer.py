import os
import toml
import re
from typing import List, Dict, Any

from base_analyzer import BaseAnalyzer

class RustDependencyAnalyzer(BaseAnalyzer):
    def analyze_dependencies(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze Rust project dependencies.
        
        Args:
            project_path (str): Path to the Rust project
        
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
        Find dependencies by scanning Cargo.toml files.
        """
        dependencies = []
        
        # Find Cargo.toml files
        for root, _, files in os.walk(project_path):
            if 'Cargo.toml' in files:
                cargo_path = os.path.join(root, 'Cargo.toml')
                dependencies.extend(self._parse_cargo_dependencies(cargo_path))
        
        # Scan source files for module imports
        imported_modules = self._scan_imports(project_path)
        dependencies.extend(imported_modules)
        
        return dependencies
    
    def _parse_cargo_dependencies(self, cargo_path: str) -> List[Dict[str, Any]]:
        """
        Parse dependencies from Cargo.toml file.
        """
        dependencies = []
        try:
            with open(cargo_path, 'r') as f:
                cargo_data = toml.load(f)
            
            # Check different dependency sections
            dependency_sections = [
                'dependencies', 
                'dev-dependencies', 
                'build-dependencies'
            ]
            
            for section in dependency_sections:
                if section in cargo_data:
                    for name, details in cargo_data[section].items():
                        # Handle different dependency specification formats
                        if isinstance(details, str):
                            version = details
                        elif isinstance(details, dict):
                            version = details.get('version', 'Unknown')
                        else:
                            version = 'Unknown'
                        
                        dependencies.append({
                            'name': name,
                            'version': version,
                            'source': cargo_path,
                            'type': section
                        })
        except Exception:
            pass
        
        return dependencies
    
    def _scan_imports(self, project_path: str) -> List[Dict[str, Any]]:
        """
        Scan Rust source files for module imports.
        """
        imported_modules = []
        
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith('.rs'):
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        # Patterns for different import styles
                        import_patterns = [
                            r'use\s+([^:;]+);',  # Simple import
                            r'use\s+([^:;]+)::[^;]+;',  # Nested import
                            r'extern\s+crate\s+([^;]+);'  # External crate
                        ]
                        
                        for pattern in import_patterns:
                            matches = re.findall(pattern, content)
                            for module in matches:
                                # Clean up module name
                                module = module.strip()
                                
                                imported_modules.append({
                                    'name': module,
                                    'source': file_path,
                                    'type': 'import'
                                })
        
        return imported_modules
    
    def detect_conflicts(self, dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential dependency conflicts.
        """
        conflicts = []
        dependency_map = {}
        
        for dep in dependencies:
            name = dep['name']
            
            if name in dependency_map:
                existing_dep = dependency_map[name]
                
                # Check for version conflicts
                if dep.get('version') and existing_dep.get('version'):
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