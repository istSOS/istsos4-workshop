---
tiutle: Workshop Installation
description: Instructions for installing the workshop content and dependencies
icon: lucide/box
---

# Workshop installation

!!! note "Installation Requirements"
    The workshop requires [Docker](https://docker.com) and
    [Docker Compose](https://docs.docker.com/compose/) to be installed on your system. More information on installing Docker can be found [here](./docker.md).
    A basic understanding of Python programming is recommended but not required, as the workshop includes step-by-step instructions and explanations.

## Installation

Download and run the workshop content:

```console
curl -O https://codeload.github.com/istSOS/istsos4-workshop/zip/main
unzip main
cd istsos4-workshop-main/workshop
```

### Linux / macOS

```console
# start the workshop
./istsos4-workshop-ctl.sh start

# display URL and open in default web browser
./istsos4-workshop-ctl.sh url

# stop workshop
./istsos4-workshop-ctl.sh stop
```
### Windows (Powershell or Command Prompt):

```console
# start the workshop
.\win-istsos4-workshop-ctl.bat start

# display URL and open in default web browser
.\win-istsos4-workshop-ctl.bat url

# stop workshop
.\win-istsos4-workshop-ctl.bat stop
```

If the above `.sh` script does not work on your system 
you can execute `docker-compose` directly via:

```console
# in dir istsos4-workshop-main/workshop
docker-compose up -d

docker logs --follow istsos4-workshop-jupyter
# look for URL+Token and Copy/Paste in browser
```

Below are utility commands. Use when stopped to clean and update.
```console
# update the workshop Docker Images in case of new versions
./istsos4-workshop-ctl.sh update

# clean your Docker environment from dangling Images/Containers
# (does not remove the workshop's images, only obsolete ones)
./istsos4-workshop-ctl.sh clean
```


## Installation Issues

Docker installed but problems installing/running the workshop? Below some tips:

### Download Problems

Although `curl` may be on your system it may have problems with SSL (one user noted using OSGeo4W).
In that case you can add the `--insecure` commandline option or copy/paste the download URL in your browser and download from there.

### File/Drive Sharing

The workshop setup involves Docker Volume Mounting.
For Mac OS and Windows installs be sure to **enable File/Drive Sharing** within Docker Desktop for the directory where you unzipped the workshop.
Go to the `Preferences/Settings | File Sharing...`  menu and make settings accordingly.

### Running Docker with privileged user in Linux

Currently, the workshop doesn't support a docker installation that needs the `sudo` command to run Docker. The following [post-installation step](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) in the Docker documentation must be performed before running our script to start the workshop.

### Cannot Access URL

The workshop should run on `http://127.0.0.1:8888?token=<token>` but in some cases this may not work.
In that case you could also try `http://0.0.0.0:8888?token=<token>`.

## No Docker Installed?

If you somehow were not able to install Docker:
there is a Cloud version of the Jupyter-Notebook-part of the workshop via "Jupyter Binder".

With some limits (e.g. no local geo-services, no data publication), you can follow most of the workshop using a remote Docker instance within your browser via "Jupyter Binder". Click on the button below
to launch the Workshop Binder Instance. Startup takes a while, be patient...

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/istsos/istsos4-workshop/master?filepath=workshop%2Fjupyter%2Fcontent%2Fnotebooks%2F01-introduction.ipynb)

Additional notes for Binder session:

* session timeout is about 10 minutes, if that happens, refreshing the page will not help, you need to start a new session using the button above

<!-- ## Support

A [Gitter](https://gitter.im/istsos/istsos4-workshop) channel exists for
discussion and live support from the developers of the workshop. -->

### Bugs and Issues

All bugs, enhancements and issues can be reported on [GitHub](https://github.com/geopython/geopython-workshop/issues).