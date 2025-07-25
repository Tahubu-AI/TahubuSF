# Style guide

TahubuSF is a growing project with many contributors. To ensure that the code is consistent and easy to read, we have created this style guide. Please follow these guidelines when contributing to the project.

## General

The solution contains different languages and frameworks. The following guidelines apply to all of them:

- Simple, clean, and readable is always better
- Avoid passing data structures around, always use strongly-typed classes
- Use the latest language features
- Use well-established design patterns
- Always think about the bigger picture (how will my choice potentially impact everyone else?)
- When introducing a new pattern/approach in your code, share with the rest of the team
- Measure 10 times, cut once (i.e. design before you code)

> Primarily, we strive to use a uniform approach across all the modules of the platform.

## Commenting

- Use comments to explain **why** you are doing something, not **what** you are doing.
- Apply comments to **all** public classes, methods, and properties.
- Comments should be written in complete sentences with proper casing and punctuation.
- Add a space after the comment delimiter (`//`, `#`, etc.).

Do:

```python
# If the search index does not exists, create the index.
```

Don't:

```python
#Create index
```

## Python

Abide by the Python naming and coding rules ([PEP (Python Enhancement Proposal) 8](https://peps.python.org/pep-0008/)).
