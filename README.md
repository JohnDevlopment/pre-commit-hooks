# pre-commit-hooks
Some pre-commit hooks.

# Usage
Add this to your `.pre-commit-config.yaml` file:

``` yaml
- repo: https://github.com/JohnDevlopment/pre-commit-hooks
  rev: v1.0 # use the ref you want to point at
  hooks:
  - id: no-push-wip-commits
  - id: no-push-squash-commits
```

## Available Hooks

### Pre-Push Hooks

#### `no-push-wip-commits`
Prevents the pushing of commits whose subjects start with "WIP".

#### `no-push-squash-commits`
Prevents the pushing of commits whose subjects start with "squash!" or "fixup!".
