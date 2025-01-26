"""
Base Analyzer for Dependency Management

Provides a common abstract base class for language-specific dependency analyzers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAnalyzer(ABC):
    """
    Abstract base class defining the interface for dependency analyzers.
    
    This class provides a standard approach to analyzing dependencies
    across different programming languages.
    """
    
    @abstractmethod
    def analyze_dependencies(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze dependencies for a given project.
        
        Args:
            project_path (str): Path to the project to be analyzed
        
        Returns:
            Dict[str, Any]: Comprehensive dependency analysis results
        """
        pass
    
    @abstractmethod
    def detect_conflicts(self, dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential dependency conflicts.
        
        Args:
            dependencies (List[Dict[str, Any]]): List of dependencies to check
        
        Returns:
            List[Dict[str, Any]]: List of detected dependency conflicts
        """
        pass
    
    def _is_semantic_version(self, version_str: str) -> bool:
        """
        Check if a version string follows semantic versioning.
        
        Args:
            version_str (str): Version string to validate
        
        Returns:
            bool: True if version follows semantic versioning, False otherwise
        """
        import re
        
        semver_pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
        
        return re.match(semver_pattern, version_str) is not None
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        Compare two version strings.
        
        Args:
            version1 (str): First version string
            version2 (str): Second version string
        
        Returns:
            int: -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        from packaging import version
        
        try:
            v1 = version.parse(version1)
            v2 = version.parse(version2)
            
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
            return 0
        except Exception:
            # Fallback to string comparison if parsing fails
            if version1 < version2:
                return -1
            elif version1 > version2:
                return 1
            return 0