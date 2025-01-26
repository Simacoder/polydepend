import subprocess
import sys
import venv
import os
import json
from typing import List, Dict, Optional

class DependencyFetcher:
    """Advanced dependency installation and management."""
    
    @staticmethod
    def create_virtual_environment(path: Optional[str] = None) -> str:
        """
        Create a virtual environment.
        
        Args:
            path (Optional[str]): Path to create virtual environment
        
        Returns:
            Path to the virtual environment
        """
        if not path:
            path = os.path.join(os.getcwd(), 'polydepend_venv')
        
        # Create virtual environment
        venv.create(path, with_pip=True)
        
        return path
    
    @classmethod
    def install_dependencies(
        cls, 
        dependencies: List[str], 
        venv_path: Optional[str] = None, 
        upgrade: bool = False
    ) -> Dict[str, bool]:
        """
        Install dependencies with advanced error handling.
        
        Args:
            dependencies (List[str]): List of dependencies to install
            venv_path (Optional[str]): Path to virtual environment
            upgrade (bool): Whether to upgrade existing packages
        
        Returns:
            Dictionary of installation results
        """
        # Use existing virtual environment or create new one
        if not venv_path:
            venv_path = cls.create_virtual_environment()
        
        # Determine pip executable
        pip_executable = os.path.join(venv_path, 'bin', 'pip')
        if sys.platform == 'win32':
            pip_executable = os.path.join(venv_path, 'Scripts', 'pip')
        
        # Installation results tracker
        installation_results = {}
        
        for dep in dependencies:
            # Prepare install command
            install_cmd = [pip_executable, 'install']
            if upgrade:
                install_cmd.append('--upgrade')
            install_cmd.append(dep)
            
            try:
                # Run installation
                result = subprocess.run(
                    install_cmd, 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                installation_results[dep] = True
            except subprocess.CalledProcessError as e:
                # Detailed error logging
                installation_results[dep] = False
                print(f"Failed to install {dep}:")
                print(f"Error output: {e.stderr}")
        
        return installation_results
    
    @classmethod
    def export_requirements(
        cls, 
        venv_path: Optional[str] = None, 
        output_path: Optional[str] = None
    ) -> str:
        """
        Export requirements from a virtual environment.
        
        Args:
            venv_path (Optional[str]): Path to virtual environment
            output_path (Optional[str]): Path to save requirements file
        
        Returns:
            Path to the generated requirements file
        """
        # Use existing virtual environment or create new one
        if not venv_path:
            venv_path = cls.create_virtual_environment()
        
        # Determine pip executable
        pip_executable = os.path.join(venv_path, 'bin', 'pip')
        if sys.platform == 'win32':
            pip_executable = os.path.join(venv_path, 'Scripts', 'pip')
        
        # Generate requirements
        try:
            result = subprocess.run(
                [pip_executable, 'freeze'], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            # Determine output path
            if not output_path:
                output_path = os.path.join(os.getcwd(), 'requirements.txt')
            
            # Write requirements to file
            with open(output_path, 'w') as f:
                f.write(result.stdout)
            
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Failed to export requirements: {e.stderr}")
            return ''
    
    @classmethod
    def manage_dependency_cache(
        cls, 
        action: str = 'clean', 
        cache_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Manage pip dependency cache.
        
        Args:
            action (str): Cache management action (clean, info)
            cache_dir (Optional[str]): Custom cache directory
        
        Returns:
            Dictionary with cache management results
        """
        # Determine pip executable
        pip_executable = sys.executable.replace('python', 'pip')
        
        # Prepare cache management command
        if action == 'clean':
            cmd = [pip_executable, 'cache', 'purge']
        elif action == 'info':
            cmd = [pip_executable, 'cache', 'info']
        else:
            raise ValueError(f"Unsupported cache action: {action}")
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            return {
                'success': True,
                'output': result.stdout
            }
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': e.stderr
            }