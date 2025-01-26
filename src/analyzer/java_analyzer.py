import os
import xml.etree.ElementTree as ET
import json
from typing import List, Dict, Any

from base_analyzer import BaseAnalyzer

class JavaDependencyAnalyzer(BaseAnalyzer):
    def analyze_dependencies(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze Java project dependencies.
        
        Args:
            project_path (str): Path to the Java project
        
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
        Find dependencies by scanning pom.xml and build.gradle files.
        """
        dependencies = []
        
        # Check Maven (pom.xml)
        pom_path = self._find_file(project_path, 'pom.xml')
        if pom_path:
            dependencies.extend(self._parse_maven_dependencies(pom_path))
        
        # Check Gradle (build.gradle)
        gradle_path = self._find_file(project_path, 'build.gradle')
        if gradle_path:
            dependencies.extend(self._parse_gradle_dependencies(gradle_path))
        
        # Scan source files for imports
        imported_modules = self._scan_imports(project_path)
        dependencies.extend(imported_modules)
        
        return dependencies
    
    def _find_file(self, project_path: str, filename: str) -> str:
        """
        Find a specific file in the project directory.
        """
        for root, _, files in os.walk(project_path):
            if filename in files:
                return os.path.join(root, filename)
        return None
    
    def _parse_maven_dependencies(self, pom_path: str) -> List[Dict[str, Any]]:
        """
        Parse dependencies from Maven pom.xml file.
        """
        dependencies = []
        try:
            tree = ET.parse(pom_path)
            root = tree.getroot()
            
            # Namespace handling
            ns = {'ns': 'http://maven.apache.org/POM/4.0.0'}
            
            # Find dependencies
            dep_elements = root.findall('.//ns:dependency', ns)
            for dep in dep_elements:
                group_id = dep.find('ns:groupId', ns)
                artifact_id = dep.find('ns:artifactId', ns)
                version = dep.find('ns:version', ns)
                
                if group_id is not None and artifact_id is not None:
                    dependencies.append({
                        'name': f"{group_id.text}:{artifact_id.text}",
                        'version': version.text if version is not None else 'Unknown',
                        'source': 'Maven (pom.xml)'
                    })
        except Exception:
            pass
        
        return dependencies
    
    def _parse_gradle_dependencies(self, gradle_path: str) -> List[Dict[str, Any]]:
        """
        Parse dependencies from Gradle build.gradle file.
        Note: This is a simplified parsing and might not cover all Gradle dependency configurations.
        """
        dependencies = []
        try:
            with open(gradle_path, 'r') as f:
                content = f.read()
                
                # Simple regex to find dependencies
                import re
                dep_pattern = r'(?:implementation|api|compileOnly)\s*[\'"]([^:]+):([^:]+):([^\'"]+)[\'"]'
                matches = re.findall(dep_pattern, content)
                
                for group, artifact, version in matches:
                    dependencies.append({
                        'name': f"{group}:{artifact}",
                        'version': version,
                        'source': 'Gradle (build.gradle)'
                    })
        except Exception:
            pass
        
        return dependencies
    
    def _scan_imports(self, project_path: str) -> List[Dict[str, Any]]:
        """
        Scan Java source files for imported packages.
        """
        imported_modules = []
        
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith('import ') and not line.startswith('import static'):
                                try:
                                    # Remove 'import ' and ';'
                                    module = line[7:].rstrip(';')
                                    
                                    imported_modules.append({
                                        'name': module,
                                        'source': file_path,
                                        'type': 'import'
                                    })
                                except Exception:
                                    pass
        
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