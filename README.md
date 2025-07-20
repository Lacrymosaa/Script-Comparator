# Script Function Comparator for Ruby or Python Files

This tool compares Ruby (`.rb`) or Python (`.py`) script files between two folders. It detects and reports changes in the contents of individual `def` blocks (functions), ignoring string literals and comments for a cleaner comparison.

Primarily designed to assist in tracking differences between versions of Pokémon Essentials scripts, but flexible enough to be adapted to Python code as well.

## Features

- Compares functions (`def`) across `.rb` files with matching filenames in two folders.
- Ignores:
  - String literals (`"like this"`)
  - Line comments (anything after `#`)
- Detects:
  - Modified functions (shows line-by-line diff)
  - Missing or new functions
- Outputs a full changelog to a `.txt` file

## Usage

1. Place your two folders of `.rb` files in the same directory as the script.
2. Set the folder names in the `__main__` section of the script:

```python
folder1 = "19.1"
folder2 = "21.1"
