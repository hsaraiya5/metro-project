#!/bin/sh
pip install virtualenv
virtualenv venv 
source venv/bin/activate

pip install -r requirements.txt
export METRO_API_KEY=cac6f061c28b46268eec2c9e40885508

gunicorn --bind localhost:5000 src.wsgi:app