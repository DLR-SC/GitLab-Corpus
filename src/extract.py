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

                        # only extract public or internal projects
                        if project_dict['visibility'] != "private":

                            # extract issue statistics
                            project_dict['issue_statistics'] = \
                                project.issuesstatistics.get(scope="all").attributes["statistics"]

                            # extract project languages
                            project_dict['languages'] = project.languages()

                            # extract members of the project
                            members = project.members_all.list(all=True)

                            # extract commits and extract committer names of the project
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

                            # match committer names to members to get the corresponding username
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

                            # extract all issues of a project and add further contributors to list
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

                            # add contributors to project data
                            if len(contributors) > 0:
                                project_dict['contributors'] = list(contributors)

                            # add all contributors that are not in the member list as external
                            if len(external_contributors) > 0:
                                project_dict['external_contributors'] = list(external_contributors)

                            # extract all merge requests
                            try:
                                mergerequests = project.mergerequests.list(state='all')
                                mr_list = []
                                for mr in mergerequests:
                                    mr_dict = mr.attributes
                                    mr_list.append(mr_dict)
                                if len(mr_list) > 0:
                                    project_dict['mergerequests'] = mr_list
                            except gitlab.exceptions.GitlabListError:
                                pass    # occurs when no mergerequests exist

                            # extract pipeline statistics
                            try:
                                pipelines = project.pipelines.list()
                                pipelines_dict = {"total": 0, "successful": 0, "failed": 0, "canceled": 0, "pending": 0}
                                for pipeline in pipelines:
                                    status = pipeline.attributes['status']
                                    if status == "success":
                                        pipelines_dict['successful'] += 1
                                    elif status == 'failed':
                                        pipelines_dict['failed'] += 1
                                    elif status == 'canceled':
                                        pipelines_dict['canceled'] += 1
                                    elif status == 'pending':
                                        pipelines_dict['pending'] += 1
                                pipelines_dict['total'] = pipelines_dict['successful'] + pipelines_dict['failed'] \
                                                          + pipelines_dict['canceled'] + pipelines_dict['pending']
                                project_dict['pipelines'] = pipelines_dict
                            except gitlab.exceptions.GitlabListError:
                                pass

                            # extract the main directory of the project
                            try:
                                project_dict['files'] = project.repository_tree(ref=project_dict['default_branch'])
                            except (gitlab.exceptions.GitlabGetError, gitlab.exceptions.GitlabHttpError, KeyError):
                                project_dict['files'] = "None"

                            # try to extract project statistics (only works for projects where the user has write
                            # access)
                            try:
                                project_dict['project_statistics'] = project.additionalstatistics.get().attributes
                            except gitlab.exceptions.GitlabGetError:
                                if self.verbose:
                                    click.echo("\n Project statistics for project {} could not be fetched. You might "
                                               "need write access to fix this.".format(project_dict["name"]))
                                else:
                                    pass

                            # add all extracted data to the corpus
                            self.corpus.data["Projects"].append(project_dict)
