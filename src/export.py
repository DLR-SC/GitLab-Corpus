# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import click
import json
from json.decoder import JSONDecodeError
from utils.export_models import Project as ProjectModel
from utils.export_models import Namespace as NamespaceModel
from utils.export_models import Language as LanguageModel
from utils.export_models import User as UserModel
from utils.export_models import File as FileModel
from utils.export_models import Commit as CommitModel
from py2neo import Graph, NodeMatcher
from utils.helpers import Corpus
from utils.export_helpers import transform_language_dict


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
                    click.echo("The input file does not contain valid JSON-data.")
        else:
            self.corpus = corpus

    def export(self, out):
        """This method exports the corpus to another format.
        :param out: Path to output file
        """
        with open(out, "w") as output:
            click.echo("Exporting...")
            if self.format.lower() == "json":
                if self.verbose:
                    click.echo("Output written to {}".format(out))
                json.dump(self.corpus.data, output, indent=4)
            elif self.format.lower() == "console":
                if self.verbose:
                    click.echo("Output will be printed to console.")
                for category in self.corpus.data:
                    for element in self.corpus.data[category]:
                        click.echo(str(element) + "\n")
            elif self.format.lower() == "neo4j":
                if self.verbose:
                    click.echo("Output will be exported to the Neo4J database.")
                self.graph = Graph(f"{self.neo4j_config['NEO4J']['protocol']}://"
                                   f"{self.neo4j_config['NEO4J']['hostname']}:"
                                   f"{self.neo4j_config['NEO4J']['port']}",
                                   user=self.neo4j_config['NEO4J']['user'],
                                   password=self.neo4j_config['NEO4J']['password'])
                self.matcher = NodeMatcher(self.graph)
                self.export_to_neo4j()

    def export_to_neo4j(self):
        for project in self.corpus.data["Projects"]:
            project_node = ProjectModel.create(self.graph, project)

            namespace_node = NamespaceModel.create(self.graph, project["namespace"])
            namespace_node.belongs_to.update(project_node)

            languages = transform_language_dict(project["languages"])

            try:
                owner_node = UserModel.create(self.graph, project["owner"])
                owner_node.owns.update(project_node)
                self.graph.push(owner_node)
            except KeyError:
                pass  # no owner found

            for user in project["users"]:
                user_node = UserModel.get_or_create(self.graph, user["id"], user)
                user_node.belongs_to.update(project_node)
                self.graph.push(user_node)

            for contributor in project["contributors"]:
                user_node = self._find_user_by_name(contributor["name"])
                if user_node is not None:
                    user_node.contributes_to.update(project_node)
                    self.graph.push(user_node)

            for commit in project["commits"]:
                commit_node = CommitModel.create(self.graph, commit)
                commit_node.belongs_to.update(project_node)
                user_node = self._find_user_by_name(commit["committer_name"])
                if user_node is not None:
                    commit_node.commited_by.update(user_node)
                self.graph.push(commit_node)

            for file in project["files"]:
                file_node = FileModel.create(self.graph, file)
                file_node.belongs_to.update(project_node)
                self.graph.push(file_node)

            for language in list(languages):
                language_node = LanguageModel.get_or_create(self.graph, language["name"], language)
                language_node.is_contained_in.update(project_node)
                self.graph.push(language_node)

            self.graph.push(namespace_node)

    def _find_user_by_name(self, name):
        if name is None:
            return None
        node = self.graph.run("match (u:User) where u.name=$x return u", x=name).evaluate()
        if not node:
            forename = name.split()[0]
            surname = name.split()[-1]
            node = self.graph.run("match (u:User) where u.name=$x return u", x=surname + ", " + forename).evaluate()
        if node:
            return UserModel.wrap(node)
        return None
