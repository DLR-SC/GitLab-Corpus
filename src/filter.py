# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import re
import click
import yaml

from utils.helpers import Corpus


def eval_percentage(project_language_percentage, evaluation):
    """This function checks if the evaluation specified in the filter is true for the selected language."""
    try:
        operator, value = evaluation.split(" ")
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
    except AttributeError:
        return True


def eval_all_percentages(project_languages, project, languages):
    """This function checks if all language evaluations are true for the project"""
    for item in project_languages:
        try:
            if eval_percentage(project["languages"][item], languages[item]):
                return True
            else:
                return False
        except KeyError:
            pass


def eval_condition(attribute, operator, condition):
    """This function evaluates if the condition is true using the specified operator."""
    if operator == "==":
        click.echo(type(attribute) + "\t" + type(condition))
        return attribute == condition
    elif operator == "!=":
        return attribute != condition
    elif operator == "contains" and isinstance(attribute, str) and isinstance(condition, str):
        return condition in attribute
    elif isinstance(attribute, str) and isinstance(condition, str):
        if condition.startswith('#') and condition.endswith('#'):
            re.escape(condition)
            return re.match(condition[1:-1], attribute)


class Filter:
    """This class implements the filter options for the corpus"""

    filtered_corpus = Corpus()

    def __init__(self, verbose, corpus, from_file=False, file="-"):
        self.verbose = verbose
        self.filters = {}
        self.any_languages = {}
        self.atleast_languages = {}
        self.atmost_languages = {}
        self.explicit_languages = {}
        self.attributes = []
        self.input_corpus = Corpus()
        if from_file:
            with open(file, 'r') as f:
                self.input_corpus.data = json.load(f)
        else:
            self.input_corpus = corpus

    def load_filters(self, filter_file):
        """This method loads the filters to be used on the extracted corpus. By default it gets passed the file
        `resources/filters.yaml`."""
        try:
            with open(filter_file, "r") as f:
                filters = yaml.full_load(f)
                if filters["filters"] is not None:  # add all filters to filter list
                    for filter_option in filters["filters"]:
                        category = next(iter(filter_option.keys()))
                        if re.match('.*_languages', category):  # add languages
                            self.load_languages(filter_option, category)
                        for key in filter_option:
                            self.filters[key] = filter_option[key]  # add all other filters

                if filters["attributes"] is not None:  # add all attributes to be shown in corpus
                    for attribute in filters["attributes"]:
                        self.attributes.append(attribute)
        except FileNotFoundError:
            if self.verbose:
                click.echo("No filter configuration file found. No filters will be applied.")
            else:
                pass

    def load_languages(self, filter_option, category):
        """This method loads the languages to be filtered and stores them in a list."""
        values = list(filter_option.values())[0]
        if values is not None:
            for element in values:
                if category == "any_languages":
                    self.any_languages[next(iter(element.keys()))] = next(iter(element.values()))
                elif category == "atleast_languages":
                    self.atleast_languages[next(iter(element.keys()))] = next(iter(element.values()))
                elif category == "atmost_languages":
                    self.atmost_languages[next(iter(element.keys()))] = next(iter(element.values()))
                else:
                    self.explicit_languages[next(iter(element.keys()))] = next(iter(element.values()))

    def filter(self):
        """This method filters the extracted corpus by using the previously loaded filter options. If no filter
        options were set, all attributes will be kept in the resulting corpus."""
        if len(self.filters) > 0:
            projects_dict = self.input_corpus.data["Projects"]
            click.echo("Filtering...")
            with click.progressbar(projects_dict) as bar:
                for project in bar:
                    if self.filter_project(project):
                        self.filtered_corpus.data["Projects"].append({key: value for key, value in project.items()
                                                                      if key in self.attributes
                                                                      or len(self.attributes) == 0})
        else:
            self.filtered_corpus.data = self.input_corpus.data

    def filter_project(self, project):
        """This method applies the specified filters to a project."""
        return_val = True
        for filter_option in self.filters:
            if re.match('.*_languages', filter_option):     # filter project languages
                if return_val:
                    if self.filters[filter_option] is None:
                        pass
                    else:
                        return_val = self.check_languages(filter_option, project)
            elif return_val:    # filter other attributes
                try:
                    operator, condition = self.filters[filter_option].split("//")
                    return_val = eval_condition(project[filter_option], operator, condition)
                except ValueError:
                    pass
        return return_val

    def check_languages(self, filter_option, project):
        """This method applies the language filters to a project."""
        project_languages = list(project["languages"].keys())
        if filter_option == "any_languages":  # project contains any language specified in the filter
            filter_languages = list(self.any_languages.keys())
            for item in project_languages:
                if item in filter_languages:
                    return eval_percentage(project["languages"][item], self.any_languages[item])
        elif filter_option == "atleast_languages":  # project contains at least the languages specified in the filter
            filter_languages = list(self.atleast_languages.keys())
            if all(elem in project_languages for elem in filter_languages):
                return eval_all_percentages(project_languages, project, self.atleast_languages)
        elif filter_option == "explicit_languages":  # project contains exactly the languages specified in the filter
            filter_languages = list(self.explicit_languages.keys())
            if all(elem in filter_languages for elem in project_languages) \
                    and len(filter_languages) == len(project_languages):
                return eval_all_percentages(project_languages, project, self.explicit_languages)
        elif filter_option == "atmost_languages":  # project contains at most the languages specified in the filter
            filter_languages = list(self.atmost_languages.keys())
            if all(elem in filter_languages for elem in project_languages):
                return eval_all_percentages(project_languages, project, self.atmost_languages)
        else:
            return False  # no languages to be filtered

