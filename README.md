# File and Folder Renamer

A powerful, user-friendly Python application for batch renaming files and folders using customizable patterns.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- **Pattern-Based Renaming** - Use flexible patterns like `{list1}_{prefix}{counter}_v{version}`
- **Custom Word Lists** - Define your own word lists for dynamic naming
- **Undo Support** - Safely revert rename operations
- **Preview Mode** - See changes before applying them
- **Recursive Processing** - Process files in subdirectories
- **File Filtering** - Filter by extension (e.g., `*.txt`, `*.jpg,*.png`)
- **Case Transformation** - Convert to uppercase, lowercase, or title case
- **Version Numbering** - Fixed, incremental, or random versioning
- **Progress Indicator** - Visual feedback for large operations

## 📸 Screenshot

![File and Folder Renamer Screenshot](screenshot.png)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python)

### Running the Application

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/file-folder-renamer.git

# Navigate to the directory
cd file-folder-renamer

# Run the application
python File_and_Folder_Renamer.py
```

## 📖 Usage

### Basic Steps

1. **Select Directory** - Click "Browse" to choose a folder
2. **Set Pattern** - Define your renaming pattern
3. **Add Custom Data** - Go to "Custom Lists" tab to add your words
4. **Preview** - Click "Preview" to see the changes
5. **Rename** - Click "Rename" to apply changes

### Pattern Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{list1}` | Random word from Custom List 1 | Project |
| `{prefix}` | Random prefix from Custom List 2 | file |
| `{counter}` | Sequential counter | 001, 002, 003 |
| `{version}` | Version number | 1.0, 1.1, 1.2 |
| `{date}` | Current date | 2024-01-15 |
| `{time}` | Current time | 10-30-45 |
| `{datetime}` | Date and time | 2024-01-15_10-30-45 |
| `{random}` | Random number (1-1000) | 547 |
| `{orig_name}` | Original filename | myfile |
| `{orig_ext}` | Original extension | .txt |

### Example Patterns

```
{list1}_{prefix}{counter}         → Project_file001.txt
{orig_name}_{date}                → myfile_2024-01-15.txt
{prefix}{counter}_v{version}      → doc001_v1.0.txt
backup_{datetime}_{orig_name}     → backup_2024-01-15_10-30-45_myfile.txt
```

## ⚙️ Options

### Version Strategies

- **Fixed** - Same version for all files
- **Incremental** - Increase version for each file (1.0, 1.1, 1.2...)
- **Random** - Random version between 0.1 and 10.0

### Case Transformations

- **None** - Keep original case
- **Uppercase** - CONVERT TO UPPERCASE
- **Lowercase** - convert to lowercase
- **Title** - Convert To Title Case

### File Filters

- `*` - All files
- `*.txt` - Only .txt files
- `*.jpg,*.png` - Multiple extensions

## 🔧 Advanced Features

### Undo Functionality

Made a mistake? Click "Undo Last" to revert the most recent rename batch.

### Recursive Mode

Enable "Recursive (Include Subdirectories)" to process files in all subdirectories.

### Custom Lists

Add your own words in the "Custom Lists" tab:

- **Custom List 1** - Words used with `{list1}` pattern
- **Custom List 2** - Prefixes used with `{prefix}` pattern

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

If you have any questions or suggestions, please open an issue on GitHub.

---

⭐ **If you find this tool useful, please give it a star!**
