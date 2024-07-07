# G.U.T.S.: Gatherer for Unacomplished Tool Specifications

![linting: pylint](https://github.com/arnaizaitor/pyguts/actions/workflows/pylint.yml/badge.svg)
![linting: flake8](https://github.com/arnaizaitor/pyguts/actions/workflows/flake8.yml/badge.svg)
![code style: black](https://github.com/arnaizaitor/pyguts/actions/workflows/black.yml/badge.svg)
![code quality: coverage](https://github.com/arnaizaitor/pyguts/actions/workflows/coverage.yml/badge.svg)
![tests: pytest](https://github.com/arnaizaitor/pyguts/actions/workflows/pytest.yml/badge.svg)

<p align="center">
    <img src="./_static/header.png">
</p>

## Security Requirements

1. Dependency Management:

All dependencies must be listed in a requirements.txt or Pipfile.
Dependencies should be updated regularly to patch known vulnerabilities.
Use a dependency checker (e.g., safety or pip-audit) to ensure no vulnerable packages are used.

2. Static Code Analysis:

Integrate static code analysis tools (e.g., bandit) to detect common security issues in Python code.
Ensure all critical issues are resolved before deployment.

3. Secrets Management:

Ensure no hardcoded secrets (API keys, passwords) are present in the source code.
Use environment variables or a secrets management tool (e.g., AWS Secrets Manager, HashiCorp Vault).

4. Secure Coding Practices:

Follow the OWASP Python Security Guidelines.
Avoid using deprecated or insecure libraries and functions.

5. Input Validation and Sanitization:

Validate and sanitize all inputs to prevent injection attacks.
Use libraries like marshmallow for serialization and validation.

6. Logging and Monitoring:

Implement structured logging using libraries like structlog.
Ensure logs do not contain sensitive information.
Integrate with monitoring tools to track anomalies and potential security incidents.

## Quality Requirements

1. Code Style and Linting:

Adhere to PEP 8 guidelines.
Use a linter (e.g., flake8 or pylint) to enforce coding standards.
Include a configuration file for the linter (e.g., .flake8 or .pylintrc).

2. Unit Testing:

Write unit tests for all critical functionalities using unittest or pytest.
Ensure a minimum code coverage threshold (e.g., 80%) using a coverage tool (coverage.py).

3. Documentation:

Include docstrings for all modules, classes, and functions (following PEP 257).
Provide a README.md with an overview, installation instructions, usage examples, and contribution guidelines.

4. Continuous Integration (CI):

Set up a CI pipeline (e.g., GitHub Actions, GitLab CI, Jenkins) to automate testing and linting.
Ensure that all tests pass and code meets quality standards before merging.

5. Version Control:

Use version control (e.g., Git) with meaningful commit messages.
Follow a branching strategy (e.g., GitFlow) for managing feature development and releases.

## Python Tool Template
Here's a template for a Python tool that incorporates the above requirements:

Project Structure

    my_python_tool/
    ├── my_tool/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── utils.py
    │   └── config.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_main.py
    │   └── test_utils.py
    ├── .flake8
    ├── .pylintrc
    ├── .gitignore
    ├── requirements.txt
    ├── Pipfile
    ├── README.md
    └── setup.py
