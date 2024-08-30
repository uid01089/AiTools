#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the virtual environment and Python file paths
VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON_FILE="$SCRIPT_DIR/CommentPythonFile.py"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Error: Virtual environment not found in $VENV_DIR. Please create a virtual environment in the .venv directory."
  exit 1
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Check if the Python file exists
if [ ! -f "$PYTHON_FILE" ]; then
  echo "Error: Python file 'CommentPythonFile.py' not found in $SCRIPT_DIR."
  exit 1
fi

# Check if an argument was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <file>"
  exit 1
fi

# Run the Python file with the provided argument
python "$PYTHON_FILE" --file "$1"

# Deactivate the virtual environment
deactivate
