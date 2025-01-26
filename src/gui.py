import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json

from analyzers.python_analyzer import PythonDependencyAnalyzer
from resolver.resolver_engine import DependencyResolver
from fetcher.fetcher import DependencyFetcher

class PolyDependGUI:
    """Graphical User Interface for PolyDepend Dependency Management"""
    def __init__(self, master):
        """Initialize the GUI application"""
        self.master = master
        master.title("PolyDepend - Dependency Management")
        master.geometry("700x600")
        
        # Project path
        self.project_path = tk.StringVar(value=os.getcwd())
        
        # Analyzer and resolver instances
        self.analyzer = PythonDependencyAnalyzer()
        self.resolver = DependencyResolver()
        self.fetcher = DependencyFetcher()
        
        # Create UI components
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout GUI widgets"""
        # Project Path Selection
        path_frame = tk.Frame(self.master)
        path_frame.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(path_frame, text="Project Path:").pack(side=tk.LEFT)
        path_entry = tk.Entry(path_frame, textvariable=self.project_path, width=50)
        path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Button(path_frame, text="Browse", command=self._browse_project_path).pack(side=tk.LEFT)
        
        # Notebook for different actions
        notebook = ttk.Notebook(self.master)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Create tabs
        tabs = [
            ("Analyze", self._create_analyze_tab),
            ("Resolve", self._create_resolve_tab),
            ("Install", self._create_install_tab),
            ("Cache", self._create_cache_tab)
        ]
        
        self.tab_frames = {}
        for label, creator in tabs:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=label)
            creator(frame)
            self.tab_frames[label] = frame
    
    def _browse_project_path(self):
        """Open file dialog to select project path"""
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.project_path.set(selected_path)
    
    def _create_analyze_tab(self, parent):
        """Create widgets for dependency analysis"""
        analyze_btn = tk.Button(
            parent, 
            text="Analyze Dependencies", 
            command=self._perform_analysis
        )
        analyze_btn.pack(pady=10)
        
        # Results display
        self.analyze_results = tk.Text(parent, height=15, width=70, wrap=tk.WORD)
        self.analyze_results.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    
    def _create_resolve_tab(self, parent):
        """Create widgets for dependency resolution"""
        resolve_btn = tk.Button(
            parent, 
            text="Resolve Dependencies", 
            command=self._perform_resolution
        )
        resolve_btn.pack(pady=10)
        
        # Results display
        self.resolve_results = tk.Text(parent, height=15, width=70, wrap=tk.WORD)
        self.resolve_results.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    
    def _create_install_tab(self, parent):
        """Create widgets for dependency installation"""
        # Upgrade checkbox
        self.upgrade_var = tk.BooleanVar(value=False)
        upgrade_check = tk.Checkbutton(
            parent, 
            text="Upgrade Existing Packages", 
            variable=self.upgrade_var
        )
        upgrade_check.pack(pady=5)
        
        install_btn = tk.Button(
            parent, 
            text="Install Dependencies", 
            command=self._perform_installation
        )
        install_btn.pack(pady=10)
        
        # Results display
        self.install_results = tk.Text(parent, height=15, width=70, wrap=tk.WORD)
        self.install_results.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    
    def _create_cache_tab(self, parent):
        """Create widgets for cache management"""
        cache_frame = tk.Frame(parent)
        cache_frame.pack(pady=10)
        
        # Cache action selection
        self.cache_action = tk.StringVar(value="info")
        cache_options = [
            ("Show Cache Info", "info"),
            ("Clean Cache", "clean")
        ]
        
        for text, value in cache_options:
            rb = tk.Radiobutton(
                cache_frame, 
                text=text, 
                variable=self.cache_action, 
                value=value
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        cache_btn = tk.Button(
            parent, 
            text="Manage Cache", 
            command=self._perform_cache_management
        )
        cache_btn.pack(pady=10)
        
        # Results display
        self.cache_results = tk.Text(parent, height=15, width=70, wrap=tk.WORD)
        self.cache_results.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
    
    def _perform_analysis(self):
        """Perform dependency analysis"""
        path = self.project_path.get()
        try:
            # Clear previous results
            self.analyze_results.delete(1.0, tk.END)
            
            # Perform analysis
            analysis_result = self.analyzer.analyze_project(path)
            
            # Display results
            result_str = json.dumps(analysis_result, indent=2)
            self.analyze_results.insert(tk.END, result_str)
        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))
    
    def _perform_resolution(self):
        """Resolve dependency conflicts"""
        path = self.project_path.get()
        try:
            # Clear previous results
            self.resolve_results.delete(1.0, tk.END)
            
            # Get project dependencies
            project_deps = self.analyzer.analyze_requirements(path)
            
            # Resolve dependencies
            resolution_result = self.resolver.resolve_dependencies(project_deps)
            
            # Display results
            result_str = json.dumps(resolution_result, indent=2)
            self.resolve_results.insert(tk.END, result_str)
        except Exception as e:
            messagebox.showerror("Resolution Error", str(e))
    
    def _perform_installation(self):
        """Install project dependencies"""
        path = self.project_path.get()
        try:
            # Clear previous results
            self.install_results.delete(1.0, tk.END)
            
            # Get project dependencies
            project_deps = self.analyzer.analyze_requirements(path)
            
            # Install dependencies
            install_results = self.fetcher.install_dependencies(
                project_deps, 
                upgrade=self.upgrade_var.get()
            )
            
            # Display results
            result_str = json.dumps(install_results, indent=2)
            self.install_results.insert(tk.END, result_str)
        except Exception as e:
            messagebox.showerror("Installation Error", str(e))
    
    def _perform_cache_management(self):
        """Manage pip dependency cache"""
        try:
            # Clear previous results
            self.cache_results.delete(1.0, tk.END)
            
            # Perform cache management
            cache_result = self.fetcher.manage_dependency_cache(
                action=self.cache_action.get()
            )
            
            # Display results
            result_str = json.dumps(cache_result, indent=2)
            self.cache_results.insert(tk.END, result_str)
        except Exception as e:
            messagebox.showerror("Cache Management Error", str(e))

def main():
    """Entry point for PolyDepend GUI"""
    root = tk.Tk()
    app = PolyDependGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()