# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import gitlab
import pytest
from extract import Extractor
from unittest import mock
from gitlab.v4.objects.projects import ProjectManager
from utils.helpers import Corpus


class Milestones:

    def __init__(self):
        self.attributes = {
            "id": 1,
            "iid": 2,
            "project_id": 123,
            "title": "1.0",
            "description": "Version",
            "due_date": "2021-08-04",
            "start_date": "2021-07-10",
            "state": "active",
            "updated_at": "2021-07-12T19:31:15Z",
            "created_at": "2021-07-10T08:13:12Z",
            "expired": False
        }

    def list(self):
        return [self]


class Pipelines:

    def __init__(self):
        self.attributes = {
            "id": 12,
            "project_id": 123,
            "status": "success",
            "ref": "test-pipeline",
            "sha": "asd78h8",
            "web_url": "https://gitlab.dlr.de/test/testproject/pipelines/12",
            "created_at": "2021-08-11T14:20:34.085Z",
            "updated_at": "2021-08-11T14:31:30.169Z"
        }

    def list(self):
        return [self]


class Mergerequests:
    def __init__(self):
        self.attributes = {
            "id": 1,
            "iid": 1,
            "project_id": 3,
            "title": "testmr",
            "description": "test merge request",
            "state": "merged",
            "merged_by": {
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            },
            "merged_at": "2021-07-07T11:16:17.520Z",
            "created_at": "2021-06-29T08:46:00Z",
            "updated_at": "2021-06-29T08:46:00Z",
            "target_branch": "master",
            "source_branch": "master",
            "author": {
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            },
            "assignee": {
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            },
            "assignees": [{
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            }],
            "reviewers": [{
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            }],
            "source_project_id": 2,
            "target_project_id": 3,
            "draft": False,
            "work_in_progress": False,
            "merge_when_pipeline_succeeds": True,
            "merge_status": "can_be_merged",
            "sha": "678235980712",
            "squash": False,
            "task_completion_status": {
                "count": 0,
                "completed_count": 0
            },
            "has_conflicts": False,
            "blocking_discussions_resolved": True
        }

    def list(self, state):
        return [self]


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


class Users:

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

    def list(self):
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
        self.users = Users()
        self.commits = Commits()
        self.issues = Issues()
        self.milestones = Milestones()
        self.lgs = {"Python": 80.0, "HTML": 20.0}
        self.repo_tree = [{"id": "hash123", "name": "test.py", "type": "blob"}]
        self.mergerequests = Mergerequests()
        self.pipelines = Pipelines()

    def repository_contributors(self):
        return self.users

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
    assert project['users'] == [{
        "id": 1,
        "username": "test_user",
        "name": "Test User",
        "state": "active",
        "last_activity_on": "2021-06-09",
        "membership_type": "group_member",
        "removable": True
    }]
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
    assert project['contributors'].attributes['username'] == 'test_user'
    assert project['files'] == [{"id": "hash123", "name": "test.py", "type": "blob"}]
    assert project['mergerequests'] == [
        {
            "id": 1,
            "iid": 1,
            "project_id": 3,
            "title": "testmr",
            "description": "test merge request",
            "state": "merged",
            "merged_by": {
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            },
            "merged_at": "2021-07-07T11:16:17.520Z",
            "created_at": "2021-06-29T08:46:00Z",
            "updated_at": "2021-06-29T08:46:00Z",
            "target_branch": "master",
            "source_branch": "master",
            "author": {
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            },
            "assignee": {
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            },
            "assignees": [{
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            }],
            "reviewers": [{
                "id": "123abc",
                "name": "Test User",
                "username": "test_user",
                "state": "active",
            }],
            "source_project_id": 2,
            "target_project_id": 3,
            "draft": False,
            "work_in_progress": False,
            "merge_when_pipeline_succeeds": True,
            "merge_status": "can_be_merged",
            "sha": "678235980712",
            "squash": False,
            "task_completion_status": {
                "count": 0,
                "completed_count": 0
            },
            "has_conflicts": False,
            "blocking_discussions_resolved": True
        }
    ]
    assert project['pipelines'] == {
        "total": 1,
        "successful": 1,
        "failed": 0,
        "canceled": 0,
        "pending": 0
    }
    assert project['milestones'] == [
        {
            "id": 1,
            "iid": 2,
            "project_id": 123,
            "title": "1.0",
            "description": "Version",
            "due_date": "2021-08-04",
            "start_date": "2021-07-10",
            "state": "active",
            "updated_at": "2021-07-12T19:31:15Z",
            "created_at": "2021-07-10T08:13:12Z",
            "expired": False
        }
    ]


if __name__ == '__main__':
    test_extract()
