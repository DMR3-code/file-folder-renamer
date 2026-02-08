import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import random
import re
from datetime import datetime
from typing import List, Tuple, Optional


class EnhancedFileFolderRenamer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("File and Folder Renamer")
        self.root.geometry("850x800")
        self.root.resizable(True, True)
        
        # Variables
        self.directory = tk.StringVar()
        self.pattern = tk.StringVar(value="{list1}_{prefix}{counter}_v{version}")
        self.start_counter = tk.IntVar(value=1)
        self.version_start = tk.StringVar(value="1.0")
        self.version_increment = tk.DoubleVar(value=0.1)
        self.include_files = tk.BooleanVar(value=True)
        self.include_folders = tk.BooleanVar(value=True)
        self.preview_mode = tk.BooleanVar(value=True)
        self.version_strategy = tk.StringVar(value="fixed")  # fixed, incremental, random
        self.recursive = tk.BooleanVar(value=False)
        self.file_filter = tk.StringVar(value="*")
        self.case_option = tk.StringVar(value="none")
        
        # Rename history for undo functionality
        self.rename_history: List[List[Tuple[str, str]]] = []
        
        # Customizable lists - generic names for general use
        self.custom_list1: List[str] = []  # Custom words list 1
        self.custom_list2: List[str] = []  # Custom words list 2 (prefixes)
        
        # Store notebook reference
        self.notebook: Optional[ttk.Notebook] = None
        self.progress: Optional[ttk.Progressbar] = None
        
        # Listbox references for custom data
        self.list1_listbox: Optional[tk.Listbox] = None
        self.list2_listbox: Optional[tk.Listbox] = None
        
        self.create_widgets()
        
    def create_widgets(self) -> None:
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main tab
        main_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(main_frame, text="Main")
        
        # Custom Data tab
        custom_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(custom_frame, text="Custom Lists")
        
        # Pattern help tab
        help_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(help_frame, text="Pattern Help")
        
        # Setup all tabs
        self.setup_main_tab(main_frame)
        self.setup_custom_data_tab(custom_frame)
        self.setup_pattern_help(help_frame)
        
    def setup_main_tab(self, main_frame: ttk.Frame) -> None:
        # Directory selection
        ttk.Label(main_frame, text="Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.directory, width=50).grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        ttk.Button(main_frame, text="Browse", command=self.browse_directory).grid(row=0, column=3, padx=5, pady=5)
        
        # Rename pattern
        ttk.Label(main_frame, text="Rename Pattern:").grid(row=1, column=0, sticky=tk.W, pady=5)
        pattern_frame = ttk.Frame(main_frame)
        pattern_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(pattern_frame, textvariable=self.pattern, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(pattern_frame, text="Pattern Help", command=self.show_pattern_help).pack(side=tk.LEFT, padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Counter options
        ttk.Label(options_frame, text="Start Counter:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(options_frame, from_=1, to=10000, textvariable=self.start_counter, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Version options
        ttk.Label(options_frame, text="Version Start:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(options_frame, textvariable=self.version_start, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(options_frame, text="Version Increment:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(options_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.version_increment, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(options_frame, text="Version Strategy:").grid(row=3, column=0, sticky=tk.W, pady=2)
        strategy_combo = ttk.Combobox(options_frame, textvariable=self.version_strategy, 
                                     values=["fixed", "incremental", "random"], width=10, state="readonly")
        strategy_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Include options
        ttk.Checkbutton(options_frame, text="Include Files", variable=self.include_files).grid(row=0, column=2, sticky=tk.W, pady=2, padx=20)
        ttk.Checkbutton(options_frame, text="Include Folders", variable=self.include_folders).grid(row=1, column=2, sticky=tk.W, pady=2, padx=20)
        ttk.Checkbutton(options_frame, text="Preview Before Renaming", variable=self.preview_mode).grid(row=2, column=2, sticky=tk.W, pady=2, padx=20)
        ttk.Checkbutton(options_frame, text="Recursive (Include Subdirectories)", variable=self.recursive).grid(row=3, column=2, sticky=tk.W, pady=2, padx=20)
        
        # File filter option
        ttk.Label(options_frame, text="File Filter:").grid(row=4, column=0, sticky=tk.W, pady=2)
        filter_entry = ttk.Entry(options_frame, textvariable=self.file_filter, width=15)
        filter_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(options_frame, text="(e.g., *.txt, *.jpg, *)").grid(row=4, column=2, sticky=tk.W, padx=5, pady=2)
        
        # Case transformation option
        ttk.Label(options_frame, text="Case Transform:").grid(row=5, column=0, sticky=tk.W, pady=2)
        case_combo = ttk.Combobox(options_frame, textvariable=self.case_option, 
                                  values=["none", "uppercase", "lowercase", "title"], width=10, state="readonly")
        case_combo.grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Preview", command=self.preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rename", command=self.rename).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Undo Last", command=self.undo_last_rename).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insert Pattern", command=self.insert_pattern).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=400)
        self.progress.grid(row=4, column=0, columnspan=4, pady=5, sticky=(tk.W, tk.E))
        
        # Preview area
        ttk.Label(main_frame, text="Preview:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        # Treeview for preview
        columns = ("current", "new")
        self.preview_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
        self.preview_tree.heading("current", text="Current Name")
        self.preview_tree.heading("new", text="New Name")
        self.preview_tree.column("current", width=350)
        self.preview_tree.column("new", width=350)
        self.preview_tree.grid(row=6, column=0, columnspan=4, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        scrollbar.grid(row=6, column=4, sticky=(tk.N, tk.S), pady=5)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=7, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
    
    def setup_custom_data_tab(self, custom_frame: ttk.Frame) -> None:
        """Setup the Custom Lists tab for managing custom word lists"""
        
        # Create two side-by-side frames
        left_frame = ttk.LabelFrame(custom_frame, text="Custom List 1 - {list1}", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.LabelFrame(custom_frame, text="Custom List 2 / Prefixes - {prefix}", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # --- Custom List 1 Section ---
        list1_input_frame = ttk.Frame(left_frame)
        list1_input_frame.pack(fill=tk.X, pady=5)
        
        self.list1_entry = tk.StringVar()
        ttk.Entry(list1_input_frame, textvariable=self.list1_entry, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(list1_input_frame, text="Add", command=self.add_list1_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(list1_input_frame, text="Remove", command=self.remove_list1_item).pack(side=tk.LEFT, padx=2)
        
        # List 1 listbox with scrollbar
        list1_list_frame = ttk.Frame(left_frame)
        list1_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.list1_listbox = tk.Listbox(list1_list_frame, height=15, selectmode=tk.SINGLE)
        list1_scrollbar = ttk.Scrollbar(list1_list_frame, orient=tk.VERTICAL, command=self.list1_listbox.yview)
        self.list1_listbox.configure(yscrollcommand=list1_scrollbar.set)
        
        self.list1_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list1_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # List 1 quick actions
        list1_btn_frame = ttk.Frame(left_frame)
        list1_btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(list1_btn_frame, text="Load Examples", command=self.load_example_list1).pack(side=tk.LEFT, padx=2)
        ttk.Button(list1_btn_frame, text="Clear All", command=self.clear_list1).pack(side=tk.LEFT, padx=2)
        
        # --- Custom List 2 / Prefixes Section ---
        list2_input_frame = ttk.Frame(right_frame)
        list2_input_frame.pack(fill=tk.X, pady=5)
        
        self.list2_entry = tk.StringVar()
        ttk.Entry(list2_input_frame, textvariable=self.list2_entry, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(list2_input_frame, text="Add", command=self.add_list2_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(list2_input_frame, text="Remove", command=self.remove_list2_item).pack(side=tk.LEFT, padx=2)
        
        # List 2 listbox with scrollbar
        list2_list_frame = ttk.Frame(right_frame)
        list2_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.list2_listbox = tk.Listbox(list2_list_frame, height=15, selectmode=tk.SINGLE)
        list2_scrollbar = ttk.Scrollbar(list2_list_frame, orient=tk.VERTICAL, command=self.list2_listbox.yview)
        self.list2_listbox.configure(yscrollcommand=list2_scrollbar.set)
        
        self.list2_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list2_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # List 2 quick actions
        list2_btn_frame = ttk.Frame(right_frame)
        list2_btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(list2_btn_frame, text="Load Examples", command=self.load_example_list2).pack(side=tk.LEFT, padx=2)
        ttk.Button(list2_btn_frame, text="Clear All", command=self.clear_list2).pack(side=tk.LEFT, padx=2)
        
        # Info label
        info_label = ttk.Label(custom_frame, 
                               text="💡 Add custom words to use with {list1} and {prefix} patterns. Click 'Load Examples' for sample data.", 
                               foreground="gray")
        info_label.pack(side=tk.BOTTOM, pady=10)
    
    # --- Custom List 1 Management ---
    def add_list1_item(self) -> None:
        """Add an item to custom list 1"""
        item = self.list1_entry.get().strip()
        if item:
            if item not in self.custom_list1:
                self.custom_list1.append(item)
                self.list1_listbox.insert(tk.END, item)
                self.list1_entry.set("")
            else:
                messagebox.showwarning("Duplicate", f"'{item}' already exists in the list")
        else:
            messagebox.showwarning("Empty", "Please enter a value")
    
    def remove_list1_item(self) -> None:
        """Remove selected item from custom list 1"""
        selection = self.list1_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.list1_listbox.get(index)
            self.list1_listbox.delete(index)
            self.custom_list1.remove(item)
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove")
    
    def clear_list1(self) -> None:
        """Clear all items from custom list 1"""
        self.list1_listbox.delete(0, tk.END)
        self.custom_list1.clear()
    
    def load_example_list1(self) -> None:
        """Load example items for custom list 1"""
        examples = ["Project", "Document", "Image", "Video", "Audio", 
                    "Archive", "Backup", "Report", "Data", "Asset"]
        for item in examples:
            if item not in self.custom_list1:
                self.custom_list1.append(item)
                self.list1_listbox.insert(tk.END, item)
    
    # --- Custom List 2 / Prefixes Management ---
    def add_list2_item(self) -> None:
        """Add an item to custom list 2"""
        item = self.list2_entry.get().strip()
        if item:
            if item not in self.custom_list2:
                self.custom_list2.append(item)
                self.list2_listbox.insert(tk.END, item)
                self.list2_entry.set("")
            else:
                messagebox.showwarning("Duplicate", f"'{item}' already exists in the list")
        else:
            messagebox.showwarning("Empty", "Please enter a value")
    
    def remove_list2_item(self) -> None:
        """Remove selected item from custom list 2"""
        selection = self.list2_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.list2_listbox.get(index)
            self.list2_listbox.delete(index)
            self.custom_list2.remove(item)
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove")
    
    def clear_list2(self) -> None:
        """Clear all items from custom list 2"""
        self.list2_listbox.delete(0, tk.END)
        self.custom_list2.clear()
    
    def load_example_list2(self) -> None:
        """Load example items for custom list 2 (prefixes)"""
        examples = ["file", "item", "doc", "img", "vid", 
                    "aud", "pkg", "bak", "tmp", "new"]
        for item in examples:
            if item not in self.custom_list2:
                self.custom_list2.append(item)
                self.list2_listbox.insert(tk.END, item)
        
    def setup_pattern_help(self, help_frame: ttk.Frame) -> None:
        help_text = """
        ═══════════════════════════════════════════════════════════════
                        FILE AND FOLDER RENAMER - PATTERN GUIDE
        ═══════════════════════════════════════════════════════════════
        
        PATTERN VARIABLES:
        
        {list1}        - Random word from Custom List 1
        {prefix}       - Random prefix from Custom List 2 + counter
        {version}      - Version number (configurable in Options)
        {counter}      - Sequential counter (001, 002, 003...)
        {date}         - Current date (YYYY-MM-DD)
        {time}         - Current time (HH-MM-SS)
        {datetime}     - Current date and time combined
        {random}       - Random number (1-1000)
        {orig_name}    - Original filename (without extension)
        {orig_ext}     - Original file extension
        
        ───────────────────────────────────────────────────────────────
        
        EXAMPLES:
        
        {list1}_{prefix}{counter}       → Project_file001
        {orig_name}_{date}              → myfile_2024-01-15
        {prefix}{counter}_v{version}    → doc001_v1.0
        backup_{datetime}_{orig_name}   → backup_2024-01-15_10-30-45_myfile
        
        ───────────────────────────────────────────────────────────────
        
        VERSION STRATEGIES:
        
        fixed          Same version for all files
        incremental    Increase version for each file (1.0, 1.1, 1.2...)
        random         Random version between 0.1 and 10.0
        
        ───────────────────────────────────────────────────────────────
        
        CASE TRANSFORMATIONS:
        
        none           Keep original case
        uppercase      CONVERT TO UPPERCASE
        lowercase      convert to lowercase
        title          Convert To Title Case
        
        ───────────────────────────────────────────────────────────────
        
        FILE FILTER EXAMPLES:
        
        *              All files
        *.txt          Only .txt files
        *.jpg,*.png    Multiple extensions (comma-separated)
        
        ───────────────────────────────────────────────────────────────
        
        TIP: Add your custom words in the "Custom Lists" tab before
        using {list1} or {prefix} patterns!
        
        ═══════════════════════════════════════════════════════════════
        """
        
        help_text_widget = tk.Text(help_frame, wrap=tk.WORD, height=30, width=70)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        
    def show_pattern_help(self) -> None:
        """Switch to the Pattern Help tab"""
        if self.notebook:
            self.notebook.select(2)  # Pattern Help is now index 2
        
    def browse_directory(self) -> None:
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            self.directory.set(directory)
            
    def matches_filter(self, filename: str) -> bool:
        """Check if filename matches the file filter pattern"""
        filter_pattern = self.file_filter.get().strip()
        if not filter_pattern or filter_pattern == "*":
            return True
        
        # Support multiple patterns separated by comma
        patterns = [p.strip() for p in filter_pattern.split(",")]
        
        for pattern in patterns:
            if pattern.startswith("*."):
                ext = pattern[1:]  # Get extension including dot
                if filename.lower().endswith(ext.lower()):
                    return True
            elif pattern == "*":
                return True
            elif "*" in pattern:
                # Simple wildcard matching
                regex_pattern = pattern.replace(".", r"\.").replace("*", ".*")
                if re.match(regex_pattern, filename, re.IGNORECASE):
                    return True
            else:
                if filename.lower() == pattern.lower():
                    return True
        return False
            
    def get_items(self) -> List[Tuple[str, str]]:
        """Get items to rename. Returns list of (relative_path, full_path) tuples."""
        directory = self.directory.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return []
        
        items: List[Tuple[str, str]] = []
        
        if self.recursive.get():
            # Recursive mode - walk through all subdirectories
            for root, dirs, files in os.walk(directory):
                rel_root = os.path.relpath(root, directory)
                
                if self.include_files.get():
                    for f in files:
                        if self.matches_filter(f):
                            full_path = os.path.join(root, f)
                            rel_path = f if rel_root == "." else os.path.join(rel_root, f)
                            items.append((rel_path, full_path))
                            
                if self.include_folders.get():
                    for d in dirs:
                        full_path = os.path.join(root, d)
                        rel_path = d if rel_root == "." else os.path.join(rel_root, d)
                        items.append((rel_path, full_path))
        else:
            # Non-recursive mode - only immediate children
            if self.include_files.get():
                for f in os.listdir(directory):
                    full_path = os.path.join(directory, f)
                    if os.path.isfile(full_path) and self.matches_filter(f):
                        items.append((f, full_path))
                        
            if self.include_folders.get():
                for f in os.listdir(directory):
                    full_path = os.path.join(directory, f)
                    if os.path.isdir(full_path):
                        items.append((f, full_path))
            
        return sorted(items, key=lambda x: x[0])
    
    def apply_case_transform(self, name: str) -> str:
        """Apply case transformation to name"""
        case = self.case_option.get()
        if case == "uppercase":
            return name.upper()
        elif case == "lowercase":
            return name.lower()
        elif case == "title":
            return name.title()
        return name
    
    def generate_new_name(self, old_name: str, counter: int, version: float, is_file: bool) -> str:
        pattern = self.pattern.get()
        name, ext = os.path.splitext(old_name)
        
        # Get current date and time
        now = datetime.now()
        
        # Replace all pattern variables
        new_name = pattern
        
        # {list1} - random word from custom list 1
        if "{list1}" in new_name:
            if self.custom_list1:
                new_name = new_name.replace("{list1}", random.choice(self.custom_list1))
            else:
                new_name = new_name.replace("{list1}", "Item")  # Fallback
            
        # {prefix} - prefix from custom list 2 with counter
        if "{prefix}" in new_name:
            if self.custom_list2:
                prefix = random.choice(self.custom_list2)
            else:
                prefix = "file"  # Fallback
            new_name = new_name.replace("{prefix}", f"{prefix}")
            
        # {version} - version number
        if "{version}" in new_name:
            new_name = new_name.replace("{version}", str(version))
            
        # {counter} - simple counter
        if "{counter}" in new_name:
            new_name = new_name.replace("{counter}", f"{counter:03d}")
            
        # {date} - current date
        if "{date}" in new_name:
            new_name = new_name.replace("{date}", now.strftime("%Y-%m-%d"))
            
        # {time} - current time
        if "{time}" in new_name:
            new_name = new_name.replace("{time}", now.strftime("%H-%M-%S"))
            
        # {datetime} - current date and time
        if "{datetime}" in new_name:
            new_name = new_name.replace("{datetime}", now.strftime("%Y-%m-%d_%H-%M-%S"))
            
        # {random} - random number
        if "{random}" in new_name:
            new_name = new_name.replace("{random}", str(random.randint(1, 1000)))
            
        # {orig_name} - original name without extension
        if "{orig_name}" in new_name:
            new_name = new_name.replace("{orig_name}", name)
            
        # {orig_ext} - original extension
        if "{orig_ext}" in new_name:
            new_name = new_name.replace("{orig_ext}", ext)
        
        # Apply case transformation
        new_name = self.apply_case_transform(new_name)
        
        # For files, preserve the original extension unless the pattern includes it
        if is_file and not os.path.splitext(new_name)[1]:
            new_name += ext
            
        return new_name
    
    def get_version(self, counter: int, strategy: str) -> float:
        """Get version number based on strategy with input validation"""
        try:
            if strategy == "fixed":
                return float(self.version_start.get())
            elif strategy == "incremental":
                start = float(self.version_start.get())
                increment = self.version_increment.get()
                return round(start + (counter - 1) * increment, 2)
            elif strategy == "random":
                return round(random.uniform(0.1, 10.0), 2)
            return 1.0
        except ValueError:
            messagebox.showerror("Error", "Invalid version format. Using default 1.0")
            return 1.0
    
    def preview(self) -> None:
        self.preview_tree.delete(*self.preview_tree.get_children())
        directory = self.directory.get()
        
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        # Check if custom data is needed
        pattern = self.pattern.get()
        if "{list1}" in pattern and not self.custom_list1:
            messagebox.showwarning("Missing Data", "Pattern uses {list1} but no items defined.\nGo to 'Custom Lists' tab to add items or load examples.")
        if "{prefix}" in pattern and not self.custom_list2:
            messagebox.showwarning("Missing Data", "Pattern uses {prefix} but no prefixes defined.\nGo to 'Custom Lists' tab to add prefixes or load examples.")
        
        items = self.get_items()
        if not items:
            messagebox.showinfo("Info", "No files or folders found to rename")
            return
        
        # Reset and configure progress bar
        if self.progress:
            self.progress['value'] = 0
            self.progress['maximum'] = len(items)
            
        counter = self.start_counter.get()
        rename_plan: List[Tuple[str, str, float]] = []
        
        for i, (rel_path, full_path) in enumerate(items):
            version = self.get_version(counter, self.version_strategy.get())
            is_file = os.path.isfile(full_path)
            
            # Get just the filename for renaming
            dirname = os.path.dirname(rel_path)
            basename = os.path.basename(rel_path)
            new_basename = self.generate_new_name(basename, counter, version, is_file)
            new_rel_path = os.path.join(dirname, new_basename) if dirname else new_basename
            
            rename_plan.append((rel_path, new_rel_path, version))
            counter += 1
            
            # Update progress
            if self.progress:
                self.progress['value'] = i + 1
                self.root.update_idletasks()
            
        for old, new, version in rename_plan:
            self.preview_tree.insert("", tk.END, values=(old, new))
            
        self.status_var.set(f"Previewing {len(rename_plan)} items")
        
    def rename(self) -> None:
        directory = self.directory.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
            
        items = self.get_items()
        if not items:
            messagebox.showinfo("Info", "No files or folders found to rename")
            return
            
        # If preview mode is on, show confirmation
        if self.preview_mode.get():
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to rename {len(items)} items?")
            if not confirm:
                return
        
        # Reset and configure progress bar
        if self.progress:
            self.progress['value'] = 0
            self.progress['maximum'] = len(items)
                
        counter = self.start_counter.get()
        renamed_count = 0
        errors: List[str] = []
        current_batch: List[Tuple[str, str]] = []  # For undo functionality
        
        for i, (rel_path, full_path) in enumerate(items):
            version = self.get_version(counter, self.version_strategy.get())
            is_file = os.path.isfile(full_path)
            
            # Get directory and filename for renaming
            parent_dir = os.path.dirname(full_path)
            basename = os.path.basename(full_path)
            new_basename = self.generate_new_name(basename, counter, version, is_file)
            new_path = os.path.join(parent_dir, new_basename)
            
            # Check if the new name already exists
            if os.path.exists(new_path):
                errors.append(f"Skipping {rel_path}: {new_basename} already exists")
                counter += 1
                continue
                
            try:
                os.rename(full_path, new_path)
                current_batch.append((new_path, full_path))  # Store for undo (new -> old)
                renamed_count += 1
            except Exception as e:
                errors.append(f"Error renaming {rel_path}: {str(e)}")
                
            counter += 1
            
            # Update progress
            if self.progress:
                self.progress['value'] = i + 1
                self.root.update_idletasks()
        
        # Save to history for undo
        if current_batch:
            self.rename_history.append(current_batch)
            
        # Update status
        if errors:
            messagebox.showerror("Errors", "\n".join(errors[:5]) + ("\n..." if len(errors) > 5 else ""))
            
        self.status_var.set(f"Renamed {renamed_count} of {len(items)} items (Undo available: {len(self.rename_history)} batches)")
        
        # Refresh preview
        self.preview()
    
    def undo_last_rename(self) -> None:
        """Undo the last batch rename operation"""
        if not self.rename_history:
            messagebox.showinfo("Info", "No actions to undo")
            return
        
        last_batch = self.rename_history.pop()
        confirm = messagebox.askyesno("Confirm Undo", f"Are you sure you want to undo {len(last_batch)} rename operations?")
        if not confirm:
            self.rename_history.append(last_batch)  # Put it back
            return
        
        # Reset and configure progress bar
        if self.progress:
            self.progress['value'] = 0
            self.progress['maximum'] = len(last_batch)
        
        undone_count = 0
        errors: List[str] = []
        
        for i, (current_path, original_path) in enumerate(last_batch):
            try:
                if os.path.exists(current_path):
                    os.rename(current_path, original_path)
                    undone_count += 1
                else:
                    errors.append(f"File not found: {current_path}")
            except Exception as e:
                errors.append(f"Error undoing {current_path}: {str(e)}")
            
            # Update progress
            if self.progress:
                self.progress['value'] = i + 1
                self.root.update_idletasks()
        
        if errors:
            messagebox.showerror("Undo Errors", "\n".join(errors[:5]) + ("\n..." if len(errors) > 5 else ""))
        
        self.status_var.set(f"Undone {undone_count} of {len(last_batch)} items (Undo available: {len(self.rename_history)} batches)")
        
        # Refresh preview
        self.preview()
        
    def clear(self) -> None:
        self.preview_tree.delete(*self.preview_tree.get_children())
        if self.progress:
            self.progress['value'] = 0
        self.status_var.set("Ready")
        
    def insert_pattern(self) -> None:
        # Create a popup for pattern insertion
        popup = tk.Toplevel(self.root)
        popup.title("Insert Pattern")
        popup.geometry("400x350")
        popup.transient(self.root)
        popup.grab_set()
        
        # Pattern selection
        ttk.Label(popup, text="Select pattern to insert:").pack(pady=10)
        
        patterns = [
            ("{list1}", "Random word from Custom List 1"),
            ("{prefix}", "Random prefix from Custom List 2"),
            ("{version}", "Version number"),
            ("{counter}", "Sequential counter (001, 002...)"),
            ("{date}", "Current date (YYYY-MM-DD)"),
            ("{time}", "Current time (HH-MM-SS)"),
            ("{datetime}", "Date and time combined"),
            ("{random}", "Random number (1-1000)"),
            ("{orig_name}", "Original filename"),
            ("{orig_ext}", "Original extension"),
        ]
        
        # Treeview for better display
        columns = ("pattern", "description")
        pattern_tree = ttk.Treeview(popup, columns=columns, show="headings", height=10)
        pattern_tree.heading("pattern", text="Pattern")
        pattern_tree.heading("description", text="Description")
        pattern_tree.column("pattern", width=100)
        pattern_tree.column("description", width=250)
        
        for pat, desc in patterns:
            pattern_tree.insert("", tk.END, values=(pat, desc))
        
        pattern_tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        
        # Button frame
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        
        def insert_selected() -> None:
            selection = pattern_tree.selection()
            if selection:
                item = pattern_tree.item(selection[0])
                pattern = item['values'][0]
                current = self.pattern.get()
                self.pattern.set(current + pattern)
            popup.destroy()
            
        ttk.Button(button_frame, text="Insert", command=insert_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedFileFolderRenamer(root)
    root.mainloop()