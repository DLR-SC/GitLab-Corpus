# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import json
import click
import gitlab
from extract import Extractor
from export import Exporter


@click.command()
@click.option('--config-path', '-cp', default='./gitlab.cfg',
              help='Path to the config file \t\t\tDEFAULT = ./gitlab.cfg')
@click.option('--source', '-s',
              help='Name of the GitLab instance, you want to analyse, if not the default value of your configuration')
@click.option('--all-elements', '-a',
              help='Get all elements available in the GitLab instance WARNING: This might take a long time and might '
                   'cause problems for the server',
              is_flag=True)
@click.argument('out', type=click.File('w'), default='./out.json')
def cli(config_path, source, all_elements, out):
    """This tool creates a corpus of all available software projects in a GitLab instance and writes its output to
    the ``out`` file (default: ``./out.json``)."""
    gl = gitlab.Gitlab.from_config(source, config_path)

    extractor = Extractor(gl)
    exporter = Exporter(format_str="console")

    extractor.extract(all_elements=all_elements)

    exporter.export(corpus=extractor.extracted_corpus, out=out)


if __name__ == '__main__':
    cli()
