import json
from unittest.mock import patch

from export import Exporter
from utils.helpers import Corpus
from unittest import mock

corpus = Corpus()
corpus.data = {"Projects": [
    {
        'id': 1,
        'description': 'test description',
        'name': 'Test Project',
        'name_with_namespace': 'User, Test / Test Project',
        'path': 'Test Project',
        'path_with_namespace': 'user_t',
        'created_at': '2021-05-10T15:00:00.000Z',
        'default_branch': 'master',
        'tag_list': [],
        'ssh_url_to_repo': 'git@gitlab.example.com:user_t/test_project.git',
        'http_url_to_repo': 'https://gitlab.example.com/user_t/test_project.git',
        'web_url': 'https://gitlab.example.com/user_t/test_project',
        'readme_url': 'null',
        'avatar_url': 'null',
        'forks_count': 0,
        'star_count': 0,
        'last_activity_at': '2021-05-10T16:00:00.000Z',
        'namespace': {
            'id': 123,
            'name': 'User, Test',
            'path': 'user_t',
            'kind': 'user',
            'full_path': 'user_t',
            'parent_id': 'null',
            'avatar_url': 'null',
            'web_url': 'https://gitlab.example.com/user_t'
        },
        '_links': {
            'self': 'https://gitlab.example.de/api/v4/projects/123',
            'issues': 'https://gitlab.example.de/api/v4/projects/123/issues',
            'merge_requests': 'https://gitlab.example.de/api/v4/projects/123/merge_requests',
            'repo_branches': 'https://gitlab.example.de/api/v4/projects/123/repository/branches',
            'labels': 'https://gitlab.example.de/api/v4/projects/123/labels',
            'events': 'https://gitlab.example.de/api/v4/projects/123/events',
            'members': 'https://gitlab.example.de/api/v4/projects/123/members'
        },
        'packages_enabled': True,
        'empty_repo': False,
        'archived': False,
        'visibility': 'internal',
        'owner': {
            'id': 123,
            'name': 'User, Test',
            'username': 'user_t',
            'state': 'active',
            'avatar_url': 'null',
            'web_url': 'https://gitlab.example.com/user_t'
        },
        'resolve_outdated_diff_discussions': False,
        'container_registry_enabled': False,
        'container_expiration_policy': {
            'cadence': '1d',
            'enabled': False,
            'keep_n': 10,
            'older_than': '90d',
            'name_regex': '.*',
            'name_regex_keep': 'null',
            'next_run_at': '2021-07-21T19:50:08.906Z'
        },
        'issues_enabled': True,
        'merge_requests_enabled': True,
        'wiki_enabled': False,
        'jobs_enabled': False,
        'snippets_enabled': False,
        'service_desk_enabled': False,
        'service_desk_address': 'null',
        'can_create_merge_request_in': True,
        'issues_access_level': 'enabled',
        'repository_access_level': 'enabled',
        'merge_requests_access_level': 'enabled',
        'forking_access_level': 'enabled',
        'wiki_access_level': 'disabled',
        'builds_access_level': 'disabled',
        'snippets_access_level': 'disabled',
        'pages_access_level': 'enabled',
        'operations_access_level': 'enabled',
        'analytics_access_level': 'enabled',
        'emails_disabled': False,
        'shared_runners_enabled': True,
        'lfs_enabled': True,
        'creator_id': 123,
        'import_status': 'none',
        'open_issues_count': 0,
        'ci_default_git_depth': 50,
        'ci_forward_deployment_enabled': True,
        'public_jobs': True,
        'build_timeout': 3600,
        'auto_cancel_pending_pipelines': 'enabled',
        'build_coverage_regex': 'null',
        'ci_config_path': 'null',
        'shared_with_groups': [],
        'only_allow_merge_if_pipeline_succeeds': False,
        'allow_merge_on_skipped_pipeline': 'null',
        'restrict_user_defined_variables': False,
        'request_access_enabled': True,
        'only_allow_merge_if_all_discussions_are_resolved': False,
        'remove_source_branch_after_merge': True,
        'printing_merge_request_link_enabled': True,
        'merge_method': 'merge',
        'suggestion_commit_message': 'null',
        'auto_devops_enabled': False,
        'auto_devops_deploy_strategy': 'continuous',
        'autoclose_referenced_issues': True,
        'approvals_before_merge': 0,
        'mirror': False,
        'requirements_enabled': False,
        'security_and_compliance_enabled': False,
        'compliance_frameworks': [],
        'issues_template': 'null',
        'merge_requests_template': 'null',
        'permissions': {
            'project_access': 'null',
            'group_access': 'null'
        },
        'issue_statistics': {
            "counts": {
                "all": 0,
                "closed": 0,
                "opened": 0
            }
        },
        'languages': {
            "Python": 100.0
        },
        'users': [
            {
                'id': 123,
                'name': 'User, Test',
                'username': 'user_t',
                'state': 'active',
                'avatar_url': 'null',
                'web_url': 'https://gitlab.example.com/user_t'
            }
        ],
        'commits': [
            {
                'id': '123abc',
                'short_id': '123abc',
                'created_at': '2021-07-20T21:50:48.000+02:00',
                'parent_ids': [],
                'title': 'init',
                'message': 'init\n',
                'author_name': 'User, Test',
                'author_email': 'test.user@example.com',
                'authored_date': '2021-07-20T21:50:48.000+02:00',
                'committer_name': 'User, Test',
                'committer_email': 'test.user@example.com',
                'committed_date': '2021-07-20T21:50:48.000+02:00',
                'web_url': 'https://gitlab.example.com/user_t/test_project/-/commit/123abc',
                'project_id': 123
            }
        ],
        'first_commit': {
            'id': '123abc',
            'short_id': '123abc',
            'created_at': '2021-07-20T21:50:48.000+02:00',
            'parent_ids': [],
            'title': 'init',
            'message': 'init\n',
            'author_name': 'User, Test',
            'author_email': 'test.user@example.com',
            'authored_date': '2021-07-20T21:50:48.000+02:00',
            'committer_name': 'User, Test',
            'committer_email': 'test.user@example.com',
            'committed_date': '2021-07-20T21:50:48.000+02:00',
            'web_url': 'https://gitlab.example.com/user_t/test_project/-/commit/123abc',
            'project_id': 123
        },
        'last_commit': {
            'id': '123abc',
            'short_id': '123abc',
            'created_at': '2021-07-20T21:50:48.000+02:00',
            'parent_ids': [],
            'title': 'init',
            'message': 'init\n',
            'author_name': 'User, Test',
            'author_email': 'test.user@example.com',
            'authored_date': '2021-07-20T21:50:48.000+02:00',
            'committer_name': 'User, Test',
            'committer_email': 'test.user@example.com',
            'committed_date': '2021-07-20T21:50:48.000+02:00',
            'web_url': 'https://gitlab.example.com/user_t/test_project/-/commit/123abc',
            'project_id': 123
        },
        'contributors': [
            {
                'name': 'User, Test',
                'email': 'test.user@example.com',
                'commits': 1,
                'additions': 0,
                'deletions': 0
            }
        ],
        'issues': [
            {
                'id': 1234,
                'iid': 16,
                'project_id': 1,
                'milestone': {
                    'id': 12,
                    'iid': 1,
                    'project_id': 1
                },
                'author': {
                    'id': 123,
                    'name': 'User, Test',
                    'username': 'user_t'
                },
                'assignees': [
                    {
                        'id': 123,
                        'name': 'User, Test',
                        'username': 'user_t'
                    }
                ]
            }
        ],
        'milestones': [
            {
                'id': 12,
                'iid': 1,
                'project_id': 1
            }
        ],
        'files': [
            {
                "id": "hash123",
                "name": "test.py",
                "type": "blob"
            }
        ]
    }
]}


class Config:

    def __init__(self):
        self.verbose = False
        self.neo4j_config = {"NEO4J": {"protocol": "bolt", "hostname": "localhost", "port": 7687, "user": "neo4j",
                                       "password": "corpus"}}


class Graph:

    def __init__(self, neo4j_url, user, password):
        self.neo4j_url = neo4j_url
        self.user = user
        self.password = password
        self.nodes = []

    def push(self, element):
        self.nodes.append(element)


class RelationMock:

    def __init__(self):
        self.related_to = []

    def update(self, element):
        self.related_to.append(element)


class LanguageRelationMock:

    def __init__(self):
        self.related_to = []

    def update(self, element1, element2):
        self.related_to.append([element1, element2])


class ProjectMock:

    def __init__(self):
        self.id = 1


class NamespaceMock:

    def __init__(self):
        self.id = 123
        self.belongs_to = RelationMock()


class OwnerMock:

    def __init__(self):
        self.id = 123
        self.owns = RelationMock()


class UserMock:

    def __init__(self):
        self.id = 123
        self.name = "User, Test"
        self.belongs_to = RelationMock()
        self.contributes_to = RelationMock()


class CommitMock:

    def __init__(self):
        self.id = "123abc"
        self.committer_name = "User, Test"
        self.belongs_to = RelationMock()
        self.committed_by = RelationMock()


class FileMock:

    def __init__(self):
        self.id = "hash123"
        self.belongs_to = RelationMock()


class LanguageMock:

    def __init__(self):
        self.name = "Python"
        self.value = 100.0
        self.is_contained_in = LanguageRelationMock()


class MilestoneMock:

    def __init__(self):
        self.id = 12
        self.belongs_to_project = RelationMock()


class IssueMock:

    def __init__(self):
        self.id = 1234
        self.author = "{'id': 123, 'name': 'User, Test', 'username': 'user_t'}"
        self.assignees = "[{'id': 123, 'name': 'User, Test', 'username': 'user_t'}]"
        self.milestone = "{'id': 12, 'iid': 1, 'project_id': 1}"
        self.authored_by = RelationMock()
        self.assigned_to = RelationMock()
        self.belongs_to_milestone = RelationMock()


def test_export_json():
    exporter = Exporter(Config(), corpus, "json")
    exporter.export("out/test.json")
    with open("out/test.json", "r") as f:
        data = f.read()

    exported_data = json.loads(data)
    assert exported_data == corpus.data


@patch('export.IssueModel')
@patch('export.MilestoneModel')
@patch('export.LanguageModel')
@patch('export.transform_language_dict')
@patch('export.FileModel')
@patch('export.CommitModel')
@patch('export.find_user_by_name')
@patch('export.UserModel')
@patch('export.NamespaceModel')
@patch('export.ProjectModel')
def test_export_neo4j(projectmodel_patch, namespacemodel_patch, usermodel_patch, find_user_by_name_patch,
                      commitmodel_patch, filemodel_patch, transform_language_dict_patch, languagemodel_patch,
                      milestonemodel_patch, issuemodel_patch):
    projectmodel_patch.create = mock.Mock(return_value=ProjectMock())
    namespacemodel_patch.create = mock.Mock(return_value=NamespaceMock())
    user = UserMock()
    usermodel_patch.create = mock.Mock(return_value=OwnerMock())
    usermodel_patch.get_or_create = mock.Mock(return_value=user)
    find_user_by_name_patch = mock.Mock(return_value=user)
    commitmodel_patch.get_or_create = mock.Mock(return_value=CommitMock())
    filemodel_patch.create = mock.Mock(return_value=FileMock())
    transform_language_dict_patch = mock.Mock(return_value=[{"name": "Python", "value": 100.0}])
    languagemodel_patch.get_or_create = mock.Mock(return_value=LanguageMock())
    milestone = MilestoneMock()
    milestonemodel_patch.create = mock.Mock(return_value=milestone)
    milestonemodel_patch.get = mock.Mock(return_value=milestone)
    issuemodel_patch.create = mock.Mock(return_value=IssueMock())

    exporter = Exporter(Config(), corpus, "neo4j")
    exporter.graph = mock.Mock(spec=Graph)
    exporter.export_to_neo4j()


def test_export_console(capfd):
    exporter = Exporter(Config(), corpus, "console")
    exporter.export()
    out, err = capfd.readouterr()
    assert "Error" not in out
