# Getting started

{!../README.md!lines=22-47}

To view the help page, simply use `corpus` or `corpus --help`

## Basic configuration

There are three files that are often needed to run `corpus`:

1. `gitlab.cfg` (mandatory)
2. `filters.yaml` (required when using `corpus filter` or `corpus build`)
3. `neo4j.cfg` (optional)

Per default, `corpus` looks for these files in the `./resources/` directory.
Locations of these files can also be passed to `corpus` commands as arguments.  

### `gitlab.cfg` - configuration of the GitLab instance to work with 

If you need help with the content of that configuration file, read the
docs here: [python-gitlab docs](https://python-gitlab.readthedocs.io/en/stable/cli-usage.html#content).
It is a [known bug](https://github.com/DLR-SC/GitLab-Corpus/issues/21), that
sometimes the execution stops with the `ReadTimeout` error. Until now,
there is no better solution, than setting the `timeout` value in the
configuration file to a higher value.

### `filter.yaml` - configure the filtering stage of corpus building

If you want to use the `corpus build` or `corpus filter` commands,
you should specify a filter file. For more information on how to write
a filter file read here: [_How to write a filter file_](filter-specification.md).

### `neo4j.cfg` - configure the Neo4J export functionality

To use the Neo4J export functionality you need to create a `neo4j.cfg`
file. For more information
on how to write the Neo4J-configuration file read here: [_How to write the Neo4J configuration_](neo4j-configuration.md).

## Information

If you use `corpus build` or `corpus extract` with the parameter
`--all-elements` it may take some time (especially pipelines that
extract a huge number of projects and export them to Neo4J can take up
to several hours). So I really recommend, that you do a
`corpus extract --all-elements` only once. In the following you can then
use `corpus filter --out=path/to/file.json`. This will prevent, that
your previously extracted corpus will be overwritten, as you probably do
not want to crawl all projects again everytime you try a new filter.

You can find interesting templates for filters here: [filter templates](https://github.com/dlr-sc/gitlab-corpus/tree/main/filter-templates).
