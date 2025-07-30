<!--
SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
SPDX-License-Identifier: MIT
-->


# GitLab-Corpus

This tool creates a corpus for accessible repositories in a GitLab instance. 
The corpus will primarily contain information about software projects.

Relevant information could be:  

- number of authors or commits
- merge requests
- programming languages used
- CI usage  
- …

The output corpus is in the JSON-format, as it is widely used and because of its compatibility with [neo4j](https://neo4j.com/).

## Requirements

- [Git](https://git-scm.com/) client >= 2.1.0
- Python >= 3.12 with [pip](https://pip.pypa.io/en/stable/) and [venv](https://docs.python.org/3/library/venv.html)
- Optionally, a modern package manager ([`uv`](https://docs.astral.sh/uv/) (recommended), `poetry`, or similar)

## Running the `corpus` CLI tool

If you use `uv`, all you need to do is clone this repository and run the `corpus` command:

```bash
git clone <URL of this Git repository> corpus
cd corpus
uv run corpus
```  

Otherwise, you need to install the dependencies and package first:

```bash
git clone <URL of this Git repository> corpus
cd corpus
python -m venv .venv  # Create a virtual environment
source .venv/bin/activate  # Activate the environment
pip install .  # Install dependencies declared in pyproject.toml
corpus  # Run the corpus CLI, should display a help message
```

## Usage

1. Create a configuration file in `resources/gitlab.cfg`
with information about the GitLab instance you want to run this tool on: 

```ini
[global]
# Sets the default GitLab instance
default = gitlab-1
# Whether SSL certificates should be validated.
# If the value is a string, it is the path to a CA file used for certificate validation.
ssl_verify = true
# Timeout for API requests
timeout = 15

# A GitLab instance
[gitlab-1]
# The instance's base URL
url = https://gitlab.example.com
# A user private token to authenticate with the GitLab API
private_token = 123abc
# The version of the GitLab API to use (the python-gitlab package supports '4' only) 
api_version = 4
```
 
2. Run the corpus tool:

```bash
Usage: corpus [OPTIONS] COMMAND [ARGS]...

  Entry point to the corpus cli.

Options:
  -g, --gl-config TEXT     Path to the GitLab config file  [default: resources/gitlab.cfg]
  -n, --neo4j-config TEXT  Path to the Neo4J config file  [default: resources/neo4j.cfg]
  -s, --source TEXT        Name of the GitLab instance, you want to analyze, if not the default value of your configuration
  -v, --verbose BOOLEAN    Prints more output during execution
  --help                   Show this message and exit.

Commands:
  build    Run the pipeline extract -> filter -> export in one command.
  export   Export a previously extracted (and maybe filtered) corpus to...
  extract  Extract projects from the specified GitLab instance and write...
  filter   Apply filters on a previously extracted corpus.
```

## Documentation

The documentation is available in the [docs](docs/source) directory.
