from py2neo import Graph
from py2neo.ogm import GraphObject, RelatedObjects, Property, RelatedFrom, RelatedTo


class NeoGraphObjectException(Exception):
    pass


class NeoGraphObject(GraphObject):
    __unique_constraints__ = []

    def __init__(self):
        super().__init__()
        self.__unique_constraints__ = NeoGraphObject.__unique_constraints__

    @classmethod
    def find(cls, matcher, **kwargs):
        """
        Matches the first label by a given keyword arguments
        """
        obj = matcher.match(**kwargs).first()
        return obj

    @classmethod
    def create(cls, graph: Graph, attributes: dict = None):
        """
        Create a label from given attributes.\
        At least the the __primarykey__ must available in the attributes dictionary.
        :param graph: The graph instance
        :type graph: Graph
        :param attributes: Attributes
        :type attributes: dict
        :return: The created label
        :rtype: NeoGraphObject
        """
        obj = cls()
        if cls.__primarykey__ not in attributes:
            raise NeoGraphObjectException(f"Primary '{obj.__primarykey__}' not in attributes")
        for attr, attr_value in attributes.items():
            if hasattr(obj, attr) and not isinstance(getattr(obj, attr), RelatedObjects):
                if not isinstance(attr_value, dict) and not isinstance(attr_value, list):
                    setattr(obj, attr, attr_value)
                else:
                    setattr(obj, attr, str(attr_value))
        graph.create(obj)
        return obj

    @classmethod
    def get(cls, graph: Graph, filters: dict):
        """
        Matches a labels from cls and reduces the result by the given filters.
        :param graph:
        :type graph:
        :param filters: A dictionary with filters as defined in the py2neo documentation
        :type filters: dict
        :return: The label with type of class
        :rtype: NeoGraphObject
        """
        obj = cls.match(graph)
        for attr, attr_value in filters.items():
            obj = obj.where(**{attr: attr_value})
        obj = obj.first()
        return obj

    @classmethod
    def get_or_create(cls, graph: Graph, pk=None, attributes: dict = None):
        """
        Serves as helper method to retrieve labels from the graph or create a new one if no label existed
        :param graph: Graph instance
        :type graph: Graph
        :param pk: The labels primary key
        :param attributes: Additional attributes used when a new label is created
        :type attributes: dict
        :return: The newly created label or an existing one.
        :rtype: NeoGraphObject
        """
        if pk is None:
            raise NeoGraphObjectException(f"Primary key missing")
        obj = cls.get(graph, filters={cls.__primarykey__: pk})
        if not obj:
            if attributes is not None:
                attributes = {cls.__primarykey__: pk, **attributes}
            else:
                attributes = {cls.__primarykey__: pk}
            obj = cls.create(graph, attributes)
        return obj

    @classmethod
    def set_constraints(cls, graph: Graph):
        """
        Sets all unique constraints defined in current class
        :param graph: The graph instance
        :type graph: Graph
        """
        for key in cls.__unique_constraints__:
            graph.schema.create_uniqueness_constraint(str(cls.__name__), key)


class Project(NeoGraphObject):
    __primarylabel__ = "Project"
    __primarykey__ = "id"

    __unique_constraints__ = [
        "id",
    ]

    id = Property("id")
    description = Property("description")
    name = Property("name")
    name_with_namespace = Property("name_with_namespace")
    path = Property("path")
    path_with_namespace = Property("path_with_namespace")
    created_at = Property("created_at")
    default_branch = Property("default_branch")
    tag_list = Property("tag_list")
    ssh_url_to_repo = Property("ssh_url_to_repo")
    http_url_to_repo = Property("http_url_to_repo")
    web_url = Property("web_url")
    readme_url = Property("readme_url")
    avatar_url = Property("avatar_url")
    forks_count = Property("forks_count")
    star_count = Property("star_count")
    last_activity_at = Property("last_activity_at")
    _links = Property("_links")
    packages_enabled = Property("packages_enabled")
    empty_repo = Property("empty_repo")
    archived = Property("archived")
    visibility = Property("visibility")
    owner = Property("owner")
    resolve_outdated_diff_discussions = Property("resolve_outdated_diff_discussions")
    container_registry_enabled = Property("container_registry_enabled")
    container_expiration_policy = Property("container_expiration_policy")
    issues_enabled = Property("issues_enabled")
    merge_requests_enabled = Property("merge_requests_enabled")
    wiki_enabled = Property("wiki_enabled")
    jobs_enabled = Property("jobs_enabled")
    snippets_enabled = Property("snippets_enabled")
    service_desk_enabled = Property("service_desk_enabled")
    service_desk_address = Property("service_desk_address")
    can_create_merge_request_in = Property("can_create_merge_request_in")
    issues_access_level = Property("issues_access_level")
    repository_access_level = Property("repository_access_level")
    merge_requests_access_level = Property("merge_requests_access_level")
    forking_access_level = Property("forking_access_level")
    wiki_access_level = Property("wiki_access_level")
    builds_access_level = Property("builds_access_level")
    snippets_access_level = Property("snippets_access_level")
    pages_access_level = Property("pages_access_level")
    operations_access_level = Property("operations_access_level")
    analytics_access_level = Property("analytics_access_level")
    emails_disabled = Property("emails_disabled")
    shared_runners_enabled = Property("shared_runners_enabled")
    lfs_enabled = Property("lfs_enabled")
    creator_id = Property("creator_id")
    import_status = Property("import_status")
    open_issues_count = Property("open_issues_count")
    ci_default_git_depth = Property("ci_default_git_depth")
    ci_forward_deployment_enabled = Property("ci_forward_deployment_enabled")
    public_jobs = Property("public_jobs")
    build_timeout = Property("build_timeout")
    auto_cancel_pending_pipelines = Property("auto_cancel_pending_pipelines")
    build_coverage_regex = Property("build_coverage_regex")
    ci_config_path = Property("ci_config_path")
    shared_with_groups = Property("shared_with_groups")
    only_allow_merge_if_pipeline_succeeds = Property("only_allow_merge_if_pipeline_succeeds")
    allow_merge_on_skipped_pipeline = Property("allow_merge_on_skipped_pipeline")
    restrict_user_defined_variables = Property("restrict_user_defined_variables")
    request_access_enabled = Property("request_access_enabled")
    only_allow_merge_if_all_discussions_are_resolved = Property("only_allow_merge_if_all_discussions_are_resolved")
    remove_source_branch_after_merge = Property("remove_source_branch_after_merge")
    printing_merge_request_link_enabled = Property("printing_merge_request_link_enabled")
    merge_method = Property("merge_method")
    suggestion_commit_message = Property("suggestion_commit_message")
    auto_devops_enabled = Property("auto_devops_enabled")
    auto_devops_deploy_strategy = Property("auto_devops_deploy_strategy")
    autoclose_referenced_issues = Property("autoclose_referenced_issues")
    approvals_before_merge = Property("approvals_before_merge")
    mirror = Property("mirror")
    requirements_enabled = Property("requirements_enabled")
    security_and_compliance_enabled = Property("security_and_compliance_enabled")
    compliance_frameworks = Property("compliance_frameworks")
    issues_template = Property("issues_template")
    merge_requests_template = Property("merge_requests_template")
    permissions = Property("permissions")
    issue_statistics = Property("issue_statistics")
    languages = Property("languages")
    first_commit = Property("first_commit")
    last_commit = Property("last_commit")
    contributors = Property("contributors")
    external_contributors = Property("external_contributors")

    owned_by = RelatedFrom("User", "OWNED_BY")
    has_contributor = RelatedFrom("User", "CONTRIBUTED_BY")
    has_user = RelatedFrom("User", "HAS_USER")
    has_language = RelatedFrom("Language", "HAS_LANGUAGE")
    has_namespace = RelatedFrom("Namespace", "HAS_NAMESPACE")
    has_file = RelatedFrom("File", "BELONGS_TO")
    has_commit = RelatedFrom("Commit", "BELONGS_TO")
    has_milestone = RelatedFrom("Milestone", "BELONGS_TO")
    has_issue = RelatedFrom("Issue", "BELONGS_TO")
    has_member = RelatedFrom("User", "BELONGS_TO")
    has_merge = RelatedFrom("MergeRequest", "BELONGS_TO")
    has_note = RelatedFrom("Note", "BELONGS_TO")


class Namespace(NeoGraphObject):
    __primarylabel__ = "Namespace"
    __primarykey__ = "id"

    __unique_constraints__ = [
        "id",
    ]

    id = Property("id")
    name = Property("name")
    path = Property("path")
    kind = Property("kind")
    full_path = Property("full_path")
    parent_id = Property("parent_id")
    avatar_url = Property("avatar_url")
    web_url = Property("web_url")

    belongs_to = RelatedTo(Project)
    

class User(NeoGraphObject):
    __primarylabel__ = "User"
    __primarykey__ = "id"

    __unique_constraints__ = [
        "id",
        "username"
    ]

    id = Property("id")
    username = Property("username")
    name = Property("name")
    state = Property("state")
    avatar_url = Property("avatar_url")
    web_url = Property("web_url")

    belongs_to = RelatedTo(Project)
    owns = RelatedTo(Project)
    contributes_to = RelatedTo(Project)
    is_author = RelatedFrom("Issue", "AUTHORED_BY")
    assigned_to = RelatedFrom("Issue", "ASSIGNED_TO")
    committer = RelatedFrom("Commit", "COMMITTED_BY")


class Language(NeoGraphObject):
    __primarylabel__ = "Language"
    __primarykey__ = "name"

    __unique_constraints__ = [
        "name"
    ]

    name = Property("name")

    is_contained_in = RelatedTo(Project)


class Milestone(NeoGraphObject):
    __primarylabel__ = "Milestone"
    __primarykey__ = "id"

    __unique_constraints__ = [
        "id",
        "iid"
    ]

    id = Property("id")
    iid = Property("iid")
    project_id = Property("project_id")
    title = Property("title")
    description = Property("description")
    state = Property("state")
    created_at = Property("created_at")
    updated_at = Property("updated_at")
    due_date = Property("due_date")
    start_date = Property("start_date")
    expired = Property("expired")
    web_url = Property("web_url")

    belongs_to = RelatedFrom("Issue", "BELONGS_TO")


class Issue(NeoGraphObject):
    __primarylabel__ = "Issue"
    __primarykey__ = "id"

    __unique_constraints__ = [
        "id",
        "iid"
    ]

    id = Property("id")
    iid = Property("iid")
    project_id = Property("project_id")
    title = Property("title")
    description = Property("description")
    state = Property("state")
    created_at = Property("created_at")
    updated_at = Property("updated_at")
    closed_at = Property("closed_at")
    closed_by = Property("closed_by")
    labels = Property("labels")
    user_notes_count = Property("user_notes_count")
    merge_requests_count = Property("merge_requests_count")
    upvotes = Property("upvotes")
    downvotes = Property("downvotes")
    due_date = Property("due_date")
    confidential = Property("confidential")
    discussion_locked = Property("discussion_locked")
    web_url = Property("web_url")
    time_stats = Property("time_stats")
    task_completion_status = Property("task_completion_status")
    weight = Property("weight")
    blocking_issues_count = Property("blocking_issues_count")
    has_tasks = Property("has_tasks")
    _links = Property("_links")
    references = Property("references")
    moved_to_id = Property("moved_to_id")
    service_desk_reply_to = Property("service_desk_reply_to")

    belongs_to_milestone = RelatedTo(Milestone)
    authored_by = RelatedTo(User)
    assigned_to = RelatedTo(User)


class File(NeoGraphObject):
    __primarylabel__ = "File"
    __primarykey__ = "id"

    __unique_constraints__ = [
        "id"
    ]

    id = Property("id")
    name = Property("name")
    file_type = Property("type")
    path = Property("path")
    mode = Property("mode")

    belongs_to = RelatedTo(Project)


class Commit(NeoGraphObject):
    __primarylabel__ = "Commit"
    __primarykey__ = "id"
    
    __unique_constraints__ = [
        "id",
        "short_id"
    ]

    id = Property("id")
    short_id = Property("short_id")
    created_at = Property("created_at")
    parent_ids = Property("parent_ids")
    title = Property("title")
    message = Property("message")
    author_name = Property("author_name")
    author_email = Property("author_email")
    authored_date = Property("authored_date")
    committer_name = Property("committer_name")
    committer_email = Property("committer_email")
    committed_date = Property("committed_date")
    web_url = Property("web_url")
    project_id = Property("project_id")

    belongs_to = RelatedTo(Project)
    commited_by = RelatedTo(User)
