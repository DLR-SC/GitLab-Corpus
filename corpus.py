import json
import click
import gitlab


@click.command()
@click.option('--config-path', default='./gitlab.cfg',
              help='Path to the config file')
@click.option('--source',
              help='Name of the GitLab instance, you want to analyse, if not the default value of your configuration')
@click.argument('out', type=click.File('w'), default='./out.txt')
def cli(config_path, source, out):
    """This tool creates a corpus of all available software projects in a GitLab instance and writes its output to
    the ``out`` file (default: ``./out.txt``)."""
    gl = gitlab.Gitlab.from_config(source, config_path)

    projects = gl.projects.list()
    for project in projects:
        click.echo(project, file=out)

    groups = gl.groups.list()
    for group in groups:
        click.echo(group, file=out)

    mergerequests = gl.mergerequests.list()
    for mergerequest in mergerequests:
        click.echo(mergerequest, file=out)
