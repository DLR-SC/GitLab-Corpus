# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

def transform_language_dict(language_dict):
    language = dict()
    for name, value in language_dict.items():
        language["name"] = name
        language["value"] = value
        yield language
