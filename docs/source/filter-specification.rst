""""""""""""""""""""""""""
How to write a filter file
""""""""""""""""""""""""""

.. contents:: Table of contents
    :depth: 2

=============================
Sections of the filter file
=============================
The filter file is separated into two main sections: ``filters`` and ``attributes``.
A filter specifies **if** a project will be saved in the output corpus. The attributes specified in the
attributes section define, which attributes of a project will be shown in the output corpus.

The two sections are specified by writing::

    filters:

    attributes:

**Without** any indentation.

The example above is also the minimal required filter file, when using ``corpus filter`` or the
``corpus build`` pipeline.

=============================
How to write a filter
=============================
A filter can be written directly under the section title ``filters:`` with an indentation (I always use 4
spaces or tab). Make sure to be consistent with the indentation or your filter file might not be read.

Any attribute a project has in a corpus, can be used as a filter option. To filter by an attribute, one
has to define the operator and the value, that will be used in the evaluation.

Here is a small example::

    filters:
        id:
            operator: "<"
            value: 12345

As we are writing a filter, we start with the keyword ``filters:``. In the next line, we write the attribute
by which we want to filter the projects. Here it is ``id:``. The next two lines are for ``operator`` and
``value``. Any non-numeric values need to be surrounded by double quotes (") or single quotes (').

Attributes with a string value can also be filtered by using a regular expression.

The value (regex string) needs to be encapsulated by two #, as shown in the following example::

    filters:
        name:
            operator: "regex"
            value: "#.*machine\slearning.*#"

Here we search for projects, which have the string 'machine learning' in its name.

================================
Special filter option: languages
================================

GitLab provides the languages used in a project through its API. We can use this, to create a corpus of projects which
use specific languages only.

Until now, there are four possible language filters:

any_languages

    A project will only be added to the corpus, it is contains any of the languages defined here.

atleast_languages

    A project will only be added to the corpus, if it contains at least the languages defined here.

atmost_languages

    A project will only be added to the corpus, if it contains at most the languages defined here.

exact_languages

    A project will only be added to the corpus, if it contains exactly the languages defined here.

Some examples can be found in the section `Examples`.


=============================
How to specify the attributes
=============================
Defining the attributes to be shown in the corpus is straight forward. Simply add the name of the attribute
in a list in the next line after ``attributes``, like so::

    attributes:
        - id
        - name
        - description
        - web_url


=============================
How to refer to a filter file
=============================
A filter file is needed, if you either run the command ``corpus build`` or ``corpus filter``. The default
location for a filter file is ``resources/filters.yaml`` from your current directory.

If you want to specify the location of the filter file manually, add the following to your command::

    corpus build --filter-file=path/to/your/filter_file.yaml

or::

    corpus filter --filter-file=path/to/your/filter_file.yaml

=============================
Examples
=============================

Assume we want to create a corpus of the projects of our GitLab instance, which currently only has two projects:

#. Project 1, which has the following languages section::

    "C#": 52.7,
    "C++": 43.14,
    "C": 4.16

#. Project 2, which has the following languages section::

    "HTML": 51.0,
    "Vue": 9.0,
    "JavaScript": 40.0


--------------------------
Examples for any_languages
--------------------------

We now want to filter out projects that have any of the languages C, C++ or Java. The filter for this would look like
this::

    filters:
        any_languages:
            C:
                operator: ">="
                value: 0.0
            C++:
                operator: ">="
                value: 0.0
            Java:
                operator: ">="
                value: 0.0

The resulting corpus would then contain Project 1 only. In the future it shall be necessary anymore, to write operator
and value in this case.


Now we want to filter more detailed, by projects which have the languages C, C++ or Java with at least 60%::

    filters:
        any_languages:
            C:
                operator: ">="
                value: 60.0
            C++:
                operator: ">="
                value: 60.0
            Java:
                operator: ">="
                value: 60.0

The resulting corpus would not contain any of the two projects.


------------------------------
Examples for atleast_languages
------------------------------

The following filter would only add Project 2 to the corpus, because Project 1 does not contain HTML or Vue::

    filters:
        atleast_languages:
            HTML:
                operator: ">"
                value: 0.0
            Vue:
                operator: ">"
                value: 0.0

Here we filter out projects, which contain at least Vue, but it should not make up more than 50% of
the projects languages::

    filters:
        atleast_languages:
            Vue:
                operator: "<="
                value: 50.0

The corpus would then contain Project 2.


------------------------------
Examples for atmost_languages
------------------------------

We now want to filter out projects, which only contain the programming languages C and C++ and nothing more::

    filters:
        atmost_languages:
            C:
                operator: ">"
                value: 0.0
            C++:
                operator: ">"
                value: 0.0

None of the above projects would be added to the corpus.

If we add C#, Python and ActionScript to the filters, Project 1 will be added to the corpus, because it contains C#,
C++ and C::

    filters:
        atmost_languages:
            C:
                operator: ">"
                value: 0.0
            C++:
                operator: ">"
                value: 0.0
            C#:
                operator: ">"
                value: 0.0
            Python:
                operator: ">"
                value: 0.0
            ActionScript:
                operator: ">"
                value: 0.0


------------------------------
Examples for exact_languages
------------------------------

We now want to filter out those project, that contain exactly HTML, Vue and JavaScript with at least 30%::

    filters:
        exact_languages:
            HTML:
                operator: ">"
                value: 0.0
            Vue:
                operator: ">"
                value: 0.0
            JavaScript:
                operator: ">="
                value: 30.0

The resulting corpus would contain Project 2 only.