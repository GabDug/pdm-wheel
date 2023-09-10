# pdm-wheel

[![Tests](https://github.com/GabDug/pdm-wheel/actions/workflows/ci.yml/badge.svg)](https://github.com/GabDug/pdm-wheel/actions/workflows/ci.yml)
[![pypi version](https://img.shields.io/pypi/v/pdm-wheel.svg)](https://pypi.org/project/pdm-wheel/)
[![License](https://img.shields.io/pypi/l/pdm-wheel.svg)](https://pypi.python.org/pypi/pdm-wheel)
[![Python version](https://img.shields.io/pypi/pyversions/pdm-wheel.svg)](https://pypi.python.org/pypi/pdm-wheel)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/GabDug/pdm-wheel/main.svg?badge_token=PzBISUnvTEeYahD7i22qiA)](https://results.pre-commit.ci/latest/github/GabDug/pdm-wheel/main?badge_token=PzBISUnvTEeYahD7i22qiA)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Ruff](https://img.shields.io/badge/ruff-lint-red)](https://github.com/charliermarsh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A PDM plugin that save your requirements as wheels, similar to [`pip wheel`](https://pip.pypa.io/en/stable/cli/pip_wheel/)

## Use cases

- You want to build wheels for your dependencies, but don't want to use `pdm export` and `pip wheel`.
- You need to pass the wheels to a CI/CD pipeline, and don't want to build them on the CI/CD server.
- You want to install dependencies in a Docker image, but don't wan't to configure private repositories in the image.

## Supported versions

- Python 3.10+
- PDM 2.7.4+

## Installation

Install it [just like any other PDM plugin](https://pdm.fming.dev/latest/dev/write/#activate-the-plugin):

```bash
pdm self add pdm-wheel
```

If you have installed PDM with the recommended tool `pipx`, add this plugin by:

```bash
pipx inject pdm pdm-wheel
```

Or if you have installed PDM with `pip install --user pdm`, install with `pip` to the user site:

```bash
python -m pip install --user pdm-wheel
```

Optionally, you can also specify [the plugin in your project](https://pdm.fming.dev/latest/dev/write/#specify-the-plugins-in-project) `pyproject.toml`, to make it installable with `pdm install --plugins`:

```toml
[tool.pdm]
plugins = [
    "pdm-wheel"
]
```

## Usage

```bash
pdm wheel [common-options] [dependencies-selection-options] [wheel-options]
```

💡 Check the options for your version of `pdm wheel` with:

```bash
pdm wheel --help
```

**Wheel Options:**

`-w OUTPUT, --wheel-dir OUTPUT`

> Specify the output directory. It will be created it it does not exists. Default is the current directory `./wheels`
> Environment variable: `PDM_WHEEL_DIR`

`--clean`

> Clean the target directory before building.

`--no-clean`

> Do not clean the target directory before building. This is the default behavior.

## Notes on lockfiles

PDM 2.8+ now saves the lockfiles with only hashes and no URL by default.

There is currently a performance overhead, as some internals expect the URL to be present, else they will try to reach the indexes to get it.

Thus, I recommend you use `pdm lock --static-urls` to have faster `pdm wheel` operations.

_Read more about this in [PDM's documentation](https://pdm.fming.dev/latest/usage/dependency/#store-static-urls-or-filenames-in-lockfile)._

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

## Changelog

See [Github Releases](https://github.com/GabDug/pdm-wheel/releases)

## Acknowledgements

`pdm-wheel` is inspired by [`pip wheel`](https://pip.pypa.io/en/stable/cli/pip_wheel/).

`pdm-wheel`'s structure is based on frostming's [`pdm-packer`](https://github.com/frostming/pdm-packer/)
