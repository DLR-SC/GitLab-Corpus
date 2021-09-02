""""""""""""""""""""""""""
Getting started
""""""""""""""""""""""""""

.. contents:: Table of contents
    :depth: 2

==========================
Preconditions
==========================

 - Have python installed (>= 3.8)

==========================
Get the code
==========================
Execute the following commands to get the code (example shows clone via https)::

    git clone https://gitlab.dlr.de/sc/ivs-open/corpus.git
    cd corpus
    pip install --editable .

After that, you should be able to run the command ``corpus``.

To view the help page, simply use ``corpus`` or ``corpus --help``


==========================
Basic configuration
==========================
There are three files that are often needed to run Corpus:

#. gitlab.cfg (mandatory)
#. filters.yaml (required when using ``corpus filter`` or ``corpus build``)
#. neo4j.cfg (optional)

To use this tool, you need a configuration file to connect to your GitLab server. It is recommended to create a
directory ``resources`` in your working directory and place a file ``gitlab.cfg`` there, as the tool will look there by
default. Otherwise, you will have to specify the location of the file manually.

If you need help with the content of that configuration file, read the docs here:
`python-gitlab docs <https://python-gitlab.readthedocs.io/en/stable/cli-usage.html#content>`_
It is a `known bug <https://gitlab.dlr.de/sc/ivs-open/corpus/-/issues/16>`_, that sometimes the execution stops with
the ReadTimeout error. Until now, there is no better solution, than setting the ``timeout`` value in the configuration
file to a higher value.

Also, if you want to use the pipeline ``corpus build`` or the command ``corpus filter`` you should specify a
filter file, also in the ``resources`` directory (recommended).
Otherwise, you will have to specify the location of the file manually.
For more information on how to write a filter file read here: :ref:`how_to_write_a_filter_file`

To use the Neo4J export functionality you need to specify a ``neo4j.cfg`` file in the ``resources`` folder or specify it
with the ``--neo4j-config=..`` parameter when running Corpus.
For more information on how to write the Neo4J-configuration file read here: :ref:`how-to-write-the-neo4j-config`

==========================
Information
==========================
If you use ``corpus build`` or ``corpus extract`` with the parameter ``--all-elements`` it may take some time (
especially pipelines that extract a huge number of projects and export them to Neo4J can take up to several hours).
So I really recommend, that you do a ``corpus extract --all-elements`` only once. In the following you can then use
``corpus filter --out=path/to/file.json``. This will prevent, that your previously extracted corpus will be overwritten,
as you probably do not want to crawl all projects again everytime you try a new filter.

You can find interesting templates for filters here:
`filter templates <https://gitlab.dlr.de/sc/ivs-open/corpus/-/tree/master/filter-templates>`_