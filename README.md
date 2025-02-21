# Recursive File Scanner with Regex Matching

## Overview
This project provides a Python-based file scanner that recursively scans a specified directory and its subdirectories for text files matching a given regex pattern. It is built using object-oriented programming with a focus on robust error handling and efficient text processing.

## Features
- **Recursive Directory Search:** Scans all subdirectories within the provided destination directory.
- **File Type Detection:**
  - **Text files:** Processed using UTF-8 encoding with error handling.
  - **Binary files:** Detected by reading the first 1024 bytes and checking for non-printable characters.
  - **Executable files:** Skipped by checking execute permissions on Unix and common executable extensions on Windows.
- **Regex Functionality:**
  - Uses a default regex pattern defined in an external `config.json` file.
  - Supports custom regex patterns via a command line parameter.
  - Finds **all** matches within each file.
- **Progress Display:** Uses a `tqdm` progress bar that shows the number of processed files and percentage completion.
- **Output Options:**
  - Results (file path, filename, and matches) can be printed to standard output.
  - Optionally, results can be written to a specified output file.
- **Error Handling:** Robust logging for file system errors, encoding issues, invalid regex patterns, and access restrictions.

## Installation

1. **Clone the repository** or download the code files.
2. **Install the required dependencies:**

   ```bash
   pip install tqdm

Usage

Run the scanner from the command line:

python scanner.py <destination_directory> [--regex CUSTOM_REGEX] [--output OUTPUT_FILE] [--config CONFIG_FILE]

Parameters:

    <destination_directory>: (Required) The directory to scan.
    --regex: (Optional) Custom regex pattern to use. This overrides the default regex from the configuration file.
    --output: (Optional) Specify an output file to write results. If omitted, results are printed to the console.
    --config: (Optional) Path to the configuration JSON file. Defaults to config.json.

Examples:

    Scan a directory using the default regex:

python scanner.py /path/to/directory

Scan a directory with a custom regex and output results to a file:

    python scanner.py /path/to/directory --regex "\\b(custom_pattern)\\b" --output results.txt

Configuration File (config.json)

The configuration file should be in JSON format and include the default regex pattern. For example:

{
  "default_regex": "\\b(?:\\d{6}-){7}\\d{6}\\b"
}

This default pattern matches a string in the format:
XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX
where each X is a digit.
Code Structure

    scanner.py: Main Python file containing the FileScanner class and CLI logic.
    config.json: JSON configuration file for default regex settings.
    README.md: This documentation file.

Code Quality

    The code is written in a modular, object-oriented style with clear separation of concerns.
    It is fully type hinted and PEP 8 compliant.
    Robust error handling is in place to ensure the scanner logs issues and continues processing.
    Efficient memory utilization and high-performance regex matching are emphasized.

License

GNU General Public License (GPL)
