# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import click
import yaml


class Filter:
    """This class implements the filter possibilities for the corpus"""

    filtered_corpus = {"Projects": [],
                       }

    def __init__(self, input_corpus, from_file=False, file="-"):
        self.filters = []
        if from_file:
            with open(file, 'w') as f:
                self.input_corpus = json.load(f)
        else:
            self.input_corpus = input_corpus

    def load_filters(self, filter_file):
        """This function loads the filters to be used on the extracted corpus. By default it gets passed the file
        `./filters.yaml`."""
        try:
            with open(filter_file, "r") as f:
                filters = yaml.full_load(f)
                if filters["filters"] is not None:
                    for filter_option in filters["filters"]:
                        self.filters.append(filter_option)
        except FileNotFoundError:
            click.echo("No filter configuration file found. No filters will be applied.")

    def filter(self):
        """This function filters the extracted corpus by using the previously loaded filter options. If no filter
        options were set, all attributes will be kept in the resulting corpus."""
        projects_dict = self.input_corpus["Projects"]
        if len(self.filters) > 0:
            click.echo("Filtering...")
            with click.progressbar(projects_dict) as bar:
                for project in bar:
                    self.filtered_corpus["Projects"].append({key: value for key, value in project.items()
                                                             if key in self.filters})
        else:
            self.filtered_corpus = self.input_corpus
