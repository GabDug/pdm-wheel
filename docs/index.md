# `pdm-wheel` User Guide

!!! info

    For more information on how this was built and deployed, as well as other Python best
    practices, see [`pdm-wheel`](https://github.com/GabDug/pdm-wheel).

!!! info

    This user guide is purely an illustrative example that shows off several features of
    [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and included Markdown
    extensions[^1].

[^1]: See `pdm-wheel`'s `mkdocs.yml` for how to enable these features.

## Installation

First, [install Poetry](https://python-poetry.org/docs/#installation):

=== "Linux/macOS"

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

=== "Windows"

    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

Then install the `pdm-wheel` package and its dependencies:

```bash
poetry install
```

Activate the virtual environment created automatically by Poetry:

```bash
poetry shell
```

## Quick Start

To use `pdm-wheel` within your project, import the `factorial` function and execute it like:

```python
from pdm-wheel.lib import factorial

assert factorial(3) == 6 # (1)!
```

1. This assertion will be `True`

!!! tip

    Within PyCharm, use ++tab++ to auto-complete suggested imports while typing.

### Expected Results

<div class="center-table" markdown>

| Input | Output |
|:-----:|:------:|
|   1   |   1    |
|   2   |   2    |
|   3   |   6    |
|   4   |   24   |

</div>
