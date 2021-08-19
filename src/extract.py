# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import click
import gitlab
from gitlab.v4.objects import ProjectManager


def get_users(project):
    try:
        users = project.users.list()
        user_list = []
        for user in users:
            user_dict = user.attributes
            user_list.append(user_dict)

        if len(user_list) > 0:
            return user_list
    except gitlab.exceptions.GitlabListError:
        pass


def get_commits(project):
    try:
        commits = project.commits.list(all=True)
        commit_list = []
        for commit in commits:
            commit_dict = commit.attributes
            commit_list.append(commit_dict)

        if len(commit_list) > 0:
            return commit_list, commit_list.__getitem__(len(commit_list) - 1), commit_list.__getitem__(0)
    except gitlab.exceptions.GitlabListError:
        pass  # some projects do not have any commits, which leads to this error


def get_contributors(project):
    try:
        contributors = project.repository_contributors()
        return contributors
    except gitlab.exceptions.GitlabGetError:
        pass  # when no contributors exist


def get_issues(project):
    issues = project.issues.list(all=True)
    issue_list = []
    for issue in issues:
        issue_dict = issue.attributes
        issue_list.append(issue_dict)
    if len(issue_list) > 0:
        return issue_list


def get_mergerequests(project):
    try:
        mergerequests = project.mergerequests.list(state='all')
        mr_list = []
        for mr in mergerequests:
            mr_dict = mr.attributes
            mr_list.append(mr_dict)
        if len(mr_list) > 0:
            return mr_list
    except gitlab.exceptions.GitlabListError:
        pass  # occurs when no mergerequests exist


def get_pipelinestatistics(project):
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
        return pipelines_dict
    except gitlab.exceptions.GitlabListError:
        pass


def get_milestones(project):
    try:
        milestones = project.milestones.list()
        ms_list = []
        for ms in milestones:
            ms_dict = ms.attributes
            ms_list.append(ms_dict)
        if len(ms_list) > 0:
            return ms_list
    except gitlab.exceptions.GitlabListError:
        pass


def get_rootdir(project, default_branch):
    try:
        return project.repository_tree(ref=default_branch)
    except (gitlab.exceptions.GitlabGetError, gitlab.exceptions.GitlabHttpError, KeyError):
        pass


def get_projectstatistics(project, verbose, name):
    try:
        return project.additionalstatistics.get().attributes
    except gitlab.exceptions.GitlabGetError:
        if verbose:
            click.echo("\n Project statistics for project {} could not be fetched. You might "
                       "need write access to fix this.".format(name))
        else:
            pass


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

                        # only extract public or internal projects
                        if project_dict['visibility'] != "private":

                            # extract issue statistics
                            project_dict['issue_statistics'] = \
                                project.issuesstatistics.get(scope="all").attributes["statistics"]

                            # extract project languages
                            project_dict['languages'] = project.languages()

                            # extract members of the project
                            project_dict['users'] = get_users(project)

                            # extract commits
                            project_dict['commits'], project_dict['first_commit'], project_dict['last_commit'] = \
                                get_commits(project)

                            # extract contributors
                            project_dict['contributors'] = get_contributors(project)

                            # extract all issues of a project and add further contributors to list
                            project_dict['issues'] = get_issues(project)

                            # extract all merge requests
                            project_dict['mergerequests'] = get_mergerequests(project)

                            # extract pipeline statistics
                            project_dict['pipelines'] = get_pipelinestatistics(project)

                            # extract milestones
                            project_dict['milestones'] = get_milestones(project)

                            # extract the main directory of the project
                            project_dict['files'] = get_rootdir(project, project_dict['default_branch'])

                            # try to extract project statistics (only works for projects where the user has write
                            # access)
                            project_dict['project_statistics'] = get_projectstatistics(project, self.verbose,
                                                                                       project_dict['name'])

                            # add all extracted data to the corpus
                            self.corpus.data["Projects"].append(project_dict)
