#!/bin/bash
gunicorn --workers=1 --threads=2 --worker-class=gthread -b 0.0.0.0:33330 flask_premier:app