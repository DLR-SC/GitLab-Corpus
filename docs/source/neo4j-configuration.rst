.. _how-to-write-the-neo4j-config:

=====================================
How to write the Neo4J configuration
=====================================

The configuration file always start with the following line: ``[NEO4J]``.

After that, the file looks like this::

    hostname = somehostname
    protocol = http(s)/bolt
    port = 9999
    user = username_for_your_db
    password = pw_for_that_user

* hostname: Hostname of your Neo4J-server (e.g. localhost or some remote hostname)
* protocol: One of http, https or bolt
* port: 7474 is default for http(s), 7687 is default for bolt. You can put a custom port here, but make sure your database is reachable through that port
* user: username to access the db
* password: password for the specified user