# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import click
import gitlab
from extract import Extractor
from export import Exporter
from filter import Filter
from utils.helpers import Corpus, Config

# instance of a corpus that can be passed as click annotation
corpus = click.make_pass_decorator(Corpus, ensure=True)

# instance of class config, which stores parameters for later use
command_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--config-path', '-cp', default='resources/gitlab.cfg',
              help='Path to the GitLab config file', show_default=True)
@click.option('--source', '-s',
              help='Name of the GitLab instance, you want to analyze, if not the default value of your configuration')
@click.option('--verbose', '-v', default=False,
              help='Prints more output during execution')
@command_config
def cli(config, config_path, source, verbose):
    """Entry point to the corpus cli."""
    config.gl = gitlab.Gitlab.from_config(source, config_path)
    config.verbose = verbose


@cli.command()
@click.option('--all-elements', '-a',
              help='Get all elements available in the GitLab instance WARNING: This might take a long time and might '
                   'cause problems for the server',
              is_flag=True)
@click.option('--filter-file', '-f',
              help='File in yaml format which defines the filters to be used on the corpus',
              default='resources/filters.yaml')
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file')
@corpus
@command_config
def build(config, corpus_data, all_elements, filter_file, out):
    """Run the pipeline extract -> filter -> export in one command."""
    extractor = Extractor(config.verbose, config.gl, corpus=corpus_data)
    corpus_filter = Filter(config.verbose, corpus=corpus_data)

    extractor.extract(all_elements=all_elements)
    corpus_filter.load_filters(filter_file=filter_file)
    corpus_filter.filter()

    exporter = Exporter(config.verbose, corpus=corpus_filter.filtered_corpus, format_str="json")
    exporter.export(out=out)


@cli.command()
@click.option('--all-elements', '-a',
              help='Get all elements available in the GitLab instance WARNING: This might take a long time and might '
                   'cause problems for the server',
              is_flag=True)
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file')
@corpus
@command_config
def extract(config, corpus_data, all_elements, out):
    """Extract projects from the specified GitLab instance and write the output to a file."""
    extractor = Extractor(config.verbose, config.gl, corpus=corpus_data)
    exporter = Exporter(config.verbose, corpus=corpus_data, format_str="json")

    extractor.extract(all_elements=all_elements)
    exporter.export(out=out)


@cli.command()
@click.option('--filter-file', '-f',
              help='File in yaml format which defines the filters to be used on the corpus',
              default='resources/filters.yaml')
@click.option('--input-file', '-i', default='out/corpus.json',
              help='Specifies the file to load the corpus from')
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file')
@corpus
@command_config
def filter(config, corpus_data, filter_file, input_file, out):
    """Apply filters on a previously extracted corpus."""
    corpus_filter = Filter(config.verbose, corpus=corpus_data, from_file=True, file=input_file)

    corpus_filter.load_filters(filter_file=filter_file)
    corpus_filter.filter()

    exporter = Exporter(config.verbose, corpus=corpus_filter.filtered_corpus, format_str="json")
    exporter.export(out=out)


@cli.command()
@click.option('--input-file', '-i', default='out/corpus.json',
              help='Specifies the file to load the corpus from')
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file')
@corpus
@command_config
def export(config, corpus_data, input_file, out):
    """Export a previously extracted (and maybe filtered) corpus to another format."""
    exporter = Exporter(config.verbose, corpus=corpus_data, format_str="json", from_file=True, file=input_file)
    exporter.export(out=out)


if __name__ == '__main__':
    cli(['--config-path=../resources/gitlab.cfg', 'build', '--filter-file=../resources/filters.yaml',
         '--out=../out/corpus.json'])
