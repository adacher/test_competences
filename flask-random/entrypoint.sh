#!/bin/bash
gunicorn --workers=1 --threads=2 --worker-class=gthread -b 0.0.0.0:44440 flask_random:app