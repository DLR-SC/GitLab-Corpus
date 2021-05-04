# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import click

from utils.helpers import Corpus


class Exporter:

    def __init__(self, verbose, corpus, format_str, from_file=False, file="-"):
        self.verbose = verbose
        self.format = format_str
        self.corpus = Corpus()
        if from_file:
            with open(file, 'r') as f:
                self.corpus.data = json.load(f)
        else:
            self.corpus = corpus

    def export(self, out):
        with open(out, "w") as output:
            click.echo("Exporting...")
            if self.format.lower() == "json":
                if self.verbose:
                    click.echo("Output written to {}".format(out))
                json.dump(self.corpus.data, output, indent=4)
            elif self.format.lower() == "console":
                if self.verbose:
                    click.echo("Output will be printed to console.")
                for category in self.corpus.data:
                    for element in self.corpus.data[category]:
                        click.echo(str(element) + "\n")
