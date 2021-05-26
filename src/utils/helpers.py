# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

class Corpus:
    """This helper class represents a corpus.

    Methods:
        __init__(self)
    """
    def __init__(self):
        """Corpus class constructor to initialize the object."""
        self.data = {"Projects": [],
                     }


class Config:
    """This helper class stores configuration options centralized, because they are used in different locations.

    Methods:
        __init__(self)
    """
    def __init__(self):
        """Config class constructor to initialize the object."""
        self.gl = None
        self.verbose = False
