# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import re
import click
import yaml

from utils.helpers import Corpus

"""
.. module:: filter
.. moduleauthor:: Emanuel Caricato <emanuel.caricato@dlr.de>
"""


def eval_percentage(project_language_percentage, evaluation):
    """This function checks if the evaluation specified in the filter is true for the selected language.
    :param project_language_percentage: Percentage of a language in a project
    :param evaluation: Value and operand the percentage of a language will be compared to
    :returns ``True`` if the evaluation is true and ``False`` otherwise
    """
    try:
        operator = evaluation['operator']
        value = evaluation['value']
        if operator == "<":
            return project_language_percentage < float(value)
        elif operator == "<=":
            return project_language_percentage <= float(value)
        elif operator == ">":
            return project_language_percentage > float(value)
        elif operator == ">=":
            return project_language_percentage >= float(value)
        elif operator == "==":
            return project_language_percentage == float(value)
        elif operator == "!=":
            return project_language_percentage != float(value)
        else:
            return False
    except AttributeError:  # never occurs anymore?
        return True


def eval_all_percentages(project_languages, project, languages):
    """This function checks if all language evaluations are true for the project.
    :param project_languages: List of all languages in the project
    :param project: The project to be evaluated
    :param languages: List of languages and filter evaluations
    :returns ``True`` if all evaluations are true and ``False`` otherwise
    """
    for item in project_languages:
        try:
            if eval_percentage(project["languages"][item], languages[item]):
                pass
            else:
                return False
        except KeyError:
            pass
    return True


def eval_condition(attribute, operator, condition):
    """This function evaluates if the condition is true using the specified operator.
    :param attribute: Attribute of the project to be checked in the evaluation
    :param operator: Operator used for the evaluation
    :param condition: Condition the attribute will be compared to
    :returns ``True`` if the evaluation is true and ``False`` otherwise
    """
    # Match types
    if isinstance(attribute, int):
        condition = int(condition)
    elif isinstance(attribute, float):
        condition = float(condition)

    if operator == "==":
        return attribute == condition
    elif operator == "!=":
        return attribute != condition
    elif operator == "<=" and (isinstance(attribute, int) or isinstance(attribute, float)):
        return attribute <= condition
    elif operator == "<" and (isinstance(attribute, int) or isinstance(attribute, float)):
        return attribute < condition
    elif operator == ">=" and (isinstance(attribute, int) or isinstance(attribute, float)):
        return attribute >= condition
    elif operator == ">" and (isinstance(attribute, int) or isinstance(attribute, float)):
        return attribute > condition
    elif operator == "contains" and isinstance(attribute, str) and isinstance(condition, str):
        return condition in attribute
    elif isinstance(attribute, str) and isinstance(condition, str):
        if condition.startswith('#') and condition.endswith('#'):
            re.escape(condition)
            return re.match(condition[1:-1], attribute) is not None


class Filter:
    """This class implements the filter options for the corpus, by loading the filter options as specified in the
    :ref:`filter-file`.

    Methods:
        __init__(self, verbose, corpus, from_file=False, file="-")
        load_filters(self, filter_file)
        load_languages(self, filter_option, category)
        filter(self)
        filter_project(self, project)
        check_languages(self, filter_option, project)
    """

    filtered_corpus = Corpus()

    def __init__(self, verbose, corpus, from_file=False, file="-"):
        """Filter class constructor to initialize the object.
        :param verbose: Prints more output, if set to ``True``
        :param corpus: Input corpus, which will be filtered
        :param from_file: Specifies, if the input corpus should be read from a file [default: ``False``]
        :param file: Path to input corpus
        """
        self.verbose = verbose
        self.filters = {}
        self.any_languages = {}
        self.atleast_languages = {}
        self.atmost_languages = {}
        self.exact_languages = {}
        self.attributes = []
        self.input_corpus = Corpus()
        if from_file:
            with open(file, 'r') as f:
                self.input_corpus.data = json.load(f)
        else:
            self.input_corpus = corpus

    def load_filters(self, filter_file):
        """This method loads the filters to be used on the extracted corpus. By default it gets passed the file
        `resources/filters.yaml`.
        :param filter_file: Path to filter file (see also :ref:`filter-file`)
        """
        try:
            with open(filter_file, "r") as f:
                filters = yaml.full_load(f)
                if filters["filters"] is not None:  # add all filters to filter list
                    for filter_option in filters["filters"]:
                        category = filter_option
                        if re.match('.*_languages', category):  # add languages
                            self.filters[category] = ""  # remember language as filter option
                            self.load_languages(filters["filters"][category], category)
                        else:
                            self.filters[category] = filters["filters"][category]  # add all other filters

                if filters["attributes"] is not None:  # add all attributes to be shown in corpus
                    for attribute in filters["attributes"]:
                        self.attributes.append(attribute)
        except FileNotFoundError:
            if self.verbose:
                click.echo("No filter configuration file found. No filters will be applied.")
            else:
                pass

    def load_languages(self, language_list, category):
        """This method loads the languages to be filtered and stores them in a list.
        :param language_list: List containing all filter options regarding the language category as specified in the
        :ref:`filter-file`
        :param category: Category of the language filter. Should be one of:
        * any_languages
        * atleast_languages
        * atmost_languages
        * exact_languages
        """
        if language_list is not None:
            for element in language_list:
                if category == "any_languages":
                    self.any_languages[element] = language_list[element]
                elif category == "atleast_languages":
                    self.atleast_languages[element] = language_list[element]
                elif category == "atmost_languages":
                    self.atmost_languages[element] = language_list[element]
                else:
                    self.exact_languages[element] = language_list[element]

    def filter(self):
        """This method filters the extracted corpus by using the previously loaded filter options. If no filter
        options were set, all projects will be kept in the resulting corpus. If no attributes are specified, all
        attributes will be kept in the resulting corpus."""
        click.echo("Filtering...")
        projects_dict = self.input_corpus.data["Projects"]
        if len(self.filters) > 0:
            with click.progressbar(projects_dict) as bar:
                for project in bar:
                    if self.filter_project(project):
                        self.filtered_corpus.data["Projects"].append({key: value for key, value in project.items()
                                                                      if key in self.attributes
                                                                      or len(self.attributes) == 0})
        elif len(self.attributes) > 0:
            with click.progressbar(projects_dict) as bar:
                for project in bar:
                    self.filtered_corpus.data["Projects"].append({key: value for key, value in project.items()
                                                                  if key in self.attributes
                                                                  or len(self.attributes) == 0})
        else:
            self.filtered_corpus.data = self.input_corpus.data

    def filter_project(self, project):
        """This method applies the specified filters to a project.
        :param project: Project, which will be filtered
        :returns ``True`` if the project passes the filter criteria and ``False`` otherwise.
        """
        return_val = True
        for filter_option in self.filters:
            if re.match('.*_languages', filter_option):  # filter project languages
                if return_val:
                    if self.filters[filter_option] is None:
                        pass
                    else:
                        return_val = self.check_languages(filter_option, project)
            elif return_val:  # filter other attributes
                try:
                    operator = self.filters[filter_option]['operator']
                    condition = self.filters[filter_option]['value']
                    return_val = eval_condition(project[filter_option], operator, condition)
                except ValueError:
                    pass
        return return_val

    def check_languages(self, filter_option, project):
        """This method applies the language filters to a project.
        :param filter_option: The language filter category
        :param project: The project to be checked
        :returns ``True``` if the language filters evaluate to true and ``False`` otherwise
        """
        project_languages = list(project["languages"].keys())
        if filter_option == "any_languages":  # project contains any language specified in the filter
            filter_languages = list(self.any_languages.keys())
            for item in project_languages:
                if item in filter_languages:
                    return eval_percentage(project["languages"][item], self.any_languages[item])
                else:
                    return False
        elif filter_option == "atleast_languages":  # project contains at least the languages specified in the filter
            filter_languages = list(self.atleast_languages.keys())
            if all(elem in project_languages for elem in filter_languages) and len(project_languages) > 0:
                return eval_all_percentages(project_languages, project, self.atleast_languages)
            else:
                return False
        elif filter_option == "exact_languages":  # project contains exactly the languages specified in the filter
            filter_languages = list(self.exact_languages.keys())
            if all(elem in filter_languages for elem in project_languages) \
                    and len(filter_languages) == len(project_languages):
                return eval_all_percentages(project_languages, project, self.exact_languages)
            else:
                return False
        elif filter_option == "atmost_languages":  # project contains at most the languages specified in the filter
            filter_languages = list(self.atmost_languages.keys())
            if all(elem in filter_languages for elem in project_languages) and len(project_languages) > 0:
                return eval_all_percentages(project_languages, project, self.atmost_languages)
            else:
                return False
        else:
            return False  # no languages to be filtered
