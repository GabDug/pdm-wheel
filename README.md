# pdm-wheel

[![Tests](https://github.com/GabDug/pdm-wheel/actions/workflows/ci.yml/badge.svg)](https://github.com/GabDug/pdm-wheel/actions/workflows/ci.yml)
[![pypi version](https://img.shields.io/pypi/v/pdm-wheel.svg)](https://pypi.org/project/pdm-wheel/)
[![License](https://img.shields.io/pypi/l/pdm-wheel.svg)](https://pypi.python.org/pypi/pdm-wheel)
[![Python version](https://img.shields.io/pypi/pyversions/ruff.svg)](https://pypi.python.org/pypi/pdm-wheel)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/GabDug/pdm-wheel/main.svg?badge_token=PzBISUnvTEeYahD7i22qiA)](https://results.pre-commit.ci/latest/github/GabDug/pdm-wheel/main?badge_token=PzBISUnvTEeYahD7i22qiA)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Ruff](https://img.shields.io/badge/ruff-lint-red)](https://github.com/charliermarsh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A PDM plugin that save your requirements as wheels, similar to [`pip wheel`](https://pip.pypa.io/en/stable/cli/pip_wheel/)

## Requirements

pdm-wheel requires Python >=3.10, and PDM >=2.4.1

## Installation

You can install the plugin directly by:

```bash
pdm plugin add pdm-wheel
```

If you have installed PDM with the recommended tool `pipx`, add this plugin by:

```bash
pipx inject pdm pdm-wheel
```

Or if you have installed PDM with `pip install --user pdm`, install with `pip` to the user site:

```bash
python -m pip install --user pdm-wheel
```

Otherwise, install `pdm-wheel` to the same place where PDM is located.

## Usage

```
pdm wheel [common-options] [dependencies-selection-options] [wheel-options]
```

💡 Check the options for your version of `pdm wheel` with:

```bash
pdm wheel --help
```

**Common Options:**

`-h, --help`

> show this help message and exit

`-v, --verbose`

> -v for detailed output and -vv for more detailed

`-g, --global`

> Use the global project, supply the project
> root with `-p` option

`-p PROJECT_PATH, --project PROJECT_PATH`

> Specify another path as the project root,
> which changes the base of pyproject.toml and `__pypackages__`

`-L LOCKFILE, --lockfile LOCKFILE`

> Specify another lockfile path. Default: `pdm.lock`. [env var: `PDM_LOCKFILE`]

**Dependencies Selection Options:**

`-G GROUP, --group GROUP`

> Select group of optional-dependencies or dev-dependencies (with `-d`). Can be supplied multiple times, use ":all" to include
> all groups under the same species.

`--no-default`

> Don't include dependencies from the default group

`-d, --dev`

> Select dev dependencies

`--prod, --production`

> Unselect dev dependencies

**Wheel Options:**

`-w OUTPUT, --wheel-dir OUTPUT`

> Specify the output directory. By default it is the current directory

## Examples

```bash
# Save all dependencies (including dev deps) as wheels in the ./wheels folder
pdm wheel -w wheels
# Save all dev dependencies  as wheels in the ./wheels folder
pdm wheel -w wheels --dev
# Save all non-dev dependencies as wheels in the ./wheels folder
pdm wheel -w wheels --prod
```

## Caveats

1. `pdm-wheel` does not check whether the wheels are already built.
2. `pdm-wheel` does not empty the output directory before building wheels.

## Changelog

See [CHANGELOG.md](https://github.com/frostming/pdm-wheel/blob/main/CHANGELOG.md)

## Acknowledgements

`pdm-wheel` is inspired by [`pip wheel`](https://pip.pypa.io/en/stable/cli/pip_wheel/).

`pdm-wheel`'s structure is based on frostming's [`pdm-packer`](https://github.com/frostming/pdm-packer/)
