# Contributing to ActTrack

Thank you for your interest in contributing to ActTrack! This document provides guidelines for contributing to the project.

## About ActTrack

ActTrack is a non-commercial, educational project for real-time body pose detection and motion capture. All contributions must align with these principles.

## Code of Conduct

- Use this project for educational and research purposes only
- Respect the non-commercial license
- Be respectful and professional in all interactions
- Help others learn and grow

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Virtual environment created and activated

### Fork and Clone

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork locally
git clone https://github.com/YOUR-USERNAME/ActTrack.git
cd ActTrack

# 3. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create a feature branch
git checkout -b feature/your-feature-name
```

## How to Contribute

### Types of Contributions

1. **Bug Fixes**: Report bugs and submit fixes
2. **Features**: Propose and implement new features
3. **Documentation**: Improve README, docstrings, and guides
4. **Tests**: Add unit tests and integration tests
5. **Code Quality**: Refactor, optimize, and improve code

### Before You Start

- Check existing issues and pull requests
- Create an issue to discuss major changes
- Keep changes focused and small
- Ensure changes don't break existing functionality

## Development Guidelines

### Code Style

- Follow **PEP 8** guidelines
- Use meaningful variable and function names
- Add docstrings to all functions:

```python
def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    
    Args:
        a (list): First point [x, y]
        b (list): Mid point [x, y]
        c (list): End point [x, y]
        
    Returns:
        float: Angle in degrees
    """
```

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Improve", "Refactor"
- Examples:
  - ✅ "Add smoothing algorithm for landmarks"
  - ✅ "Fix UDP connection timeout issue"
  - ❌ "fixed stuff"
  - ❌ "changes"

```bash
git commit -m "Add feature: implement custom angle calculation"
```

### Testing

- Test your changes thoroughly
- Include simple test cases for new features
- Verify existing functionality still works
- Test on different configurations if possible

## Submitting Changes

### Pull Request Process

1. **Update from Main**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Go to GitHub and click "Compare & pull request"
   - Provide clear description of changes
   - Reference any related issues (#123)
   - Include before/after behavior

4. **PR Description Template**
   ```markdown
   ## Description
   Brief explanation of what this PR does
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   
   ## Changes Made
   - Change 1
   - Change 2
   
   ## Testing
   Describe how to test these changes
   
   ## Related Issues
   Closes #123
   ```

### PR Review Process

- At least one maintainer review required
- Respond to feedback constructively
- Make requested changes
- Push updates to the same branch (auto-updates PR)

## Documentation Contributions

### Improving Documentation

1. **README.md**: Update project overview, features, or usage
2. **CONTRIBUTING.md**: These guidelines
3. **Code Comments**: Add helpful comments in complex logic
4. **Docstrings**: Document all functions and classes

### Documentation Standards

- Clear and concise language
- Include code examples where helpful
- Update version numbers if applicable
- Check formatting and links

## Reporting Issues

### Bug Reports

Include the following in bug reports:

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 3.x
- OS: Windows/Mac/Linux
- Camera model: (if relevant)

## Error Message/Logs
```
Error output here
```
```

### Feature Requests

Include:

```markdown
## Feature Description
What you want to add

## Use Case
Why this feature is useful

## Proposed Implementation
How you think it could be implemented

## Additional Context
Any other relevant information
```

## Development Tips

### Useful Debug Commands

```bash
# Check code style
pip install pylint
pylint body.py

# Run doctests
python -m doctest body.py -v

# Profile performance
python -m cProfile -s cumtime body.py
```

### Common Issues

**Issue**: Changes don't appear when running
- Solution: Restart Python and clear cache `rm -r __pycache__`

**Issue**: Merge conflicts
```bash
# View conflicts
git status

# Edit conflicted files manually
# Then:
git add .
git commit -m "Resolve merge conflicts"
```

## License Compliance

- All contributions must be compatible with non-commercial use
- Don't include commercial code or assets
- Maintain attribution to XeroD
- All code must adhere to the LICENSE agreement

## Getting Help

- Check [README.md](README.md) for documentation
- Review existing code for examples
- Create an issue to ask questions
- Be patient and respectful

## Recognition

Contributors who make significant contributions will be recognized in:
- CONTRIBUTORS.md file
- README.md acknowledgments
- Commit history

## Questions?

If you have questions about contributing:
1. Check existing discussions
2. Review the README and documentation
3. Create an issue asking for clarification

---

**Thank You for Contributing!** 🙏

Your contributions help make ActTrack better for everyone in the educational and research community.

*Last Updated: February 25, 2026*
