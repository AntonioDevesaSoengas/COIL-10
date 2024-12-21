# Contributing Guidelines

## Introduction

This document outlines the guidelines for contributing to **RegressionMaker**, a Python application that allows users to create and visualize both simple and multiple linear regression models using data from CSV, Excel, and SQLite files. The project also supports saving and loading models, as well as making predictions. Development follows Agile methodology with the Scrum framework.

---

## Getting Started

To contribute, ensure you have the following tools installed:

- **Python 3.x**
- **Git**
- Libraries: `Pandas`, `Scikit-learn`, `Matplotlib`, `PyQt5`
- **SQLite3**: For managing SQLite files.
- **GitHub Account**: To collaborate on the repository.
- **Taiga Account**: For Scrum-based task management.

### Initial Setup:
1. Clone the repository:
   ```bash
   git clone https://github.com/AntonioDevesaSoengas/COIL-10.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Contribution Workflow

### 1. Branching Strategy

We use a simplified GitFlow branching model:
- **main**: Stable, production-ready code.
- **develop**: The branch where all new development is merged.
- **feature/[feature-name]**: Create feature branches from `develop` for new tasks or features.

**Rules:**
- Always work on a feature branch created from `develop`.
- Merge into `develop` only through pull requests (PRs) after a review.

---

### 2. Commit Messages

Follow a clear and consistent commit message format:
```
<type>(<module>): <short description>
Ref: #<issue-number>
```

#### Common Types:
- **feat**: For new features.
- **fix**: For bug fixes.
- **docs**: For documentation updates.
- **style**: For code formatting or style changes.
- **refactor**: For code improvements without adding features.

**Examples:**
```
feat(ui): add dropdown for column selection
Ref: #15

fix(data_preparation): handle missing values correctly
Ref: #22

refactor(model_management): optimize model saving logic
Ref: #30
```

---

### 3. Pull Requests (PRs)

When your feature is ready:
1. Push your branch to the remote repository.
2. Open a pull request to merge your branch into `develop`.
3. Ensure the following:
   - The feature is fully implemented and tested.
   - Documentation is updated if necessary.
   - The PR includes a clear description of changes.
   - At least one team member reviews and approves your PR.

---

## Scrum Practices

We follow **Scrum practices** to ensure efficient collaboration:
- **Sprint planning**: Define goals and assign tasks for each sprint.
- **Continuous updates**: Use Taiga to notify the team about progress and blockers.
- **Sprint review**: At the end of each sprint, review completed work and its alignment with project goals.
- **Sprint retrospective**: Reflect on lessons learned and plan improvements.

---

## Code Style Guidelines

We adhere to **PEP 8** for Python code:
- **Indentation**: Use 4 spaces per level.
- **Line length**: Limit to 79 characters.
- **Naming conventions**: Use snake_case for variables/functions and CamelCase for class names.
- Include **docstrings** in all key functions and classes to describe their purpose and usage.

---

## Testing

- All features must include relevant tests to ensure proper functionality.
- Use `pytest` or `unittest` for testing.
- Tests should cover both normal and edge cases.
- Ensure all tests pass before opening a PR.

---

## Reporting Issues

If you encounter a bug, report it by opening an **issue** in the repository. Include:
1. A clear description of the issue.
2. Steps to reproduce the problem.
3. Expected vs. actual behavior.
4. Any error messages or logs (if applicable).

---

## Role of the Seneca Member

The Seneca member has additional responsibilities:
1. **Documentation**:
   - Maintain the `README.md` with installation instructions, user guides, and features.
2. **Collaboration**:
   - Ensure the team’s progress is properly documented in Taiga.
   - Act as a liaison for external reviewers.

---

## Conclusion

By following these guidelines, we ensure an organized and efficient workflow, enabling the delivery of high-quality code and collaborative success. Thank you for contributing! 
