# GitLab-Corpus
This tool creates a corpus for publicly accessible repositories in the DLR-GitLab instance. 
The corpus will primarily contain information about software projects. 
Relevant information could be:  
* number of authors or commits
* license information
* programming languages used
* CI usage  

and more.  
The output corpus will most-likely be in the JSON-format, as it is widely used. Especially, because of it's 
compatibility with [neo4j](https://neo4j.com/)

## Install
The tool requires Python >= 3.8 and uses the libraries [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/) 
and [click](https://click.palletsprojects.com/en/7.x/).

You can clone this repository and then install the tool as follows:  
```bash
git clone ...
cd gitlab-corpus
pip install .
```  

## Usage
**NOTE** In order to use this tool you first need to write a `config-file` in which you provide information about the 
GitLab instance you want to run this tool on. For further information read the corresponding 
[python-gitlab docs](https://python-gitlab.readthedocs.io/en/stable/cli.html#content).  
The tool can be run using the command *tbd*.

Running the command without any additional parameters or using the `-h` or `--help` parameter, will print the help page.
