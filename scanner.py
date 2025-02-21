#!/usr/bin/env python3
"""
Recursive File Scanner with Regex Matching

Scans a destination directory recursively for text files and searches for all matches
of a regex pattern. The default regex pattern is loaded from an external JSON configuration file.
Binary files and executable files are skipped.
"""

import os
import re
import argparse
import logging
import json
import sys
import stat
import string
from tqdm import tqdm
from typing import List, Optional, Pattern

class FileScanner:
    """
    A class to recursively scan directories and search files for regex matches.
    """

    def __init__(self, directory: str, regex_pattern: str, output_file: Optional[str] = None) -> None:
        """
        Initialize the scanner.

        :param directory: Destination directory to scan.
        :param regex_pattern: Regex pattern to search in files.
        :param output_file: Optional output file to write results.
        """
        self.directory = directory
        self.regex_pattern = regex_pattern
        try:
            self.compiled_pattern: Pattern = re.compile(regex_pattern)
        except re.error as err:
            logging.error(f"Invalid regex pattern: {regex_pattern}. Error: {err}")
            raise ValueError(f"Invalid regex pattern: {regex_pattern}") from err
        self.output_file = output_file
        self.results: List[str] = []

    def is_binary(self, file_path: str) -> bool:
        """
        Check if a file is binary by reading its first 1024 bytes and analyzing the ratio
        of non-printable characters.

        :param file_path: Path to the file.
        :return: True if file is binary, else False.
        """
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
            if not chunk:
                return False
            # Build a set of printable ASCII bytes
            printable = set(bytes(string.printable, 'ascii'))
            non_printable = [b for b in chunk if b not in printable]
            # If more than 30% of the bytes are non-printable, consider it binary.
            if len(non_printable) / len(chunk) > 0.30:
                return True
            return False
        except Exception as e:
            logging.error(f"Error checking if file is binary: {file_path}. Error: {e}")
            return True

    def is_executable(self, file_path: str) -> bool:
        """
        Determine if a file is executable.
        On Unix-like systems, checks the execute permission.
        On Windows, checks for common executable extensions.

        :param file_path: Path to the file.
        :return: True if the file is executable, else False.
        """
        try:
            if os.name == 'nt':
                # Check for common Windows executable extensions.
                executable_extensions = {'.exe', '.bat', '.cmd', '.com'}
                ext = os.path.splitext(file_path)[1].lower()
                return ext in executable_extensions
            else:
                # Check execute permission on Unix-like systems.
                return os.access(file_path, os.X_OK)
        except Exception as e:
            logging.error(f"Error checking if file is executable: {file_path}. Error: {e}")
            return False

    def process_file(self, file_path: str) -> None:
        """
        Process a single file: open it as UTF-8 text (ignoring errors), search for all regex matches,
        and record the result if matches are found.

        :param file_path: Path to the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            matches = self.compiled_pattern.findall(content)
            if matches:
                formatted_result = (f"Path: {file_path} | Filename: {os.path.basename(file_path)} "
                                    f"| Matches: {matches}")
                self.results.append(formatted_result)
        except Exception as e:
            logging.error(f"Error processing file: {file_path}. Error: {e}")

    def scan(self) -> None:
        """
        Recursively scan the directory for files. All files (including those skipped) are counted in
        the progress bar.
        """
        all_files: List[str] = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                full_path = os.path.join(root, file)
                all_files.append(full_path)
        total_files = len(all_files)
        logging.info(f"Found {total_files} files in {self.directory}")

        for file_path in tqdm(all_files, total=total_files, desc="Processing files"):
            # Skip binary files
            if self.is_binary(file_path):
                continue
            # Skip executable files
            if self.is_executable(file_path):
                continue
            self.process_file(file_path)

    def output_results(self) -> None:
        """
        Output the scan results either to standard output or write them to the specified output file.
        """
        if self.output_file:
            try:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    for line in self.results:
                        f.write(line + "\n")
                logging.info(f"Results written to {self.output_file}")
            except Exception as e:
                logging.error(f"Error writing to output file: {self.output_file}. Error: {e}")
        else:
            for line in self.results:
                print(line)

def load_config(config_path: str = "config.json") -> dict:
    """
    Load configuration from a JSON file.

    :param config_path: Path to the configuration file.
    :return: Dictionary with configuration settings.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading configuration file: {config_path}. Error: {e}")
        return {}

def setup_logging() -> None:
    """
    Set up logging to display messages to standard error.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)]
    )

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Recursive File Scanner with Regex Matching"
    )
    parser.add_argument(
        "destination",
        type=str,
        help="Destination directory to scan"
    )
    parser.add_argument(
        "--regex",
        type=str,
        help="Custom regex pattern to use. Overrides default configuration."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file to write results. If not specified, prints to standard output."
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to the configuration JSON file containing default regex."
    )
    return parser.parse_args()

def main() -> None:
    """
    Main entry point: parse arguments, load configuration, create a FileScanner instance,
    perform the scan, and output results.
    """
    setup_logging()
    args = parse_arguments()
    config = load_config(args.config)
    # Load the default regex pattern from the configuration file.
    default_regex = config.get("default_regex", r"\b(?:\d{6}-){7}\d{6}\b")
    regex_pattern = args.regex if args.regex else default_regex

    scanner = FileScanner(
        directory=args.destination,
        regex_pattern=regex_pattern,
        output_file=args.output
    )
    scanner.scan()
    scanner.output_results()

if __name__ == "__main__":
    main()
