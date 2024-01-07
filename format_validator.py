#!/usr/bin/env python3
import os
import subprocess
import glob
import logging
import shutil

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global constant for the expected clang-format path (used as a fallback)
actual_clang_format_path = None


def check_clang_format():
    """Check if clang-format is installed."""
    global actual_clang_format_path

    # Check if clang-format is in system PATH
    actual_clang_format_path = shutil.which("clang-format-11") or "/usr/bin/clang-format-11"

    if os.path.isfile(actual_clang_format_path):
        logging.info(f"clang-format-11 found at {actual_clang_format_path}")
    else:
        logging.error("clang-format-11 not found in the system PATH or the expected path, please install it.")
        exit(3)


def verify_code_style(filepath):
    """Format a file and check for differences."""
    logging.info(f"Checking formatting for {filepath}...")

    try:
        format_output = subprocess.run([actual_clang_format_path, "-n", "--Werror", "--style=file",
                                        "--fallback-style=LLVM", filepath], capture_output=True, text=True)

        if format_output.returncode != 0:
            logging.error(f"Formatting issue found in {filepath}:")
            # logging.error(format_output.stderr)
            return 1

        logging.info(f"No formatting issues found in {filepath}.")
        return 0

    except Exception as e:
        logging.error(f"Failed to run clang-format on {filepath}: {e}")
        return 1


def get_include_exlude_paths():
    """Parse and set include and exclude paths."""
    # Get environment variable for include paths or default to '.' if empty/undefined
    include_paths_env = os.getenv('INPUT_INCLUDE_FOLDERS', '.').strip()
    include_paths = [os.path.normpath(path.strip()) for path in include_paths_env.split(',')] if include_paths_env else ['.']

    # Get environment variable for exclude paths or default to an empty list if empty/undefined
    exclude_paths_env = os.getenv('INPUT_EXCLUDE_FOLDERS', '').strip()
    exclude_paths = [os.path.normpath(path.strip()) for path in exclude_paths_env.split(',')] if exclude_paths_env else []

    # Ensure the current directory is not inadvertently excluded
    exclude_paths = [path for path in exclude_paths if path != "."]

    logging.info(f"Include paths set to: {include_paths}")
    logging.info(f"Exclude paths set to: {exclude_paths}")

    return include_paths, exclude_paths


def find_files(include_paths, exclude_paths):
    """Gather all .h and .cpp files from include paths excluding the exclude paths."""
    files_to_check = []

    for path in include_paths:
        for extension in ["**/*.h", "**/*.cpp", "**/*.cxx", "**/*.hpp"]:
            for file in glob.glob(f"{path}/{extension}", recursive=True):
                if not any(os.path.normpath(exclude) in os.path.normpath(file) for exclude in exclude_paths):
                    files_to_check.append(file)

    return files_to_check


def check_files(files_to_check):
    """Check the formatting of the files."""
    exit_code = 0

    for file in files_to_check:
        result = verify_code_style(file)
        if result != 0:
            exit_code = 1

    return exit_code


def find_and_check_files(include_paths, exclude_paths):
    """Find and check files for formatting."""
    files_to_check = find_files(include_paths, exclude_paths)
    return check_files(files_to_check)


if __name__ == "__main__":
    """Main execution function."""
    logging.info("Starting clang-format check...")

    check_clang_format()

    include_paths, exclude_paths = get_include_exlude_paths()

    try:
        os.chdir(os.getenv('GITHUB_WORKSPACE', '.'))
        logging.info(f"Changed directory to {os.getenv('GITHUB_WORKSPACE')}.")
    except Exception as e:
        logging.error(f"Failed to enter GITHUB_WORKSPACE: {e}")
        exit(2)

    logging.info(f"Started file checking")
    exit_code = find_and_check_files(include_paths, exclude_paths)

    if exit_code == 0:
        logging.info("clang-format check completed successfully.")
    else:
        logging.error("clang-format check completed with formatting issues.")

    exit(exit_code)
