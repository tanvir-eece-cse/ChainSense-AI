# Contributing to ChainSense-AI

First off, thank you for considering contributing to ChainSense-AI! It's people like you that make this project better.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots)
- **Describe the expected behavior**
- **Include your environment details** (OS, Python version, Node.js version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any additional context** (mockups, examples from other projects)

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Git

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Running Tests

```bash
# Backend tests
cd backend
pytest --cov=app tests/

# Frontend tests
cd frontend
npm run test

# Lint checks
cd backend && black . && isort . && flake8
cd frontend && npm run lint
```

## Style Guidelines

### Python Style Guide

- Follow PEP 8
- Use Black for formatting
- Use isort for import sorting
- Maximum line length: 100 characters
- Use type hints

### TypeScript/React Style Guide

- Use ESLint with the provided configuration
- Use Prettier for formatting
- Prefer functional components with hooks
- Use TypeScript strict mode

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests when relevant

### Branch Naming

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring

## Review Process

1. All submissions require review
2. Reviews may suggest changes
3. Address feedback and update the PR
4. Once approved, the PR will be merged

## Questions?

Feel free to contact the maintainer:
- **Md. Tanvir Hossain**
- Email: tanvir.eece.mist@gmail.com
- LinkedIn: [tanvir-eece](https://www.linkedin.com/in/tanvir-eece/)

Thank you for contributing! 🎉
