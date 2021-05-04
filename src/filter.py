# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import re

import click
import yaml

from utils.helpers import Corpus


class Filter:
    """This class implements the filter possibilities for the corpus"""

    filtered_corpus = Corpus()

    def __init__(self, verbose, corpus, from_file=False, file="-"):
        self.verbose = verbose
        self.filters = {}
        self.languages = []
        self.attributes = []
        self.input_corpus = Corpus()
        if from_file:
            with open(file, 'r') as f:
                self.input_corpus.data = json.load(f)
        else:
            self.input_corpus = corpus

    def load_filters(self, filter_file):
        """This function loads the filters to be used on the extracted corpus. By default it gets passed the file
        `./filters.yaml`."""
        try:
            with open(filter_file, "r") as f:
                filters = yaml.full_load(f)
                if filters["filters"] is not None:  # add all filters to filter list
                    for filter_option in filters["filters"]:
                        if re.match('.*_languages', next(iter(filter_option.keys()))):
                            values = list(filter_option.values())
                            if None not in values:
                                for element in values[0]:
                                    self.languages.append(next(iter(element.keys())))
                        for key in filter_option:
                            self.filters[key] = filter_option[key]

                if filters["attributes"] is not None:  # add all attributes to be shown in corpus
                    for attribute in filters["attributes"]:
                        self.attributes.append(attribute)
        except FileNotFoundError:
            if self.verbose:
                click.echo("No filter configuration file found. No filters will be applied.")
            else:
                pass

    def filter(self):
        """This function filters the extracted corpus by using the previously loaded filter options. If no filter
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
        project_languages = list(project["languages"].keys())
        for filter_option in self.filters:
            if filter_option == "any_languages":
                if self.filters[filter_option]:
                    return any(item in project_languages for item in self.languages)
            elif filter_option == "atleast_languages":
                if self.filters[filter_option]:
                    return all(item in project_languages for item in self.languages)
            elif filter_option == "explicit_languages":
                if self.filters[filter_option]:
                    return all(item in self.languages for item in project_languages) \
                           and len(project_languages) == len(self.languages)
            elif filter_option == "atmost_languages":
                if self.filters[filter_option]:
                    return set(project_languages).issubset(self.languages) and len(project_languages) > 0
            else:
                if project[filter_option] == self.filters[filter_option]:
                    return True
