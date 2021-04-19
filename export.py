# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import click


class Exporter:

    def __init__(self, verbose, format_str):
        self.verbose = verbose
        self.format = format_str

    def export(self, corpus, out):
        if self.format.lower() == "json":
            if self.verbose:
                click.echo("Output format is JSON.")
            json.dump(corpus, out, indent=4)
        elif self.format.lower() == "console":
            if self.verbose:
                click.echo("Output will be printed to console.")
            for category in corpus:
                for element in corpus[category]:
                    click.echo(str(element) + "\n")
