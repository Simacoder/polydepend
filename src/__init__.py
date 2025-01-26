"""
PolyDepend Analyzers Module

This module provides comprehensive dependency analysis capabilities 
for multiple programming languages and project types.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """
    Abstract base class for dependency analyzers across different languages.
    
    Defines the core interface for dependency analysis operations.
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

# Import specific language analyzers
from .python_analyzer import PythonDependencyAnalyzer
from .javascript_analyzer import JavaScriptDependencyAnalyzer
from .java_analyzer import JavaDependencyAnalyzer
from .rust_analyzer import RustDependencyAnalyzer

# Define public API
__all__ = [
    'BaseAnalyzer',
    'PythonDependencyAnalyzer',
    'JavaScriptDependencyAnalyzer',
    'JavaDependencyAnalyzer',
    'RustDependencyAnalyzer'
]

# Version and metadata
__version__ = '0.2.0'