# Installation

# Prerequisites

- PostgreSQL 9.6+, uses the latest if possible. Official repositories for RH/Debian and Ubuntu availables: https://www.postgresql.org/download/
- postgresql-contrib 9.6+, same as above
- Elixir 1.5+, [install from here, Debian and Ubuntu ship older versions](https://elixir-lang.org/install.html#unix-and-unix-like) or uses [asdf](https://github.com/asdf-vm/asdf) under the pyairwaves user
- git
- libsqlite3-dev
- build-essentials

# PostgreSQL

Create an user and database.

Please makes sure your postgresql is in UTF8 ! In doubt uses `-E UTF8` when doing `createdb`.

# Install

    useradd -m -s /bin/bash pyairwaves
    sudo su - pyairwaves
    git clone https://github.com/rhaamo/pyAirwaves
    cd pyAirwaves/backend
    mix deps.get
    cp config/prod.secret.exs.sample config/prod.secret.exs
    $EDITOR config/prod.secret.exs
    mix compile
    
    # Edit frontend config to your needs
    $EDITOR ~/backend/priv/static/js/config.js
    
    # Setup database
    cd ~/backend/
    mix ecto.create
    mix ecto.migrate
    
    # Import datas in database
    mix pyairwaves.update_aircrafts
    mix pyairwaves.update_aircrafts_registrations
    mix pyairwaves.update_translations
    mix pyairwaves.update_aircrafts_mode_s
    mix pyairwaves.update_aircrafts_mode_sogn

    # Python part for the ingesters
    cd ~/
    python3 -m venv venv
    cd pyAirwaves
    $EDITOR config.py
    # don't forget to always enable the virtualenv
    source ~/venv/bin/activate
    pip install -r requirements.txt


# Automatic run

Look at the `installation/` folder, there is sample SystemD services for each part.

# CLI commands

See commands with:
```
cd ~/backend
mix pyairwaves
```

And extended help for a command with:
```
cd ~/backend
mix help pyairwaves.update_aircrafts
```

# Crontabs

- pyairwaves.update_aircrafts: one time per month
- pyairwaves.update_translations: one time per month
- pyairwaves.update_aircrafts_mode_s: one time per month
- pyairwaves.update_aircrafts_mode_sogn: one time per month
