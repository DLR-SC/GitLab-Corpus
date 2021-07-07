""""""""""""""""""""""""""
Getting started
""""""""""""""""""""""""""

.. contents:: Table of contents
    :depth: 2

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
To use this tool, you need a configuration file to connect to your GitLab instance. It is recommended to create a
directory ``resources`` in your working directory and place a file ``gitlab.cfg`` there, as the tool will look there by
default. Otherwise, you will have to specify the location of the file manually.

If you need help with the content of that configuration file, read the docs here:
`python-gitlab docs <https://python-gitlab.readthedocs.io/en/stable/cli-usage.html#content>`_
It is a `known bug <https://gitlab.dlr.de/sc/ivs-open/corpus/-/issues/16>`_, that sometimes the execution stops with
the ReadTimeout error. Until now, there is no better solution, than setting the ``timeout`` value in the configuration
file to 15 or more.

Also, if you want to use the pipeline ``corpus build`` or the command ``corpus filter`` you should specify a
filter file, also in the ``resources`` directory (recommended).
Otherwise, you will have to specify the location of the file manually.


==========================
Information
==========================
If you use ``corpus build`` or ``corpus extract`` with the parameter ``--all-elements`` it may take some time (I have
witnessed execution times of over 40 minutes). So I really recommend, that you do a ``corpus extract --all-elements``
only once. In the following you can then use ``corpus filter --out=path/to/file.json``. This will prevent, that your
previously extracted corpus will be overwritten, as you probably do not want to crawl all projects again everytime you
try a new filter.

You can find interesting templates for filters here:
`filter templates <https://gitlab.dlr.de/sc/ivs-open/corpus/-/tree/master/filter-templates>`_