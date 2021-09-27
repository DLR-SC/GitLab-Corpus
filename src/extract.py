# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import click
import gitlab
from gitlab.v4.objects import ProjectManager

"""
.. module:: extract
.. moduleauthor:: Emanuel Caricato <emanuel.caricato@dlr.de>
"""


def get_users(project):
    """
    This function returns a list of users for a specified project.

    :param project: The project, that is to be extracted.
    :return: A list of users. None, if no users are found.
    :rtype: list or None

    """
    try:
        user_list = [user.attributes for user in project.users.list()]
        if len(user_list) > 0:
            return user_list
        return None
    except gitlab.exceptions.GitlabListError:
        return None


def get_commits(project):
    """
    This function returns a list of commits, the last, and the first commit for a specified project.

    :param project: The project, that is to be extracted.
    :return: A list of commits, the last, and the first commit. None, if no commits are found.
    :rtype: tuple of (list, dict, dict) or (None, None, None)

    """
    try:
        commit_list = [commit.attributes for commit in project.commits.list(all=True)]
        if len(commit_list) > 0:
            return commit_list, commit_list.__getitem__(len(commit_list) - 1), commit_list.__getitem__(0)
        return None, None, None
    except gitlab.exceptions.GitlabListError:
        return None, None, None


def get_contributors(project):
    """
    This function returns a list of contributors for a specified project.

    :param project: The project, that is to be extracted.
    :return: A list of contributors. None, if no contributors are found.
    :rtype: list or None

    """
    try:
        contributors = project.repository_contributors()
        return contributors
    except gitlab.exceptions.GitlabGetError:
        return None


def get_issues(project):
    """
    This function returns a list of issues for a specified project.

    :param project: The project, that is to be extracted.
    :return: A list of issues. None, if no issues are found.
    :rtype: list or None

    """
    issue_list = [issue.attributes for issue in project.issues.list(all=True)]
    if len(issue_list) > 0:
        return issue_list
    return None


def get_mergerequests(project):
    """
    This function returns a list of mergerequests for a specified project.

    :param project: The project, that is to be extracted.
    :return: A list of mergerequests. None, if no mergerequests are found.
    :rtype: list or None

    """
    try:
        mergerequests = project.mergerequests.list(state='all')
        mr_list = []
        for mr in mergerequests:
            mr_dict = mr.attributes
            mr_commits = mr.commits()
            mr_dict["commits"] = []
            for commit in mr_commits:
                mr_dict["commits"].append(commit.attributes)
            mr_dict["close_issues"] = []
            close_issues = mr.closes_issues()
            for close_issue in close_issues:
                mr_dict["close_issues"].append(close_issue.attributes)
            mr_list.append(mr_dict)
        if len(mr_list) > 0:
            return mr_list
        return None
    except gitlab.exceptions.GitlabListError:
        return None


def get_pipelinestatistics(project):
    """
    This function returns the pipeline statistics for a specified project.

    :param project: The project, that is to be extracted.
    :return: A dictionary of the pipeline statistics. None, if no mergerequests are found.
    :rtype: dict or None

    """
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
        return None


def get_milestones(project):
    """
    This function returns a list of milestones for a specified project.

    :param project: The project, that is to be extracted.
    :return: A list of milestones. None, if no milestones are found.
    :rtype: list or None

    """
    try:
        ms_list = [milestone.attributes for milestone in project.milestones.list()]
        if len(ms_list) > 0:
            return ms_list
        return None
    except gitlab.exceptions.GitlabListError:
        return None


def get_rootdir(project, project_dict):
    """
    This function returns a list of files from the root directory for a specified project.

    :param project: The project, that is to be extracted.
    :param project_dict: The dictionary of the projects attributes, to get the default branch.
    :return: A list of files. None, if no files are found.
    :rtype: list or None

    """
    try:
        return project.repository_tree(ref=project_dict['default_branch'])
    except (gitlab.exceptions.GitlabGetError, gitlab.exceptions.GitlabHttpError, KeyError):
        return None


def get_projectstatistics(project, verbose, name):
    """
    This function returns the project statistics for a specified project.

    :param project: The project, that is to be extracted.
    :param verbose: Boolean value to print extra output.
    :param name: Name of the project.
    :return: A dict of the projects statistics. None, if no statistics are found or if the rights are not sufficient to
        fetch the project statistics.
    :rtype: dict or None

    """
    try:
        return project.additionalstatistics.get().attributes
    except gitlab.exceptions.GitlabGetError:
        if verbose:
            click.echo("\n Project statistics for project {} could not be fetched. You might "
                       "need write access to fix this.".format(name))
        else:
            pass
        return None


def get_releases(project):
    """
    This function returns a list of releases for a specified project.

    :param project: The project, that is to be extracted.
    :return: A list of releases. None, if no releases are found.
    :rtype: list or None

    """
    try:
        rs_list = [release.attributes for release in project.releases.list()]
        if len(rs_list) > 0:
            return rs_list
        return None
    except gitlab.exceptions.GitlabListError:
        return None


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
            objects = manager.list(all=all_elements)  # gets all managers available (for projects, groups, users..)
            if isinstance(manager, ProjectManager):
                self.extract_projects(objects)

    def extract_projects(self, objects):
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
                    users = get_users(project)
                    if users is not None:
                        project_dict['users'] = users

                    # extract commits
                    commits, first_commit, last_commit = get_commits(project)
                    if commits is not None:
                        project_dict['commits'], project_dict['first_commit'], project_dict['last_commit'] = \
                            commits, first_commit, last_commit

                    # extract contributors
                    contributors = get_contributors(project)
                    if contributors is not None:
                        project_dict['contributors'] = contributors

                    # extract all issues
                    issues = get_issues(project)
                    if issues is not None:
                        project_dict['issues'] = issues

                    # extract all merge requests
                    mergerequests = get_mergerequests(project)
                    if mergerequests is not None:
                        project_dict['mergerequests'] = mergerequests

                    # extract pipeline statistics
                    pipelinestatistics = get_pipelinestatistics(project)
                    if pipelinestatistics is not None:
                        project_dict['pipelines'] = pipelinestatistics

                    # extract milestones
                    milestones = get_milestones(project)
                    if milestones is not None:
                        project_dict['milestones'] = milestones

                    # extract the main directory of the project
                    rootdir = get_rootdir(project, project_dict)
                    if rootdir is not None:
                        project_dict['files'] = rootdir

                    # try to extract project statistics (only works for projects where the user has write
                    # access)
                    project_statistics = get_projectstatistics(project, self.verbose, project_dict['name'])
                    if project_statistics is not None:
                        project_dict['project_statistics'] = project_statistics

                    # extract releases
                    releases = get_releases(project)
                    if releases is not None:
                        project_dict['releases'] = releases

                    # add all extracted data to the corpus
                    self.corpus.data["Projects"].append(project_dict)
