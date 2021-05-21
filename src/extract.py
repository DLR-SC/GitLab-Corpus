# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import click
import gitlab
from gitlab.v4.objects import ProjectManager


class Extractor:
    """This class represents the extraction module."""

    def __init__(self, verbose, gitlab_manager, corpus):
        self.gl = gitlab_manager
        self.verbose = verbose
        self.managers = [self.gl.projects]
        self.corpus = corpus

    def extract(self, all_elements):

        for manager in self.managers:
            click.echo("Retrieving projects...")
            objects = manager.list(all=all_elements)
            if isinstance(manager, ProjectManager):
                click.echo("Extracting...")
                with click.progressbar(objects) as bar:
                    if self.verbose:
                        click.echo("{} projects found.".format(bar.length))
                    for project in bar:
                        project_dict = project.attributes

                        if project_dict['visibility'] != "private":

                            project_dict['issue_statistics'] = \
                                project.issuesstatistics.get(scope="all").attributes["statistics"]

                            project_dict['languages'] = project.languages()

                            try:
                                project_dict['files'] = project.repository_tree(ref=project_dict['default_branch'])
                            except (gitlab.exceptions.GitlabGetError, gitlab.exceptions.GitlabHttpError, KeyError):
                                project_dict['files'] = "None"

                            try:
                                project_dict['project_statistics'] = project.additionalstatistics.get().attributes
                            except gitlab.exceptions.GitlabGetError:
                                if self.verbose:
                                    click.echo("\n Project statistics for project {} could not be fetched. You might "
                                               "need write access to fix this.".format(project_dict["name"]))
                                else:
                                    pass

                            self.corpus.data["Projects"].append(project_dict)
