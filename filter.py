# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import click
import yaml

from helpers import Corpus


class Filter:
    """This class implements the filter possibilities for the corpus"""

    filtered_corpus = Corpus()

    def __init__(self, verbose, corpus, from_file=False, file="-"):
        self.verbose = verbose
        self.filters = {}
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
        for filter_option in self.filters:
            if filter_option == "any_languages":
                if self.filters[filter_option]:
                    for language in self.filters[filter_option]:
                        return any(item in list(project["languages"].keys()) for item in list(language.keys()))
            elif filter_option == "atleast_languages":
                if self.filters[filter_option]:
                    languages = []
                    for element in self.filters[filter_option]:
                        languages.append(next(iter(element.keys())))
                    return all(item in list(project["languages"].keys()) for item in languages)
            elif filter_option == "explicit_languages":
                if self.filters[filter_option]:
                    languages = []
                    for element in self.filters[filter_option]:
                        languages.append(next(iter(element.keys())))
                    return all(item in languages for item in list(project["languages"].keys())) \
                           and len(project["languages"]) == len(languages)
            else:
                if project[filter_option] == self.filters[filter_option]:
                    return True
