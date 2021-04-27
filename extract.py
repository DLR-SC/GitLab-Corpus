# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import click
import gitlab


def get_category(manager_string):
    """This helper method extracts the category"""
    start_index = -1
    for i in range(0, 3):
        start_index = manager_string.find(".", start_index + 1)
    end_index = manager_string.find("Manager")
    return manager_string[start_index + 1:end_index] + "s"


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
            category = get_category(str(manager))
            if category == 'Projects':
                click.echo("Extracting...")
                with click.progressbar(objects) as bar:
                    for project in bar:
                        project_dict = project.attributes

                        project_dict['issue_statistics'] = \
                            project.issuesstatistics.get(scope="all").attributes["statistics"]

                        project_dict['languages'] = project.languages()

                        project_dict['is_software'] = True if not project_dict['languages'] else False

                        try:
                            project_dict['files'] = project.repository_tree(ref=project_dict['default_branch'])
                        except (gitlab.exceptions.GitlabGetError, gitlab.exceptions.GitlabHttpError, KeyError) as e:
                            project_dict['files'] = "None"

                        try:
                            project_dict['project_statistics'] = project.additionalstatistics.get().attributes
                        except gitlab.exceptions.GitlabGetError:
                            if self.verbose:
                                click.echo("\n Project statistics for project {} could not be fetched. You might need "
                                           "write access to fix this.")
                            else:
                                pass

                        self.corpus.data[category].append(project_dict)
