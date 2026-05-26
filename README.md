# istSOS4 SensorThingsAPI Workshop

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0)

Website: https://istsos.github.io/istsos4-workshop/

## Introduction

### Internet of Things (IoT)

The **Internet of Things (IoT)** refers to the network of physical devices, sensors, vehicles, appliances, and other objects embedded with electronics, software, and connectivity that enables them to collect and exchange data. IoT devices generate vast amounts of real-time measurements — from environmental monitoring stations tracking temperature, humidity and air quality, to smart city sensors measuring traffic flows and noise levels.

Managing, storing, and accessing this continuous stream of sensor observations requires a standardized, interoperable approach. This is where OGC SensorThings API comes in.

### OGC SensorThings API

The **OGC SensorThings API** is an open standard developed by the [Open Geospatial Consortium (OGC)](https://www.ogc.org/) that provides an open and unified way to connect IoT sensing devices, data, and applications over the web. It follows a RESTful approach and uses JSON/GeoJSON for data encoding, making it easy to integrate with modern web and cloud environments.

Key concepts in SensorThings API:
- **Thing**: A physical or virtual object in the real world (e.g., a weather station)
- **Location**: The geographic location of a Thing
- **Sensor**: An instrument that observes a property (e.g., a thermometer)
- **ObservedProperty**: The phenomenon being measured (e.g., air temperature)
- **Datastream**: A collection of observations from a Sensor on a Thing for a specific ObservedProperty
- **Observation**: A single measurement value at a given time

### istSOS4

**istSOS4** is an open-source implementation of the OGC SensorThings API developed at the [Institute of Earth Sciences (IST)](https://www.supsi.ch/ist) of SUPSI (University of Applied Sciences and Arts of Southern Switzerland). It is built with modern Python web technologies (FastAPI, SQLAlchemy, PostgreSQL/PostGIS) and provides:

- Full compliance with OGC SensorThings API Part 1: Sensing
- Support for historical and real-time sensor data
- Geospatial capabilities through PostGIS integration
- A RESTful JSON/GeoJSON API for IoT data management
- Scalable architecture suitable for production deployments

**Repository**: https://github.com/istSOS/istSOS4

## Workshop

See the workshop entry documentation for setup and content information.

## Installation

### Requirements

The workshop requires [Docker](https://docker.com)
and [Docker Compose](https://docs.docker.com/compose/) on your system.

### Running

```bash
cd workshop
# start workshop
./istsos4-workshop-ctl.sh start
# display URL and open in default web browser
./istsos4-workshop-ctl.sh url
# stop workshop
./istsos4-workshop-ctl.sh stop
```

### Znesical serve
```bash
cd web
# start znesical server
workon zensical
zensical serve
```
## License

This workshop material is released under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0) license.

See [LICENSE.md](LICENSE.md) for details.

## Bugs and Issues

All bugs, enhancements and issues are managed on [GitHub](https://github.com/istSOS/istsos4-workshop/issues).