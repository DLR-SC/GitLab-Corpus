# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import sys
import click
import json
import logging
from json.decoder import JSONDecodeError
from utils.export_models import Project as ProjectModel, NeoGraphObjectException
from utils.export_models import Namespace as NamespaceModel
from utils.export_models import Language as LanguageModel
from utils.export_models import User as UserModel
from utils.export_models import File as FileModel
from utils.export_models import Commit as CommitModel
from utils.export_models import Milestone as MilestoneModel
from utils.export_models import Issue as IssueModel
from py2neo import Graph, NodeMatcher
from utils.helpers import Corpus
from utils.export_helpers import transform_language_dict, find_user_by_name

logging.basicConfig(filename="corpus.log", filemode="w")
log = logging.getLogger(__name__)
log.addHandler((logging.StreamHandler(sys.stdout)))


class Exporter:
    """This class provides a method to export a corpus in another format.

    Methods:
        __init__(self, verbose, corpus, format_str, from_file=False, file="-")
        export(self, out)
    """

    def __init__(self, config, corpus, format_str, from_file=False, file="-"):
        """Exporter class constructor to initialize the object.
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
                    # click.echo("The input file does not contain valid JSON-data.")
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
                    # click.echo("Output written to {}".format(out))
                json.dump(self.corpus.data, output, indent=4)
        elif self.format.lower() == "console":
            if self.verbose:
                log.info("Output will be printed to console.")
                # click.echo("Output will be printed to console.")
            for category in self.corpus.data:
                for element in self.corpus.data[category]:
                    click.echo(str(element) + "\n")
        elif self.format.lower() == "neo4j":
            if self.verbose:
                log.info("Output will be exported to the Neo4J database.")
                # click.echo("Output will be exported to the Neo4J database.")
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

                try:
                    project_node = ProjectModel.create(self.graph, project)
                except NeoGraphObjectException:
                    log.error("A project could not be exported. The ID is missing.")

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
                    author_name = eval(issue_node.author)["name"]
                    if author_name is not None:
                        user_node = find_user_by_name(self.graph, author_name)
                        issue_node.authored_by.update(user_node)
                    for assignee in eval(issue_node.assignees):
                        user_node = find_user_by_name(self.graph, assignee["name"])
                        issue_node.assigned_to.update(user_node)
                    if issue_node.milestone is not None:
                        milestone = eval(issue_node.milestone)
                        milestone_node = MilestoneModel.get(self.graph, {"id": milestone["id"]})
                        if milestone_node is not None:
                            issue_node.belongs_to_milestone.update(milestone_node)
                    self.graph.push(issue_node)

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
