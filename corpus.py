import json
import click
import gitlab

corpus_dict = {"projects": [],
               "groups": [],
               "mergerequests": []
               }


def append_to_corpus(obj, category=""):
    """This helper function appends a JSON object to the corpus."""
    global corpus_dict
    corpus_dict[category].append(obj)


@click.command()
@click.option('--config-path', default='./gitlab.cfg',
              help='Path to the config file')
@click.option('--source',
              help='Name of the GitLab instance, you want to analyse, if not the default value of your configuration')
@click.option('--all-elements',
              help='Get all elements available in the GitLab instance WARNING: This might take a long time and might '
                   'cause problems for the server',
              is_flag=True)
@click.argument('out', type=click.File('w'), default='./out.json')
def cli(config_path, source, all_elements, out):
    """This tool creates a corpus of all available software projects in a GitLab instance and writes its output to
    the ``out`` file (default: ``./out.json``)."""
    gl = gitlab.Gitlab.from_config(source, config_path)

    projects = gl.projects.list(all=all_elements)
    for project in projects:
        append_to_corpus(project.attributes, category="projects")

    groups = gl.groups.list(all=all_elements)
    for group in groups:
        append_to_corpus(group.attributes, category="groups")

    mergerequests = gl.mergerequests.list(all=all_elements)
    for mergerequest in mergerequests:
        append_to_corpus(mergerequest.attributes, category="mergerequests")

    json.dump(corpus_dict, out, indent=4)


if __name__ == '__main__':
    cli()
