# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT
import gitlab
import pytest
from extract import Extractor
from unittest import mock
from gitlab.v4.objects.projects import ProjectManager
from utils.helpers import Corpus


class Additionalstatistics:

    def get(self):
        raise gitlab.exceptions.GitlabGetError


class Issuestatistics:

    def __init__(self):
        self.attributes = {"statistics": {"counts": {"all": 0, "closed": 0, "opened": 0}}}

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

    assert extractor.corpus.data == {"Projects": [
        {
            'id': 1,
            'description': 'test description',
            'name': 'Test Project',
            'created_at': '2021-05-10T15:00:00.000Z',
            'default_branch': 'master',
            'last_activity_at': '2021-05-10T16:00:00.000Z',
            'archived': False,
            'visibility': 'internal',
            'issues_enabled': True,
            'creator_id': 10,
            'open_issues_count': 0,
            'issue_statistics': {
                "counts": {
                    "all": 0,
                    "closed": 0,
                    "opened": 0
                }
            },
            'languages': {
                "Python": 80.0,
                "HTML": 20.0
            },
            'files': [
                {
                    "id": "hash123",
                    "name": "test.py",
                    "type": "blob"
                }
            ]
        }
    ]}


if __name__ == '__main__':
    test_extract()
