#!/usr/bin/env bash

format_diff(){
    local filepath="$1"
    local_format="$(/usr/bin/clang-format-10 -n --Werror --style=file --fallback-style=LLVM "${filepath}")"
    local format_status="$?"
    if [[ "${format_status}" -ne 0 ]]; then
        echo "$local_format" >&2
        exit_code=1
        return "${format_status}"
    fi
    return 0
}

cd "$GITHUB_WORKSPACE" || exit 2

# initialize exit code
exit_code=0

# Find files
FILES=$(find src -path src/out -prune -o -path src/utils -prune -o -name \*.h -print -o -name \*.cpp  -print)

# Сheck style in files
for FILE in $FILES; do
    format_diff "${FILE}"
done

exit "$exit_code"
