# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

from utils.export_models import User as UserModel


def transform_language_dict(language_dict):
    language = dict()
    for name, value in language_dict.items():
        language["name"] = name
        language["value"] = value
        yield language


def find_user_by_name(graph, name):
    if name is None or "":
        return None
    node = graph.run("match (u:User) where u.name=$x return u", x=name).evaluate()
    if not node:
        try:
            forename = name.split()[0]
            surname = name.split()[-1]
            node = graph.run("match (u:User) where u.name=$x return u", x=surname + ", " + forename).evaluate()
        except IndexError:
            pass
    if node:
        return UserModel.wrap(node)
    return None
