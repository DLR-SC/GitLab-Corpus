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


class Filter:
    """This class implements the filter options for the corpus"""

    filtered_corpus = Corpus()

    def __init__(self, verbose, corpus, from_file=False, file="-"):
        self.verbose = verbose
        self.filters = {}
        self.languages = {}
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
                        if re.match('.*_languages', next(iter(filter_option.keys()))):  # add languages
                            self.load_languages(filter_option)
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

    def load_languages(self, filter_option):
        """This method loads the languages to be filtered and stores them in a list."""
        values = list(filter_option.values())[0]
        if values is not None:
            for element in values:
                self.languages[next(iter(element.keys()))] = next(iter(element.values()))

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
                                                                      if key in self.attributes})
        else:
            self.filtered_corpus.data = self.input_corpus.data

    def filter_project(self, project):
        """This method applies the specified filters to a project."""
        for filter_option in self.filters:
            if re.match('.*_languages', filter_option):
                if self.check_languages(filter_option, project):
                    return True
            elif project[filter_option] == self.filters[filter_option]:
                return True

    def check_languages(self, filter_option, project):
        """This method applies the language filters to a project."""
        project_languages = list(project["languages"].keys())
        filter_languages = list(self.languages.keys())
        if filter_option == "any_languages":  # project contains any language specified in the filter
            if self.filters[filter_option]:
                for item in project_languages:
                    if item in filter_languages:
                        return eval_percentage(project["languages"][item], self.languages[item])
        elif filter_option == "atleast_languages":  # project contains at least the languages specified in the filter
            if self.filters[filter_option]:
                if all(elem in project_languages for elem in filter_languages):
                    return self.eval_all_percentages(project_languages, project)
        elif filter_option == "explicit_languages":  # project contains exactly the languages specified in the filter
            if self.filters[filter_option]:
                if all(elem in filter_languages for elem in project_languages) \
                        and len(filter_languages) == len(project_languages):
                    return self.eval_all_percentages(project_languages, project)
        elif filter_option == "atmost_languages":   # project contains at most the languages specified in the filter
            if self.filters[filter_option]:
                if all(elem in filter_languages for elem in project_languages):
                    return self.eval_all_percentages(project_languages, project)
        else:
            return False    # no languages to be filtered

    def eval_all_percentages(self, project_languages, project):
        """This method checks if all language evaluations are true for the project"""
        for item in project_languages:
            try:
                if eval_percentage(project["languages"][item], self.languages[item]):
                    return True
            except KeyError:
                pass
