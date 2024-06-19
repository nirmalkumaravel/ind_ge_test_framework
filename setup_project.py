import os
import subprocess
import sys
import platform

# Define the project structure
project_structure = [
    "my_great_expectations_project/data/raw",
    "my_great_expectations_project/data/processed",
    "my_great_expectations_project/data/expectations",
    "my_great_expectations_project/notebooks",
    "my_great_expectations_project/tests",
    "my_great_expectations_project/great_expectations/checkpoints",
    "my_great_expectations_project/great_expectations/expectations",
    "my_great_expectations_project/great_expectations/validations",
    "my_great_expectations_project/great_expectations/uncommitted",
    "my_great_expectations_project/scripts",
]

# Create directories
for directory in project_structure:
    os.makedirs(directory, exist_ok=True)

# Create .gitignore
gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class

# Virtual Environment
venv/

# Great Expectations uncommitted files
great_expectations/uncommitted/

# Logs
*.log

# Jupyter Notebook checkpoints
.ipynb_checkpoints/
"""

with open("my_great_expectations_project/.gitignore", "w") as f:
    f.write(gitignore_content)

# Create requirements.txt
requirements_content = """great_expectations
pytest
"""

with open("my_great_expectations_project/requirements.txt", "w") as f:
    f.write(requirements_content)

# Create pytest.ini
pytest_ini_content = """[pytest]
testpaths = tests
python_files = test_*.py
"""

with open("my_great_expectations_project/pytest.ini", "w") as f:
    f.write(pytest_ini_content)

# Create README.md
with open("my_great_expectations_project/README.md", "w") as f:
    f.write("# My Great Expectations Project\n")

# Create data validation script
data_validation_script_content = """import great_expectations as ge
from great_expectations.checkpoint import SimpleCheckpoint

def validate_data():
    context = ge.data_context.DataContext()

    checkpoint_config = {
        "name": "my_checkpoint",
        "config_version": 1.0,
        "class_name": "SimpleCheckpoint",
        "batches": [
            {
                "batch_kwargs": {
                    "path": "data/processed/my_dataset.csv",
                    "datasource": "my_datasource"
                },
                "expectation_suite_names": ["default"]
            }
        ]
    }
    context.add_checkpoint(**checkpoint_config)
    results = context.run_checkpoint(checkpoint_name="my_checkpoint")
    return results

if __name__ == "__main__":
    validation_results = validate_data()
    print(validation_results)
"""

with open("my_great_expectations_project/scripts/data_validation.py", "w") as f:
    f.write(data_validation_script_content)

# Create test script
test_script_content = """import pytest
from scripts.data_validation import validate_data

def test_data_validation():
    results = validate_data()
    assert results["success"] is True
"""

with open("my_great_expectations_project/tests/test_data_validation.py", "w") as f:
    f.write(test_script_content)

# Determine the python executable
python_executable = sys.executable

# Initialize a virtual environment
subprocess.run([python_executable, "-m", "venv", "my_great_expectations_project/venv"])

# Activate the virtual environment and install dependencies
venv_activate = os.path.join("my_great_expectations_project", "venv", "Scripts", "activate") if platform.system() == "Windows" else os.path.join("my_great_expectations_project", "venv", "bin", "activate")

# Create a batch script to activate the virtual environment and install dependencies
activation_script_content = f"""
source {venv_activate}
pip install -r my_great_expectations_project/requirements.txt
great_expectations init -y
"""

with open("my_great_expectations_project/setup.sh" if platform.system() != "Windows" else "my_great_expectations_project/setup.bat", "w") as f:
    f.write(activation_script_content)

# Print instructions for the user to finish the setup
print("Project setup script has been created.")
if platform.system() == "Windows":
    print("Please run 'my_great_expectations_project\\setup.bat' to complete the setup.")
else:
    print("Please run 'sh my_great_expectations_project/setup.sh' to complete the setup.")
