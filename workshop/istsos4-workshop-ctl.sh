#!/bin/bash
# Control script for the istSOS4 workshop

WORKSHOP_DIR="$(cd "$(dirname "$0")" && pwd)"

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
        cd "$WORKSHOP_DIR" && $DOCKER_COMPOSE up -d
        echo "Workshop started. Run '$0 url' to get the Jupyter URL."
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
