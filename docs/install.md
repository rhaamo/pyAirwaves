# Installation

# Prerequirements

    sudo apt install build-essential libcurl4-openssl-dev libssl-dev libncursesw5-dev libsqlite3-dev libbz2-dev zlib1g-dev
    sudo useradd -m -s /bin/bash pyairwaves
    sudo su - pyairwaves
    # Install pyenv [https://github.com/pyenv/pyenv]
    curl https://pyenv.run | bash
    # add things in bashrc as asked by installer
    cd ~
    git clone https://github.com/rhaamo/pyAirwaves
    # Install required python version
    pyenv install `cat pyAirwaves/.python-version`

# PostgreSQL

Create an user and database.

# Install

    sudo su - pyairwaves
    cd pyAirwaves
    pip install -r requirements.txt
    # copy sample config and edit to your needs
    cp config.py.sample config.py
    $EDITOR config.py
    
    # Edit frontend config to your needs
    $EDITOR static/js/config.js
    
    # Setup database
    flask db upgrade
    
    # Import datas in database (offline ones)
    flask import-aircrafts
    flask import-registrations
    
    # Import more datas (online)
    flask update-db

# Automatic run

Look at the `installation/` folder, there is sample SystemD services for each part.
