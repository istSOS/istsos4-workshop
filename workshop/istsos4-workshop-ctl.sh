#!/bin/bash
# Control script for the istSOS4 workshop

SCRIPT_PATH="${BASH_SOURCE[0]}"
WORKSHOP_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

# This script is intended to be executed, not sourced.
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
    echo "ERROR: Do not source this script. Run it as: ./istsos4-workshop-ctl.sh <command>"
    return 1 2>/dev/null || exit 1
fi

usage() {
    echo "Usage: $0 {start|stop|url|update|clean}"
    echo ""
    echo "Commands:"
    echo "  start   - Start the workshop services"
    echo "  stop    - Stop the workshop services"
    echo "  url     - Display the Jupyter notebook URL"
    echo "  update  - Update workshop Docker images"
    echo "  clean   - Clean up dangling Docker images/containers"
    exit 1
}

# Determine docker compose command
if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
elif docker-compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
else
    echo "ERROR: Docker Compose not found. Please install Docker Compose."
    exit 1
fi

case "$1" in
    start)
        echo "Starting istSOS4 workshop..."
        if cd "$WORKSHOP_DIR" && $DOCKER_COMPOSE up -d; then
            echo "Workshop started. Run '$0 url' to get the Jupyter URL."
        else
            echo "ERROR: Failed to start workshop services."
            exit 1
        fi
        ;;
    stop)
        echo "Stopping istSOS4 workshop..."
        cd "$WORKSHOP_DIR" && $DOCKER_COMPOSE down
        ;;
    url)
        TOKEN=$(docker logs istsos4-workshop-jupyter 2>&1 | grep -oP '(?<=token=)[a-zA-Z0-9]+' | tail -1)
        if [ -n "$TOKEN" ]; then
            echo "Jupyter URL: http://localhost:8888/?token=$TOKEN"
        else
            echo "Jupyter URL: http://localhost:8888"
        fi
        ;;
    update)
        echo "Updating workshop Docker images..."
        cd "$WORKSHOP_DIR" && $DOCKER_COMPOSE pull
        ;;
    clean)
        echo "Cleaning dangling Docker images..."
        docker image prune -f
        ;;
    *)
        usage
        ;;
esac
