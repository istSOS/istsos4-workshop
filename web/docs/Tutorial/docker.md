# Docker Installation

The workshop requires [Docker](https://docker.com) and
[Docker Compose](https://docs.docker.com/compose/) to be installed on your system.

## Installing Docker

### Linux

Follow the official [Docker Engine installation guide for Linux](https://docs.docker.com/engine/install/).

After installation, ensure Docker is managed by a non-root user:

```console
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

### macOS

Download and install [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/).

### Windows

Download and install [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/).

## Verifying your installation

```console
docker version

docker compose version
```

Both commands should return version information without errors.

## File Sharing (macOS / Windows)

The workshop uses Docker Volume Mounting. On macOS and Windows, ensure that
**File/Drive Sharing** is enabled in Docker Desktop settings for the directory
where you unpacked the workshop.

Go to `Settings | Resources | File Sharing` and add the workshop directory.
