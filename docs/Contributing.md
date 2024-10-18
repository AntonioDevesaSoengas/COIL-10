# Contributing

## Contributing Guidelines

### Introduction

This document outlines the guidelines for contributing to the development of a Python application that allows users to create and visualize simple and multiple linear regression models using CSV, Excel, and SQLite files. The project will also support saving and loading models, as well as making predictions. All work follows Agile methodology and the Scrum framework.

### Getting Started

To contribute to this project, ensure you have the following tools installed:

- **Python 3.x**
- **Git**
- **Libraries:** Pandas, Scikit-learn, Matplotlib (for handling models and visualization)
- **SQLite3** (for database handling)
- **Tkinter** (for the graphical user interface)
- **Taiga account** (for Scrum management)

### Contribution Workflow

#### 1. Branching Strategy

We follow the GitFlow branching model:

- **main:** Contains stable, production-ready code.
- **develop:** Contains the latest development work.
- **feature/[feature-name]:** For each new feature or task, create a feature branch from the develop branch.

All work must be committed and pushed to feature branches and only integrated into `develop` through pull requests (PRs) after review.

#### 2. Commit Messages

Use clear and concise commit messages, following this structure:

- **feat:** For new features (e.g., `feat: Add CSV import functionality`).
- **fix:** For bug fixes (e.g., `fix: Correct CSV file parser issue`).
- **docs:** For documentation updates (e.g., `docs: Update contributing.md`).
- **test:** For adding or modifying tests (e.g., `test: Add unit tests for regression model`).

#### 3. Pull Requests (PRs)

Once your feature is ready, push your branch to the remote repository and create a pull request from your feature branch to the `develop` branch. Ensure the following before submitting:

- The feature is fully implemented and tested.
- Documentation has been updated where necessary.
- Include a brief description of the changes in the PR.

At least one team member must review and approve the PR before merging it into `develop`.

#### 4. Scrum Practices

We follow Scrum practices, including:

- **Daily stand-ups:** We hold daily meetings to discuss progress and blockers.
- **Sprint planning:** Tasks are assigned at the start of each sprint.
- **Sprint reviews and retrospectives:** At the end of each sprint, we review completed work and discuss improvements.

#### 5. Issue Tracking

We use Taiga to manage the Scrum board and track issues. All tasks are logged and updated in the system. Ensure you regularly update your progress on the board.

#### 6. Code Style Guidelines

Follow the PEP8 guidelines for Python code:

- **Indentation:** Use 4 spaces for indentation.
- **Line length:** Limit all lines to a maximum of 79 characters.
- **Use descriptive names for variables and functions.**
- **Document all functions and methods with docstrings.**

#### 7. Testing

All features must be accompanied by unit tests. Ensure your tests cover both normal and edge cases. Use `unittest` or `pytest` frameworks. Ensure all tests pass before creating a pull request.

#### 8. How to Report Bugs

If you encounter a bug, please report it by creating an issue in the GitHub repository. Include:

- A clear description of the problem.
- Steps to reproduce the issue.
- Expected vs. actual behavior.
- Any error messages or logs if available.

#### 9. Coding Etiquette

- Be respectful when giving feedback in code reviews.
- Help fellow team members when they encounter blockers.
- Keep the repository clean—delete branches after merging and avoid cluttering the project with unnecessary files.

### Role of Seneca Member

The team member from the Seneca program has the additional responsibility of documenting the progress and features of the project in the `README.md` file. This documentation will include:

- **Installation/Deployment Guide:** Instructions on how to install and run the application.
- **User Manual:** With screenshots explaining how to use the application to perform its functionalities.

The Seneca member must also ensure that the documentation in the `README.md` is always updated and clear for other users and contributors.

### Conclusion

By following these guidelines, we will maintain a productive and organized collaborative environment, ensuring high-quality code delivery and the project's progress as planned. Thank you for contributing!
