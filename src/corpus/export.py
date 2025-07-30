# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import sys
import time
import click
import json
import logging
from json.decoder import JSONDecodeError
from corpus.utils.export_models import Project as ProjectModel, NeoGraphObjectException
from corpus.utils.export_models import Namespace as NamespaceModel
from corpus.utils.export_models import Language as LanguageModel
from corpus.utils.export_models import User as UserModel
from corpus.utils.export_models import File as FileModel
from corpus.utils.export_models import Commit as CommitModel
from corpus.utils.export_models import Milestone as MilestoneModel
from corpus.utils.export_models import Issue as IssueModel
from corpus.utils.export_models import Mergerequest as MergerequestModel
from corpus.utils.export_models import Release as ReleaseModel
from py2neo import Graph, NodeMatcher
from corpus.utils.helpers import Corpus
from corpus.utils.export_helpers import transform_language_dict, find_user_by_name

"""
.. module:: export
.. moduleauthor:: Emanuel Caricato <emanuel.caricato@dlr.de>
"""
try:
    logging.basicConfig(filename="out/corpus.log", filemode="w")
    log = logging.getLogger(__name__)
    log.addHandler((logging.StreamHandler(sys.stdout)))
except:
    pass


class Exporter:
    """This class provides a method to export a corpus in another format.

    Methods:
        __init__(self, verbose, corpus, format_str, from_file=False, file="-")
        export(self, out)
    """

    def __init__(self, config, corpus, format_str, from_file=False, file="-"):
        """
        Exporter class constructor to initialize the object.

        :param config: Configuration for neo4j and verbose mode
        :param corpus: Input corpus, which will be exported
        :param from_file: Specifies, if the input corpus should be read from a file [default: ``False``]
        :param file: Path to input corpus

        """
        self.verbose = config.verbose
        self.format = format_str
        self.corpus = Corpus()
        self.graph = None
        self.matcher = None
        self.neo4j_config = config.neo4j_config
        if from_file:
            with open(file, 'r') as f:
                try:
                    self.corpus.data = json.load(f)
                except JSONDecodeError:
                    log.critical("The input file does not contain valid JSON-data.")
        else:
            self.corpus = corpus

    def export(self, out="-"):
        """This method exports the corpus to another format.

        :param out: Path to output file

        """

        click.echo("Exporting...")
        if self.format.lower() == "json":
            with open(out, "w") as output:
                if self.verbose:
                    log.info("Output written to {}".format(out))
                json.dump(self.corpus.data, output, indent=4)
        elif self.format.lower() == "console":
            if self.verbose:
                log.info("Output will be printed to console.")
            for category in self.corpus.data:
                for element in self.corpus.data[category]:
                    click.echo(str(element) + "\n")
        elif self.format.lower() == "neo4j":
            if self.verbose:
                log.info("Output will be exported to the Neo4J database.")
            self.graph = Graph(f"{self.neo4j_config['NEO4J']['protocol']}://"
                               f"{self.neo4j_config['NEO4J']['hostname']}:"
                               f"{self.neo4j_config['NEO4J']['port']}",
                               user=self.neo4j_config['NEO4J']['user'],
                               password=self.neo4j_config['NEO4J']['password'])
            self.matcher = NodeMatcher(self.graph)
            self.export_to_neo4j()

    def export_to_neo4j(self):
        """This method exports the corpus to a neo4j database as specified in the configuration file."""
        with click.progressbar(self.corpus.data["Projects"]) as bar:
            for project in bar:
                self.export_project(project)

    def export_category(self, category_model, category, project, get_or_create=False, pk=""):
        try:
            if isinstance(project[category], list):
                for element in project[category]:
                    try:
                        if get_or_create:
                            element_node = category_model.get_or_create(self.graph, element[pk], element)
                        else:
                            element_node = category_model.create(self.graph, element)
                        yield element_node
                    except NeoGraphObjectException:
                        log.error("An element for category {} in project {} could not be exported. "
                                  "The ID is missing.".format(category, project["id"]))
            else:
                try:
                    yield category_model.create(self.graph, project[category])
                except NeoGraphObjectException:
                    log.error("An element of category {} in project {} could not be exported. "
                              "The ID is missing.".format(category, project["id"]))
        except KeyError:
            log.info("No elements for category '{}' found in project {}.".format(category, project["id"]))

    def export_project(self, project):
        try:
            project_node = ProjectModel.create(self.graph, project)
        except NeoGraphObjectException:
            log.error("A project could not be exported. The ID is missing.")
            return

        for namespace_node in self.export_category(NamespaceModel, "namespace", project):
            namespace_node.belongs_to.update(project_node)
            self.graph.push(namespace_node)

        for owner_node in self.export_category(UserModel, "owner", project):
            owner_node.owns.update(project_node)
            self.graph.push(owner_node)

        for user_node in self.export_category(UserModel, "users", project, True, "id"):
            user_node.belongs_to.update(project_node)
            self.graph.push(user_node)

        try:
            for contributor in project["contributors"]:
                user_node = find_user_by_name(self.graph, contributor["name"])
                if user_node is not None:
                    user_node.contributes_to.update(project_node)
                    self.graph.push(user_node)
        except KeyError:
            log.info("No contributor found for project {}.".format(project["id"]))

        for commit_node in self.export_category(CommitModel, "commits", project, True, "id"):
            commit_node.belongs_to.update(project_node)
            user_node = find_user_by_name(self.graph, commit_node.committer_name)
            if user_node is not None:
                commit_node.committed_by.update(user_node)
            self.graph.push(commit_node)

        for file_node in self.export_category(FileModel, "files", project):
            file_node.belongs_to.update(project_node)
            self.graph.push(file_node)

        for language in transform_language_dict(project["languages"]):
            try:
                language_node = LanguageModel.get_or_create(self.graph, language["name"], language)
                language_node.is_contained_in.update(project_node, {'value': language['value']})
                self.graph.push(language_node)
            except NeoGraphObjectException:
                log.error("A language for project {} could not be exported. "
                          "The ID is missing.".format(project["id"]))

        for milestone_node in self.export_category(MilestoneModel, "milestones", project):
            milestone_node.belongs_to_project.update(project_node)
            self.graph.push(milestone_node)

        for issue_node in self.export_category(IssueModel, "issues", project):
            self.update_attribute(issue_node.author, issue_node.authored_by, by_id=False)
            self.update_attribute(issue_node.assignees, issue_node.assigned_to, by_id=False)
            self.update_attribute(issue_node.milestone, issue_node.belongs_to_milestone, model=MilestoneModel)
            self.graph.push(issue_node)

        for mergerequest_node in self.export_category(MergerequestModel, "mergerequests", project):
            self.update_attribute(mergerequest_node.author, mergerequest_node.authored_by, model=UserModel)
            self.update_attribute(mergerequest_node.merged_by, mergerequest_node.is_merged_by, model=UserModel)
            self.update_attribute(mergerequest_node.closed_by, mergerequest_node.is_closed_by, model=UserModel)
            self.update_attribute(mergerequest_node.assignees, mergerequest_node.assigned_to, model=UserModel)
            self.update_attribute(mergerequest_node.commits, mergerequest_node.has_commit, model=CommitModel)
            self.update_attribute(mergerequest_node.close_issues, mergerequest_node.closes, model=IssueModel)
            self.graph.push(mergerequest_node)

        for release_node in self.export_category(ReleaseModel, "releases", project):
            self.update_attribute(release_node.author, release_node.authored_by, model=UserModel)
            self.update_attribute(release_node.commit, release_node.committed_through, model=CommitModel)
            self.update_attribute(release_node.milestones, release_node.belongs_to, model=MilestoneModel)
            self.graph.push(release_node)

    def update_attribute(self, src_attribute, node_attribute, model=None, by_id=True):
        if by_id:
            if src_attribute:
                src_dict = eval(src_attribute)
                if isinstance(src_dict, list):
                    for element in src_dict:
                        node = model.get(self.graph, {"id": element["id"]})
                        if node:
                            node_attribute.update(node)
                else:
                    node = model.get(self.graph, {"id": src_dict["id"]})
                    if node:
                        node_attribute.update(node)
        else:
            if src_attribute:
                src_dict = eval(src_attribute)
                if isinstance(src_dict, list):
                    for element in src_dict:
                        node = find_user_by_name(self.graph, element["name"])
                        if node:
                            node_attribute.update(node)
                else:
                    node = find_user_by_name(self.graph, src_dict["name"])
                    if node:
                        node_attribute.update(node)
