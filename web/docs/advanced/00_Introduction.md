# istSOS4 SensorThings API workshop overview

> **Workflow position:** start here.  
> This notebook introduces the concepts used by notebooks `01` to `04`.

The workshop follows one continuous path:

| Notebook | Focus | Main outcome |
|---|---|---|
| `00_Introduction.ipynb` | Concepts and workflow | Understand IoT, SensorThings API, istSOS4, and the run order |
| `01_Authorization.ipynb` | Authentication and authorization | Create and test `viewer` and `editor` users |
| `02_STA_Entities.ipynb` | Core SensorThings entities | Create a complete single-station SensorThings example |
| `03_STA_Observations.ipynb` | Bulk observations | Create a multi-datastream station and upload CSV observations |
| `04_Time_Travel.ipynb` | Reproducibility and lineage | Query current and historical states with time-travel parameters |

Run the notebooks in numerical order. Each notebook assumes the concepts, users, or data created in the previous steps.

## Internet of Things

The **Internet of Things (IoT)** is a network of physical or virtual objects that can collect, exchange, and expose data through digital services.

In environmental monitoring, typical IoT resources include:

- meteorological stations;
- river and lake monitoring stations;
- air-quality sensors;
- traffic and noise sensors;
- data loggers that periodically send measurements.

These systems produce continuous streams of observations. To make those observations reusable, queryable, and interoperable, the data model and the API need to be standardized.

## OGC SensorThings API

The **OGC SensorThings API** is a web standard from the Open Geospatial Consortium for publishing IoT observations and sensor metadata.

It uses a RESTful API style and JSON/GeoJSON payloads. This makes it practical for web applications, dashboards, data pipelines, and scientific workflows.

The core model used in this workshop is:

| Entity | Meaning | Workshop example |
|---|---|---|
| `Thing` | The physical or logical object being observed | A station or platform |
| `Location` | Where the `Thing` is located | A point geometry in `EPSG:2056` |
| `Sensor` | The device or method that produces measurements | Temperature, precipitation, or voltage sensor |
| `ObservedProperty` | The phenomenon being measured | Air temperature, relative humidity, voltage |
| `Datastream` | The link between `Thing`, `Sensor`, `ObservedProperty`, and unit | A time series for one measured variable |
| `Observation` | One measured value with time information | A single temperature or voltage value |
| `FeatureOfInterest` | The feature whose property is observed | Usually derived from the station location in this workshop |

## istSOS4

**istSOS4** is an open-source implementation of the OGC SensorThings API developed at the Institute of Earth Sciences of SUPSI.

In this workshop, istSOS4 is used as the backend service that stores users, policies, SensorThings entities, observations, and historical versions.

Main technical characteristics:

- Python web API based on FastAPI;
- relational storage through SQLAlchemy and PostgreSQL;
- geospatial support through PostGIS;
- JSON/GeoJSON REST interface;
- support for SensorThings API workflows and istSOS4 extensions such as Networks and time travel.

Repository: <https://github.com/istSOS/istSOS4>

## Workshop conventions

The notebooks use the following conventions:

| Convention | Value |
|---|---|
| API endpoint inside Docker/Jupyter | `http://api:5000/v4/v1.1` |
| Shared helper module | `istsos_utils.py` |
| Common network name | `DDT_workshop` |
| Resource-name prefix | `<editor_username>-` |
| CSV expected by notebook `03` | `data/observations.csv` |

The username prefix is important in a shared workshop environment: it reduces name collisions when several participants create resources on the same istSOS4 instance.

## Recommended run order

1. Start with `01_Authorization.ipynb` to create and test workshop users.
2. Continue with `02_STA_Entities.ipynb` to learn the SensorThings entity model step by step.
3. Run `03_STA_Observations.ipynb` to create a larger station and import observations from CSV.
4. Finish with `04_Time_Travel.ipynb` to inspect reproducibility, commits, and historical states.

> Keep `istsos_utils.py` in the same folder as the notebooks. Notebook imports expect it to be available as `from istsos_utils import ...`.

## License

This workshop material is licensed under the Creative Commons Attribution 4.0 International License.

Ready to start? Open `01_Authorization.ipynb`.
