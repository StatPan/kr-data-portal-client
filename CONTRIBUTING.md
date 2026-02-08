# Contributing Guidelines

Thank you for considering contributing to `kr-data-portal-client`!

## Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. This allows us to automatically generate changelogs and manage versioning.

### Format
`<type>(<scope>): <description>`

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

### Examples
- `feat(api): add support for stock price info`
- `fix(client): handle timeout errors gracefully`
- `chore: update dependencies`

## Development Workflow

1. **Install environment**:
   ```bash
   uv sync --all-extras
   ```

2. **Setup pre-commit**:
   ```bash
   uv run pre-commit install --hook-type commit-msg --hook-type pre-commit
   ```

3. **Run tests**:
   ```bash
   uv run pytest
   ```

4. **Linting**:
   We use `ruff` for linting and formatting. It is checked automatically via pre-commit.

## Release Process

The project uses GitHub Actions to automate PyPI publishing and GitHub Release creation.
Every push to `main` (that isn't a skip-CI commit) will:
1. Run quality checks and integration tests.
2. Bump the patch version.
3. Publish to PyPI.
4. Create a GitHub Release with auto-generated release notes.
