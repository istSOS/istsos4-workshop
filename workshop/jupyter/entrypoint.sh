#!/bin/bash
# Entrypoint for the istSOS4 workshop Jupyter container
#
# WARNING: Authentication is disabled for ease of local workshop use.
# Do NOT expose this container to untrusted networks or the public internet.

exec jupyter notebook --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password=''
