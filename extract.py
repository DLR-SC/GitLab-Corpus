# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import click
import gitlab
import csv


def get_category(manager_string):
    """This helper method extracts the category"""
    start_index = -1
    for i in range(0, 3):
        start_index = manager_string.find(".", start_index + 1)
    end_index = manager_string.find("Manager")
    return manager_string[start_index + 1:end_index] + "s"


class Extractor:
    """This class represents the extraction module."""

    extracted_corpus = {"Projects": [],  # This object represents the output corpus and will exist only once
                        }  # https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables

    def __init__(self, gitlab_manager):
        self.gl = gitlab_manager
        self.managers = [self.gl.projects]
        self.extensions = []
        with open('extensions.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for extension in csv_reader:
                self.extensions.append(extension)

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
                        project_dict['files'] = project.repository_tree(ref=project_dict['default_branch'])
                        project_dict['is_software'] = self.get_project_category(project_dict, project)
                        try:
                            project_dict['project_statistics'] = project.additionalstatistics.get().attributes
                        except gitlab.exceptions.GitlabGetError:
                            pass
                            # click.echo("Project statistics for project {} could not be fetched. You need write access "
                            #            "for the project.".format(project_dict["name"]))
                        self.extracted_corpus[category].append(project_dict)

    def get_project_category(self, project_dict, project):
        if not project_dict['languages']:
            # TODO check if project has releases
            tree = project.repository_tree(ref=project_dict['default_branch'])
            paths = []
            for file in tree:
                if file['type'] == 'tree':
                    paths.append(file['path'])
                    # TODO check subdirectories
                elif file['name'].split(".")[1] in self.extensions:
                    return True
                else:
                    return False
        else:
            return True
