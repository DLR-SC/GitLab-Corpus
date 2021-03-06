<!--
SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
SPDX-License-Identifier: MIT
-->


# GitLab-Corpus
This tool creates a corpus for publicly accessible repositories in the DLR-GitLab instance. 
The corpus will primarily contain information about software projects. 
Relevant information could be:  
* number of authors or commits
* mergerequests
* programming languages used
* CI usage  

and more.  
The output corpus is in the JSON-format, as it is widely used and because of its 
compatibility with [neo4j](https://neo4j.com/)

## Install
The tool requires Python >= 3.8.

## Dependencies to use this tool
See setup.cfg under the section `install_requires`.

## Dependencies to develop this tool
See requirements.txt.

You can clone this repository and then install the tool as follows:  
```bash
git clone <url>
cd corpus
pip install --editable .
```  

## Usage
**NOTE** In order to use this tool you first need to write a `config-file` in which you provide information about the 
GitLab instance you want to run this tool on. Here is an example:

```
[global]
default = gitlab-1
ssl_verify = true
timeout = 15

[gitlab-1]
url = https://gitlab.example.com
private_token = 123abc
api_version = 4
```
 
The tool can be run using the command `corpus`.

Running the command using the `--help` parameter or without any parameter, will print the help page.


## Documentation
[Click here to read the documentation.](
https://sc.pages.gitlab.dlr.de/ivs-open/corpus/)
