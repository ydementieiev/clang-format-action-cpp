# clang-format-action-cpp
# Usage

To use this action, create a `.github/workflows/clang-format-check.yml` in your repository containing:

```
name: clang-format Check
on: [push]
jobs:
  formatting-check:
    name: Formatting Check
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run clang-format style check for Cpp programs.
      uses: ydementieiev/clang-format-action-cpp@master
```
