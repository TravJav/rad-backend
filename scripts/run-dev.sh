#!/bin/bash

poetry config virtualenvs.create false
poetry install

export FLASK_APP=radpair.src.health.api:app
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run --debugger -h 0.0.0.0 -p 5000 --reload
