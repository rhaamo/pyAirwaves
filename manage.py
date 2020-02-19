#!/usr/bin/env python
""" Module for managing tasks through a simple cli interface. """
# Libraries
from manager import Manager

from server import create_app
from server.config import LISTEN_HOST, LISTEN_PORT

# Constants.
manager = Manager()

# TODO use click


@manager.command
def runserver():
    """ Starts server on port 8000. """
    app = create_app()
    app.run(host=LISTEN_HOST, port=LISTEN_PORT)


if __name__ == "__main__":
    manager.main()
