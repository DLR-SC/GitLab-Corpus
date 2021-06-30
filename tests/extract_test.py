# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import gitlab
import pytest
from extract import Extractor
from unittest import mock
from gitlab.v4.objects.projects import ProjectManager
from utils.helpers import Corpus


class Issues:
    def __init__(self):
        self.attributes = {
            'state': 'opened',
            'description': 'Test issue',
            'author': {
                'state': 'active',
                'id': '123abc',
                'name': 'Test User',
                'username': 'test_user'
            },
            'assignees': [{
                'state': 'active',
                'id': '123abd',
                'name': 'Other User',
                'username': 'other_user'
            }],
            'project_id': 1,
            'type': 'ISSUE',
            'updated_at': '2021-01-04T15:31:51.081Z',
            'id': 70,
            'has_tasks': True,
            'task_status': '10 of 15 tasks completed',
        }

    def list(self, all):
        return [self]


class Commits:

    def __init__(self):
        self.attributes = {
            'id': '123abc',
            'short_id': '1a',
            'title': 'Initial commit',
            'author_name': 'Test User',
            'author_email': 'test@us.er',
            'authored_date': '2021-09-20T12:00:00+01:00',
            'committer_name': 'Tester',
            'committer_email': 'tester@example.com',
            'committed_date': '2021-09-20T12:00:00+01:00',
            'created_at': '2021-09-20T12:00:00+01:00',
            'message': 'test commit',
            'parent_ids': [
                '456def'
            ],
            'web_url': 'test.com'
        }

    def list(self, all):
        return [self]


class Members:

    def __init__(self):
        self.attributes = {
            "id": 1,
            "username": "test_user",
            "name": "Test User",
            "state": "active",
            "last_activity_on": "2021-06-09",
            "membership_type": "group_member",
            "removable": True
        }

    def list(self, all):
        return [self]


class Additionalstatistics:

    def get(self):
        raise gitlab.exceptions.GitlabGetError


class Issuestatistics:

    def __init__(self):
        self.attributes = {"statistics": {"counts": {"all": 1, "closed": 0, "opened": 1}}}

    def get(self, scope):
        return self


class Project:

    def __init__(self):
        self.attributes = {'id': 1, 'description': 'test description', 'name': 'Test Project',
                           'created_at': '2021-05-10T15:00:00.000Z', 'default_branch': 'master',
                           'last_activity_at': '2021-05-10T16:00:00.000Z', 'archived': False,
                           'visibility': 'internal', 'issues_enabled': True, 'creator_id': 10,
                           'open_issues_count': 0}
        self.issuesstatistics = Issuestatistics()
        self.additionalstatistics = Additionalstatistics()
        self.members_all = Members()
        self.commits = Commits()
        self.issues = Issues()
        self.lgs = {"Python": 80.0, "HTML": 20.0}
        self.repo_tree = [{"id": "hash123", "name": "test.py", "type": "blob"}]

    def languages(self):
        return self.lgs

    def repository_tree(self, ref):
        return self.repo_tree


def pm_list(all):
    return [Project()]


def setup_gitlab_mock():
    # project manager mock
    project_manager = mock.Mock(spec=ProjectManager, list=pm_list)

    # gitlab mock
    gl = mock.Mock(projects=project_manager)

    return gl


@pytest.mark.slow
def test_extract():
    extractor = Extractor(False, setup_gitlab_mock(), Corpus())
    extractor.extract(False)

    project = extractor.corpus.data['Projects'][0]
    assert project['id'] == 1
    assert project['description'] == 'test description'
    assert project['name'] == 'Test Project'
    assert project['created_at'] == '2021-05-10T15:00:00.000Z'
    assert project['default_branch'] == 'master'
    assert project['last_activity_at'] == '2021-05-10T16:00:00.000Z'
    assert not project['archived']
    assert project['visibility'] == 'internal'
    assert project['issues_enabled']
    assert project['creator_id'] == 10
    assert project['open_issues_count'] == 0
    assert project['issue_statistics'] == {"counts": {"all": 1, "closed": 0, "opened": 1}}
    assert project['languages'] == {"Python": 80.0, "HTML": 20.0}
    assert project['commits'] == [
                {
                    'id': '123abc',
                    'short_id': '1a',
                    'title': 'Initial commit',
                    'author_name': 'Test User',
                    'author_email': 'test@us.er',
                    'authored_date': '2021-09-20T12:00:00+01:00',
                    'committer_name': 'Tester',
                    'committer_email': 'tester@example.com',
                    'committed_date': '2021-09-20T12:00:00+01:00',
                    'created_at': '2021-09-20T12:00:00+01:00',
                    'message': 'test commit',
                    'parent_ids': [
                        '456def'
                    ],
                    'web_url': 'test.com'
                }
            ]
    assert project['first_commit'] == {
                'id': '123abc',
                'short_id': '1a',
                'title': 'Initial commit',
                'author_name': 'Test User',
                'author_email': 'test@us.er',
                'authored_date': '2021-09-20T12:00:00+01:00',
                'committer_name': 'Tester',
                'committer_email': 'tester@example.com',
                'committed_date': '2021-09-20T12:00:00+01:00',
                'created_at': '2021-09-20T12:00:00+01:00',
                'message': 'test commit',
                'parent_ids': [
                    '456def'
                ],
                'web_url': 'test.com'
            }
    assert project['last_commit'] == {
                'id': '123abc',
                'short_id': '1a',
                'title': 'Initial commit',
                'author_name': 'Test User',
                'author_email': 'test@us.er',
                'authored_date': '2021-09-20T12:00:00+01:00',
                'committer_name': 'Tester',
                'committer_email': 'tester@example.com',
                'committed_date': '2021-09-20T12:00:00+01:00',
                'created_at': '2021-09-20T12:00:00+01:00',
                'message': 'test commit',
                'parent_ids': [
                    '456def'
                ],
                'web_url': 'test.com'
            }
    assert project['issues'] == [
                {
                    'state': 'opened',
                    'description': 'Test issue',
                    'author': {
                        'state': 'active',
                        'id': '123abc',
                        'name': 'Test User',
                        'username': 'test_user'
                    },
                    'assignees': [{
                        'state': 'active',
                        'id': '123abd',
                        'name': 'Other User',
                        'username': 'other_user'
                    }],
                    'project_id': 1,
                    'type': 'ISSUE',
                    'updated_at': '2021-01-04T15:31:51.081Z',
                    'id': 70,
                    'has_tasks': True,
                    'task_status': '10 of 15 tasks completed',
                }
            ]
    assert all(elem in project['contributors'] for elem in ['test_user', 'other_user'])
    assert project['files'] == [{"id": "hash123", "name": "test.py", "type": "blob"}]


if __name__ == '__main__':
    test_extract()
