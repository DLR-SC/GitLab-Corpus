# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import click
import gitlab
from gitlab.v4.objects import ProjectManager


class Extractor:
    """This class provides a method to extract projects of GitLab instance.

    Methods:
        __init__(self, verbose, gitlab_manager, corpus)
        extract(self, all_elements)
    """

    def __init__(self, verbose, gitlab_manager, corpus):
        """Extractor class constructor to initialize the object.
        :param verbose: Prints more output, if set to ``True``
        :param gitlab_manager: Manager object for python-gitlab
        :param corpus: Initialized corpus object, which will be used to save the projects data
        """
        self.gl = gitlab_manager
        self.verbose = verbose
        self.managers = [self.gl.projects]
        self.corpus = corpus

    def extract(self, all_elements):
        """This method extracts the projects of the defined GitLab instance and stores them in the corpus attribute.
        :param all_elements: Ignores the pagination of the GitLab-API and extracts all projects, if set to ``True``.
        """
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
                        contributors = set()
                        external_contributors = set()
                        contributor_names = set()

                        if project_dict['visibility'] != "private":

                            project_dict['issue_statistics'] = \
                                project.issuesstatistics.get(scope="all").attributes["statistics"]

                            project_dict['languages'] = project.languages()

                            members = project.members_all.list(all=True)

                            try:
                                commits = project.commits.list(all=True)
                                commit_list = []
                                for commit in commits:
                                    commit_dict = commit.attributes
                                    commit_list.append(commit_dict)
                                    contributor_names.add(commit_dict['author_name'])

                                if len(commit_list) > 0:
                                    project_dict['commits'] = commit_list
                                    project_dict['first_commit'] = commit_list.__getitem__(len(commit_list) - 1)
                                    project_dict['last_commit'] = commit_list.__getitem__(0)
                            except gitlab.exceptions.GitlabListError:
                                pass  # some projects do not have any commits, which leads to this error

                            for member in members:
                                try:
                                    surname, forename = member.attributes['name'].split(', ')
                                    member_name = forename + ' ' + surname
                                except ValueError:
                                    member_name = member.attributes['name']
                                to_be_removed = set()
                                for name in contributor_names:
                                    if member_name == name:
                                        contributors.add(member.attributes['username'])
                                        to_be_removed.add(name)
                                for name in to_be_removed:
                                    contributor_names.remove(name)
                            external_contributors.update(contributor_names)

                            issues = project.issues.list(all=True)
                            issue_list = []
                            for issue in issues:
                                issue_dict = issue.attributes
                                issue_list.append(issue_dict)
                                contributors.add(issue_dict['author']['username'])
                                for assignee in issue_dict['assignees']:
                                    contributors.add(assignee['username'])
                            if len(issue_list) > 0:
                                project_dict['issues'] = issue_list

                            if len(contributors) > 0:
                                project_dict['contributors'] = list(contributors)

                            if len(external_contributors) > 0:
                                project_dict['external_contributors'] = list(external_contributors)

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
