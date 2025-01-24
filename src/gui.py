import tkinter as tk
from tkinter import filedialog
from analyzers.python_analyzer import analyze_python_dependencies
from resolver.resolver_engine import resolve_dependencies
from fetcher.fetcher import fetch_python_dependencies

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        dependencies = analyze_python_dependencies(folder_path)
        resolved = resolve_dependencies(dependencies)
        fetch_python_dependencies(resolved.values())
        result_label.config(text=f"Dependencies installed: {', '.join(resolved.values())}")

# Create GUI
root = tk.Tk()
root.title("PolyDepend - Dependency Manager")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Select your project folder:")
label.pack()

select_button = tk.Button(frame, text="Browse", command=select_folder)
select_button.pack()

result_label = tk.Label(frame, text="")
result_label.pack()

root.mainloop()
