# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import click

from utils.helpers import Corpus


class Exporter:
    """This class provides a method to export a corpus in another format.

    Methods:
        __init__(self, verbose, corpus, format_str, from_file=False, file="-")
        export(self, out)
    """

    def __init__(self, verbose, corpus, format_str, from_file=False, file="-"):
        """Exporter class constructor to initialize the object.
        :param verbose: Prints more output, if set to ``True``
        :param corpus: Input corpus, which will be exported
        :param from_file: Specifies, if the input corpus should be read from a file [default: ``False``]
        :param file: Path to input corpus
        """
        self.verbose = verbose
        self.format = format_str
        self.corpus = Corpus()
        if from_file:
            with open(file, 'r') as f:
                self.corpus.data = json.load(f)
        else:
            self.corpus = corpus

    def export(self, out):
        """This method exports the corpus to another format.
        :param out: Path to output file
        """
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
