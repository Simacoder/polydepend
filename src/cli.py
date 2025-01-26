import argparse
import os
import json
from typing import Dict, Any

from analyzer import (
    PythonDependencyAnalyzer,
    JavaScriptDependencyAnalyzer,
    JavaDependencyAnalyzer,
    RustDependencyAnalyzer
)

class PolyDependCLI:
    def __init__(self):
        self.analyzers = {
            'python': PythonDependencyAnalyzer(),
            'javascript': JavaScriptDependencyAnalyzer(),
            'java': JavaDependencyAnalyzer(),
            'rust': RustDependencyAnalyzer()
        }
    
    def analyze_project(self, project_path: str, language: str = None) -> Dict[str, Any]:
        """
        Analyze dependencies for a project.
        
        Args:
            project_path (str): Path to the project
            language (str, optional): Specific language to analyze
        
        Returns:
            Dict[str, Any]: Comprehensive dependency analysis
        """
        results = {}
        
        # If language is specified, analyze only that language
        if language:
            if language not in self.analyzers:
                raise ValueError(f"Unsupported language: {language}")
            
            analyzer = self.analyzers[language]
            results[language] = analyzer.analyze_dependencies(project_path)
            return results
        
        # Otherwise, try all supported analyzers
        for lang, analyzer in self.analyzers.items():
            try:
                results[lang] = analyzer.analyze_dependencies(project_path)
            except Exception as e:
                results[lang] = {
                    'error': str(e)
                }
        
        return results
    
    def output_results(self, results: Dict[str, Any], output_format: str = 'json'):
        """
        Output analysis results in specified format.
        
        Args:
            results (Dict[str, Any]): Dependency analysis results
            output_format (str, optional): Output format (json or text)
        """
        if output_format == 'json':
            print(json.dumps(results, indent=2))
        else:
            for lang, data in results.items():
                print(f"--- {lang.upper()} Dependencies ---")
                print(f"Dependencies: {len(data.get('dependencies', []))}")
                print(f"Conflicts: {len(data.get('conflicts', []))}")
                print()

def main():
    parser = argparse.ArgumentParser(description='PolyDepend: Multi-language Dependency Analyzer')
    parser.add_argument('project_path', help='Path to the project to analyze')
    parser.add_argument('-l', '--language', 
                        help='Specific language to analyze (python, javascript, java, rust)')
    parser.add_argument('-o', '--output', 
                        choices=['json', 'text'], 
                        default='json',
                        help='Output format')
    
    args = parser.parse_args()
    
    cli = PolyDependCLI()
    
    try:
        results = cli.analyze_project(
            os.path.abspath(args.project_path), 
            args.language
        )
        cli.output_results(results, args.output)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()