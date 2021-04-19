# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import click
import gitlab
from extract import Extractor
from export import Exporter
from filter import Filter


@click.command()
@click.option('--config-path', '-cp', default='./gitlab.cfg',
              help='Path to the config file \t\t\tDEFAULT = ./gitlab.cfg')
@click.option('--source', '-s',
              help='Name of the GitLab instance, you want to analyse, if not the default value of your configuration')
@click.option('--all-elements', '-a',
              help='Get all elements available in the GitLab instance WARNING: This might take a long time and might '
                   'cause problems for the server',
              is_flag=True)
@click.option('--filter-file', '-f',
              help='File in yaml format which defines the filters to be used on the corpus',
              default='./filters.yaml')
@click.option('--verbose', '-v',
              help='More output',
              is_flag=True)
@click.argument('out', type=click.File('w'), default='./out.json')
def cli(config_path, source, all_elements, filter_file, out, verbose):
    """This tool creates a corpus of all available software projects in a GitLab instance and writes its output to
    the ``out`` file (default: ``./out.json``)."""
    gl = gitlab.Gitlab.from_config(source, config_path)

    extractor = Extractor(verbose, gl)
    corpus_filter = Filter(verbose, input_corpus=extractor.extracted_corpus)
    exporter = Exporter(verbose, format_str="json")

    extractor.extract(all_elements=all_elements)

    corpus_filter.load_filters(filter_file=filter_file)
    corpus_filter.filter()

    exporter.export(corpus=corpus_filter.filtered_corpus, out=out)


if __name__ == '__main__':
    cli()
