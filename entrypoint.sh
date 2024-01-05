#!/usr/bin/env bash

# Function to check if clang-format is installed
check_clang_format() {
    if ! command -v /usr/bin/clang-format-11 &> /dev/null; then
        echo "clang-format-11 not found, please install it."
        exit 3
    fi
}

# Function to format a file and check for differences
format_diff() {
    local filepath="$1"
    local format_output

    format_output=$(/usr/bin/clang-format-11 -n --Werror --style=file --fallback-style=LLVM "${filepath}" 2>&1)
    local format_status=$?

    if [[ "${format_status}" -ne 0 ]]; then
        echo "Formatting issue found in ${filepath}:"
        echo "${format_output}"
        exit_code=1  # Indicate that an issue was found
    fi
}

# Function to parse and set include and exclude paths
set_paths() {
    include_paths="${INPUT_INCLUDE_FOLDERS:-.}"
    local exclude_paths_string="${INPUT_EXCLUDE_FOLDERS:-3rdparty,3rd_party}"

    IFS=',' read -r -a exclude_paths <<< "$exclude_paths_string"
}

# Function to find and check files
find_and_check_files() {
    while IFS= read -r -d '' file; do
        format_diff "$file"
    done < <(find "$include_paths" "${exclude_paths[@]/#/-path }" -prune -o -name '*.h' -print0 -o -name '*.cpp' -print0)
    local find_status=$?

    if [[ "${find_status}" -ne 0 ]]; then
        echo "Find command failed with status ${find_status}"
        exit_code=1  # Indicate that an issue was found
    fi
}

# Main execution
main() {
    check_clang_format

    set_paths

    # Ensure the script is running in the GitHub workspace
    if ! cd "$GITHUB_WORKSPACE"; then
        echo "Failed to enter $GITHUB_WORKSPACE"
        exit 2
    fi

    # Initialize exit code
    exit_code=0

    find_and_check_files

    # Exit with the determined status
    exit "$exit_code"
}

main "$@"
