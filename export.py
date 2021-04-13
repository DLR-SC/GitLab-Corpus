# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import click


class Exporter:

    def __init__(self, format_str):
        self.format = format_str

    def export(self, corpus, out):
        if self.format.lower() == "json":
            json.dump(corpus, out, indent=4)
        elif self.format.lower() == "console":
            for category in corpus:
                for element in corpus[category]:
                    click.echo(str(element) + "\n")
