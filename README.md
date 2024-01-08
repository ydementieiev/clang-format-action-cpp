
# Clang-Format Code Style Action for C++

This GitHub Action applies `clang-format` to check the formatting of your C++ codebase. It's designed to ensure your code adheres to a consistent style by checking it against the formatting rules defined in your `.clang-format` file.

This check will be performed on every push, and you can see the results even on your pull requests.
<img width="450" alt="pr" src="https://github.com/ydementieiev/clang-format-action-cpp/assets/57259850/75ef9afe-4a80-41a5-9dc4-4c75b5fa3760">

## Usage

To integrate this action into your workflow, add a `.github/workflows/clang-format-check.yml` file to your repository with the following content:

```yaml
name: clang-format Check
on: [push]
jobs:
  formatting-check:
    name: Formatting Check
    runs-on: ubuntu-20.04
    steps:
    - uses: actions/checkout@v2
    - name: Run clang-format style check for Cpp programs.
      uses: ydementieiev/clang-format-action-cpp@master
      with:
        include_folders: 'src,include'               # Optional.
        exclude_folders: 'src/3rdparty,src/external' # Optional.
        style_guide: 'some_folder/.clang-format'     # Optional.
```

This configuration will trigger the clang-format check on every push to the repository. It will check files in the `include_folders` directories, while excluding any files found in `exclude_folders`. But you can customize folders as described below.

### Inputs

- `include_folders`: Comma-separated list of folders to include in the formatting check. It's not required and default is `'./'`.
- `exclude_folders`: Comma-separated list of folders to exclude from the formatting check. It's not required and default is `''`.
- `style_guide`: Path to the clang-format style guide file. Adjust if your style guide file is located elsewhere. It's not required and defaults to `.clang-format` at the project's root.

## Contributing

Contributions to improve this action are welcome! Feel free to open issues or submit pull requests.
