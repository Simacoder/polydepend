import re
from typing import List, Dict, Any
import pkg_resources

class DependencyResolver:
    """Advanced dependency resolution and conflict management."""
    
    @staticmethod
    def parse_version(version_str: str) -> tuple:
        """
        Parse version string into comparable components.
        
        Args:
            version_str (str): Version string
        
        Returns:
            Tuple of version components for comparison
        """
        # Remove any leading 'v' or 'V'
        version_str = version_str.lstrip('vV')
        
        # Split version into components, handling pre-release tags
        components = re.split(r'[.-]', version_str)
        
        # Convert to integers where possible
        parsed_components = []
        for comp in components:
            try:
                parsed_components.append(int(comp))
            except ValueError:
                # Handle pre-release tags like alpha, beta
                parsed_components.append(comp)
        
        return tuple(parsed_components)
    
    def resolve_version_conflicts(self, dependencies: List[str]) -> Dict[str, str]:
        """
        Resolve version conflicts using smart version comparison.
        
        Args:
            dependencies (List[str]): List of dependencies with versions
        
        Returns:
            Dictionary of resolved dependencies
        """
        # Group dependencies by package name
        dependency_groups = {}
        for dep in dependencies:
            # Split into package name and version
            match = re.match(r'([a-zA-Z0-9-_]+)[=><]*(.*)', dep)
            if match:
                pkg_name, version = match.groups()
                if not version:
                    version = '*'  # No specific version specified
                
                if pkg_name not in dependency_groups:
                    dependency_groups[pkg_name] = []
                dependency_groups[pkg_name].append(version)
        
        # Resolve conflicts
        resolved_dependencies = {}
        for pkg_name, versions in dependency_groups.items():
            if len(versions) == 1:
                resolved_dependencies[pkg_name] = versions[0]
            else:
                # Compare versions and select the highest
                sorted_versions = sorted(versions, key=self.parse_version, reverse=True)
                resolved_dependencies[pkg_name] = sorted_versions[0]
        
        return resolved_dependencies
    
    def check_compatibility(self, dependencies: Dict[str, str]) -> List[str]:
        """
        Check compatibility between dependencies.
        
        Args:
            dependencies (Dict[str, str]): Resolved dependencies
        
        Returns:
            List of potential compatibility issues
        """
        compatibility_warnings = []
        
        for pkg_name, version in dependencies.items():
            try:
                # Check if package is available
                dist = pkg_resources.get_distribution(pkg_name)
                
                # Check for potential conflicts with installed packages
                for req in dist.requires():
                    req_name = req.project_name
                    if req_name in dependencies:
                        # Check if the required version matches
                        required_version = req.specifier
                        resolved_version = dependencies[req_name]
                        
                        if not pkg_resources.Requirement.parse(f"{req_name}{required_version}").specifier.contains(resolved_version):
                            compatibility_warnings.append(
                                f"Potential conflict: {pkg_name} requires {req_name} {required_version}, but resolved version is {resolved_version}"
                            )
            except pkg_resources.DistributionNotFound:
                # Package not installed, can't perform deep compatibility check
                pass
        
        return compatibility_warnings
    
    def resolve_dependencies(self, dependencies: List[str]) -> Dict[str, Any]:
        """
        Comprehensive dependency resolution.
        
        Args:
            dependencies (List[str]): List of dependencies
        
        Returns:
            Comprehensive resolution report
        """
        resolved_versions = self.resolve_version_conflicts(dependencies)
        compatibility_warnings = self.check_compatibility(resolved_versions)
        
        return {
            'resolved_dependencies': resolved_versions,
            'compatibility_warnings': compatibility_warnings
        }
