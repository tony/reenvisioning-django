# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django project demonstrating modern GraphQL API development using Strawberry GraphQL. The project uses Django 5.1+ with Python 3.12+ and the uv package manager.

## Development Commands

### Setup
```bash
# Install dependencies
uv pip install -e .
uv pip install -e ".[dev]"

# Database setup
python manage.py migrate
python manage.py loaddata berries
```

### Running the Development Server
```bash
python manage.py runserver
# Access GraphQL endpoints at:
# - http://localhost:8000/graphql (async)
# - http://localhost:8000/graphql/sync (sync)
```

### Testing
```bash
# Run all tests
pytest

# Run tests with file watching
pytest-watcher

# Run a specific test file
pytest src/envision/core/tests/test_example.py

# Run tests with verbose output
pytest -v
```

### Code Quality
```bash
# Linting and formatting with Ruff
ruff check src/
ruff format src/

# Type checking with MyPy
mypy
```

## Architecture

### Project Structure
- `src/envision/` - Main Django project directory
  - `settings/base.py` - Django configuration
  - `core/` - Core application module containing models, GraphQL schema, and API logic
    - `models.py` - Django models (Fruit, Color)
    - `schema.py` - GraphQL schema definitions with queries and mutations
    - `types.py` - Strawberry GraphQL type definitions
    - `urls.py` - URL routing for GraphQL endpoints

### Key Components

1. **GraphQL Schema** (src/envision/core/schema.py):
   - Provides full CRUD operations for Fruit and Color models
   - Includes user registration mutation
   - Supports filtering, ordering, and pagination
   - Both async and sync endpoints available

2. **Models** (src/envision/core/models.py):
   - `Fruit`: Simple model with name and optional color relationship
   - `Color`: Model with name and reverse relationship to fruits

3. **Type Definitions** (src/envision/core/types.py):
   - Strawberry GraphQL types that correspond to Django models
   - Includes filtering and ordering capabilities

### Important Configuration Notes

- The project uses `uv` as the package manager (not pip directly)
- Django settings are in `src/envision/settings/base.py`
- Debug mode is currently enabled with a hardcoded secret key (development only)
- SQLite3 is used as the default database
- The project follows a src-layout structure

### Common Development Patterns

When adding new GraphQL functionality:
1. Define models in `models.py`
2. Create corresponding Strawberry types in `types.py`
3. Add queries/mutations to `schema.py`
4. Run migrations if models changed: `python manage.py makemigrations && python manage.py migrate`

When modifying existing code:
- Follow the existing code style (Ruff will enforce this)
- Ensure type hints are used throughout (MyPy will check this)
- Add tests for new functionality in the appropriate test files

## Git Commit Standards

### Commit Message Format
```
Component/File(commit-type[Subcomponent/method]): Concise description

why: Explanation of necessity or impact.
what:
- Specific technical changes made
- Focused on a single topic

refs: #issue-number, breaking changes, or relevant links
```

### Common Commit Types
- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting

### Dependencies Commit Format
- Python packages: `py(deps): Package update`
- Python dev packages: `py(deps[dev]): Dev package update`

### Examples

#### Feature Addition
```
core/schema(feat[Query]): Add fruit filtering by color

why: Users need to filter fruits by color in GraphQL queries
what:
- Add color filter parameter to fruits query
- Update resolver to handle color filtering
- Add tests for color filtering

refs: #42
```

#### Bug Fix
```
core/types(fix[FruitType]): Correct optional color relationship

why: Color field was incorrectly marked as required
what:
- Change color field to use Optional type
- Update tests to handle None values

refs: #38
```

#### Dependencies Update
```
py(deps[dev]): Add django-stubs for type checking

why: Improve type safety for Django models and ORM
what:
- Add django-stubs to dev dependencies
- Configure MyPy to use django-stubs plugin
```

### Guidelines
- Subject line: Maximum 50 characters
- Body lines: Maximum 72 characters
- Use imperative mood ("Add", "Fix", not "Added", "Fixed")
- One topic per commit
- Separate subject from body with blank line
- Mark breaking changes: `BREAKING:`