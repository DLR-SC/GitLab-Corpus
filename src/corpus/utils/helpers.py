# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT

import configparser


class Corpus:
    """This helper class represents a corpus.
    
    Methods:
        __init__(self)


    """

    def __init__(self):
        """Corpus class constructor to initialize the object."""
        self.data = {"Projects": [],
                     }


def validate_neo4j_config(config):
    """

    :param config: 

    """
    if 'NEO4J' in config:
        return all(key in config['NEO4J'] for key in ['hostname', 'protocol', 'port', 'user', 'password'])


def load_neo4j_config(config_path):
    """

    :param config_path: 

    """
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        if validate_neo4j_config(config):
            return config
        else:
            print('Neo4j config is not valid.')
    except FileNotFoundError:
        print('No Neo4j config found.')


class Config:
    """This helper class stores configuration options centralized, because they are used in different locations.
    
    Methods:
        __init__(self)


    """

    def __init__(self):
        """Config class constructor to initialize the object."""
        self.gl = None
        self.verbose = False
        self.neo4j_config = None
