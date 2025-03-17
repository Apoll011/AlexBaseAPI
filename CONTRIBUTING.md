# Contributing to Alex Base API

Thank you for your interest in contributing to Alex Base API! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please be kind and constructive in your communications.

## How to Contribute

### Reporting Bugs

Before submitting a bug report:
1. Check the [issue tracker](https://github.com/Apoll011/Alex-Base-API/issues) to avoid duplicates
2. Update to the latest version to see if your issue has already been resolved

When reporting a bug, please include:
- A clear and descriptive title
- Steps to reproduce the behavior
- Expected vs. actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, Docker version)
- Any additional context that might be helpful

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:
1. Use a clear and descriptive title
2. Describe the current behavior and explain the behavior you'd like to see
3. Explain why this enhancement would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch from `main` for your feature or bugfix
3. Make your changes, adhering to the project's coding style
4. Add or update tests as necessary
5. Ensure the test suite passes
6. Update documentation if needed
7. Submit a pull request

## Development Setup

### Local Development

1. Fork and clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/Alex-Base-API.git
cd Alex-Base-API
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Download required language models
```bash
python -m snips_nlu download-language-entities pt_pt
python -m snips_nlu download-language-entities en
```

### Docker Development

1. Build the Docker image
```bash
docker build -t alex-server-dev .
```

2. Run the container in development mode
```bash
docker run -p 1178:1178 -v $(pwd):/app alex-server-dev
```

## Coding Guidelines

- Follow PEP 8 style guidelines for Python code
- Write clear, commented code
- Add docstrings to all functions, classes, and modules
- Keep functions small and focused on a single task
- Use descriptive variable and function names

## Testing

- Add tests for new features or bug fixes
- Run the full test suite before submitting a pull request
- Make sure all tests pass before submitting

## Documentation

- Update the README.md if you change functionality
- Add comments to complex code sections
- Update API documentation when endpoints change
- Document new features and changes in the pull request description

## Versioning

We follow [Semantic Versioning](https://semver.org/) for this project:
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward-compatible manner
- PATCH version for backward-compatible bug fixes

## Licensing

By contributing to Alex Base API, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

Thank you for your contributions!
