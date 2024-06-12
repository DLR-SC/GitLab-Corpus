# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import sys
import click
import gitlab
import logging
from corpus.extract import Extractor
from corpus.export import Exporter
from corpus.filter import Filter
from utils.helpers import Corpus, Config, load_neo4j_config

logging.basicConfig(filename="corpus.log", filemode="w")
logging.getLogger().addHandler((logging.StreamHandler(sys.stdout)))

# instance of a corpus that can be passed as click annotation
corpus = click.make_pass_decorator(Corpus, ensure=True)

# instance of class config, which stores parameters for later use
command_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--gl-config', '-g', default='resources/gitlab.cfg',
              help='Path to the GitLab config file', show_default=True)
@click.option('--neo4j-config', '-n', default='resources/neo4j.cfg',
              help='Path to the Neo4J config file', show_default=True)
@click.option('--source', '-s',
              help='Name of the GitLab instance, you want to analyze, if not the default value of your configuration')
@click.option('--verbose', '-v', default=False,
              help='Prints more output during execution')
@command_config
def cli(config, gl_config, neo4j_config, source, verbose):
    """Entry point to the corpus cli."""
    config.gl = gitlab.Gitlab.from_config(source, [gl_config])
    config.verbose = verbose
    config.neo4j_config = load_neo4j_config(neo4j_config)


@cli.command()
@click.option('--all-elements', '-a',
              help='Get all elements available in the GitLab instance WARNING: This might take a long time and might '
                   'cause problems for the server',
              is_flag=True)
@click.option('--filter-file', '-f',
              help='File in yaml format which defines the filters to be used on the corpus',
              default='resources/filters.yaml', show_default=True)
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file', show_default=True)
@click.option('--output-format', '-F', default='json',
              help='Specifies the output format', show_default=True)
@click.option('--include-private', '-p', is_flag=True,
              help='If set, GitLab projects with visibility private will be included as well')
@corpus
@command_config
def build(config, corpus_data, all_elements, filter_file, out, output_format, include_private):
    """Run the pipeline extract -> filter -> export in one command."""
    extractor = Extractor(config.verbose, config.gl, corpus=corpus_data)
    corpus_filter = Filter(config.verbose, corpus=corpus_data, from_file=False)

    extractor.extract(all_elements=all_elements, include_private=include_private)
    corpus_filter.load_filters(filter_file=filter_file)
    corpus_filter.filter()

    exporter = Exporter(config, corpus=corpus_filter.filtered_corpus, format_str=output_format, from_file=False)
    exporter.export(out=out)


@cli.command()
@click.option('--all-elements', '-a',
              help='Get all elements available in the GitLab instance WARNING: This might take a long time and might '
                   'cause problems for the server',
              is_flag=True)
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file', show_default=True)
@click.option('--include-private', '-p', is_flag=True,
              help='If set, GitLab projects with visibility private will be included as well')
@corpus
@command_config
def extract(config, corpus_data, all_elements, out, include_private):
    """Extract projects from the specified GitLab instance and write the output to a file."""
    extractor = Extractor(config.verbose, config.gl, corpus=corpus_data)
    exporter = Exporter(config, corpus=corpus_data, format_str="json")

    extractor.extract(all_elements=all_elements, include_private=include_private)
    exporter.export(out=out)


@cli.command()
@click.option('--filter-file', '-f',
              help='File in yaml format which defines the filters to be used on the corpus',
              default='resources/filters.yaml', show_default=True)
@click.option('--input-file', '-i', default='out/corpus.json',
              help='Specifies the file to load the corpus from', show_default=True)
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file', show_default=True)
@corpus
@command_config
def filter(config, corpus_data, filter_file, input_file, out):
    """Apply filters on a previously extracted corpus."""
    corpus_filter = Filter(config.verbose, corpus=corpus_data, from_file=True, file=input_file)

    corpus_filter.load_filters(filter_file=filter_file)
    corpus_filter.filter()

    exporter = Exporter(config, corpus=corpus_filter.filtered_corpus, format_str="json")
    exporter.export(out=out)


@cli.command()
@click.option('--input-file', '-i', default='out/corpus.json',
              help='Specifies the file to load the corpus from', show_default=True)
@click.option('--out', '-o', default='out/corpus.json',
              help='Specifies the output file', show_default=True)
@click.option('--output-format', '-F', default='json',
              help='Specifies the output format', show_default=True)
@corpus
@command_config
def export(config, corpus_data, input_file, out, output_format):
    """Export a previously extracted (and maybe filtered) corpus to another format."""
    exporter = Exporter(config, corpus=corpus_data, format_str=output_format, from_file=True, file=input_file)
    exporter.export(out=out)


if __name__ == '__main__':
    # cli(['--gl-config=../resources/gitlab.cfg', '--neo4j-config=../resources/neo4j.cfg', 'export',
    #      '--input-file=../out/test_corpus.json ',
    #      '--output-format=neo4j', '--out=../out/corpus.json'])
    cli(['--gl-config=../resources/gitlab.cfg', '--neo4j-config=../resources/neo4j.cfg', 'build',
         '--out=../out/corpus.json', '--filter-file=../resources/filters.yaml'])
