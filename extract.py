# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

def get_category(manager_string):
    """This helper method extracts the category"""
    start_index = -1
    for i in range(0, 3):
        start_index = manager_string.find(".", start_index + 1)
    end_index = manager_string.find("Manager")
    return manager_string[start_index + 1:end_index] + "s"


class Extractor:
    """This class represents the extraction module."""

    extracted_corpus = {"Projects": [],  # This object represents the output corpus and will exist only once
                        }  # https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables

    def __init__(self, gitlab_manager):
        self.gl = gitlab_manager
        self.managers = [self.gl.projects]

    def extract(self, all_elements):
        for manager in self.managers:
            objects = manager.list(all=all_elements)
            category = get_category(str(manager))
            for obj in objects:
                self.extracted_corpus[category].append(obj.attributes)
