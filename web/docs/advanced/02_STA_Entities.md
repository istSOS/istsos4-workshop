# Register core SensorThings API entities

> **Workflow position:** after `01_Authorization.ipynb`.  
> This notebook introduces the SensorThings data model by creating one complete station workflow step by step.

The goal is to build a small but complete SensorThings example:

1. create a `Network`;
2. create a monitored object, called a `Thing`;
3. assign a `Location` to the `Thing`;
4. define the measured property with an `ObservedProperty`;
5. define the measuring instrument with a `Sensor`;
6. connect everything through a `Datastream`;
7. send one or more `Observations`.

## Entity model used here

| Entity | Meaning | Example in this notebook | Why it matters |
|---|---|---|---|
| `Network` | A group of related stations or datastreams | `DDT_workshop` | Organizes data by project or campaign |
| `Thing` | The object being monitored | Fiume Ticino Valle station | Central object that observations belong to |
| `Location` | Where the `Thing` is located | Swiss coordinate point | Places the station spatially |
| `ObservedProperty` | What is measured | Water voltage | Defines the observed phenomenon |
| `Sensor` | Device or method used to measure | `Ecolog 1000` | Describes how values are produced |
| `Datastream` | Time-series container for one measured property | Voltage datastream | Connects Thing, Sensor, ObservedProperty, and unit |
| `Observation` | One measured value | `3.63` | Stores the actual data |
| `FeatureOfInterest` | Feature observed by the observation | Usually inferred from the Thing location | Explains what the observation refers to |

> This notebook assumes that an `editor` user and policy were created in notebook `01`.

### :lucide-play: Setup

Import the helper functions and define the base URL of the istSOS4 API.

When the notebook runs inside the Jupyter Docker container, the API is reachable through:

```python
IST_SOS_ENDPOINT = "http://api:5000/v4/v1.1"
```


```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from istsos_utils import (
    REQUEST_TIMEOUT,
    auth_headers,
    display_error_response,
    get_or_create_network,
    login,
    print_created,
)

rome_tz = ZoneInfo("Europe/Rome")

IST_SOS_ENDPOINT = "http://api:5000/v4/v1.1"
```

### :lucide-play: Login as administrator

In this notebook, the administrator is used only to create or retrieve the workshop `Network`.

All SensorThings entities are created later with the `editor` user.


```python
admin_username = input("Enter administrator username: ")
admin_password = input("Enter administrator password: ")

if not admin_username or not admin_password:
    print("Username or password is empty")
else:
    admin_token, login_body = login(
        IST_SOS_ENDPOINT,
        admin_username,
        admin_password,
        timeout=REQUEST_TIMEOUT,
    )

    if admin_token:
        print(f"Logged in as {admin_username}")
```

### :lucide-play: Create or retrieve a `Network`

A `Network` groups related datastreams, stations, or monitoring resources.

The helper function `get_or_create_network()` first searches for `DDT_workshop`. If it already exists, its identifier is reused; otherwise, a new network is created.

> This step requires the Network extension to be enabled in the istSOS4 deployment.


```python
network_name = "DDT_workshop"

network_id = get_or_create_network(
    IST_SOS_ENDPOINT,
    admin_token,
    network_name,
    timeout=REQUEST_TIMEOUT,
)

print(f"Network ID: {network_id}")
```

### :lucide-play: Login as editor

From now on, requests use the `editor` user created in notebook `01`.

The editor username is used as a prefix for resource names. This reduces collisions when several workshop participants run the notebooks on the same API instance.


```python
editor_username = input("Enter editor username: ")
editor_password = input("Enter editor password: ")

if not editor_username or not editor_password:
    print("Username or password is empty")
else:
    editor_token, login_body = login(
        IST_SOS_ENDPOINT,
        editor_username,
        editor_password,
        timeout=REQUEST_TIMEOUT,
    )

    if editor_token:
        prefix = editor_username + "-"
        print(f"Logged in as {editor_username}")
        print("Resource names will be prefixed with: " + prefix)
```

### :lucide-play: Create a `Thing`

A `Thing` represents the object being monitored.

Here, the `Thing` is a river monitoring station. Its identifier is saved as `thing_id` and reused when creating the location and datastream.


```python
thing_body = {
    "name": f"{prefix}FIU_VAL",
    "description": "Water level, water temperature and water electrical conductivity recorder on the Ticino river",
    "properties": {
        "keywords": "water, river, height, temperature, conductivity, ACSOT",
        "description": "River level, water temperature and water electrical conductivity at Fiume Ticino Valle",
    },
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Things",
    json=thing_body,
    headers=auth_headers(editor_token, "Create new thing"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    thing_id = print_created("Thing", response)
else:
    display_error_response(response)
```

### :lucide-play: Create a `Location`

A `Location` describes where the `Thing` is placed.

The payload uses a GeoJSON point with Swiss coordinates in `EPSG:2056` and links the location to the `Thing` created in the previous step.


```python
location_body = {
    "name": f"{prefix}Fiume Ticino Valle",
    "description": "Location of the river monitoring station",
    "encodingType": "application/vnd.geo+json",
    "location": {
        "type": "Point",
        "coordinates": [
            2717185.973,
            1114552.035,
        ],
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:2056",
            },
        },
    },
    "Things": [
        {"@iot.id": thing_id},
    ],
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Locations",
    json=location_body,
    headers=auth_headers(editor_token, "Create new location"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    location_id = print_created("Location", response)
else:
    display_error_response(response)
```

### :lucide-play: Create an `ObservedProperty`

An `ObservedProperty` defines what is being measured.

In this example, the datastream will represent voltage measurements, so the observed property describes water voltage.


```python
observed_property_body = {
    "name": f"{prefix}ground:water:voltage",
    "description": "Ground water voltage",
    "properties": {},
    "definition": "{}",
}

response = requests.post(
    IST_SOS_ENDPOINT + "/ObservedProperties",
    json=observed_property_body,
    headers=auth_headers(editor_token, "Create new ObservedProperty"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    observed_property_id = print_created("ObservedProperty", response)
else:
    display_error_response(response)
```

### :lucide-play: Create a `Sensor`

A `Sensor` describes the device, instrument, or method used to produce measurements.

The created `sensor_id` is later referenced by the datastream.


```python
sensor_body = {
    "name": f"{prefix}Ecolog 1000",
    "description": "Pressure, temperature and electrical conductivity sensor",
    "properties": {},
    "encodingType": "application/json",
    "metadata": '{"brand": "OTT", "type": "Pressure, temperature, electrical conductivity sensor"}',
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Sensors",
    json=sensor_body,
    headers=auth_headers(editor_token, "Create new Sensor"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    sensor_id = print_created("Sensor", response)
else:
    display_error_response(response)
```

### :lucide-play: Create a `Datastream`

A `Datastream` connects the key SensorThings entities:

- `Thing`: where the measurement belongs;
- `Sensor`: how the measurement is produced;
- `ObservedProperty`: what is measured;
- unit of measurement;
- optional `Network`: how the datastream is organized.

Once the datastream exists, observations can be posted to it.


```python
datastream_body = {
    "name": f"{prefix}V_FIU_VAL",
    "description": "Voltage datastream for the Fiume Ticino Valle station",
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
    "unitOfMeasurement": {
        "name": "Voltage",
        "symbol": "V",
        "definition": "",
    },
    "properties": {
        "samplingFrequency": "PT60M",
        "acquisitionFrequency": "PT60M",
    },
    "Thing": {"@iot.id": thing_id},
    "Sensor": {"@iot.id": sensor_id},
    "ObservedProperty": {"@iot.id": observed_property_id},
    "Network": {"@iot.id": network_id},
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Datastreams",
    json=datastream_body,
    headers=auth_headers(editor_token, "Create new Datastream"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    datastream_id = print_created("Datastream", response)
else:
    display_error_response(response)
```

### :lucide-play: Create one `Observation`

An `Observation` is a measured value.


```python
phenomenon_time = (
    datetime.now(rome_tz)
    - timedelta(days=1)
).replace(
    hour=10,
    minute=0,
    second=0,
    microsecond=0,
)

observation_body = {
    "result": 3.63,
    "phenomenonTime": phenomenon_time.isoformat(),
    "Datastream": {"@iot.id": datastream_id},
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Observations",
    json=observation_body,
    headers=auth_headers(editor_token, "Create new Observation"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    observation_id = print_created("Observation", response)
else:
    display_error_response(response)
```

### :lucide-play: Create a `Datastream` with nested `Observations`

SensorThings API also allows related entities to be created together in one request.

Here, a second datastream is created and three observations are embedded directly in the datastream payload. This pattern is useful for small imports where the related entities are known in advance.


```python
datastream_with_observations_body = {
    "name": f"{prefix}RSSI_FIU_VAL",
    "description": "RSSI datastream for the Fiume Ticino Valle station",
    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
    "unitOfMeasurement": {
        "name": "",
        "symbol": "RSSI",
        "definition": "",
    },
    "properties": {
        "samplingFrequency": "PT60M",
        "acquisitionFrequency": "PT60M",
    },
    "ObservedProperty": {"@iot.id": observed_property_id},
    "Sensor": {"@iot.id": sensor_id},
    "Thing": {"@iot.id": thing_id},
    "Network": {"@iot.id": network_id},
    "Observations": [
        {
            "result": result,
            "phenomenonTime": (
                phenomenon_time + timedelta(minutes=10 * index)
            ).isoformat(),
        }
        for index, result in enumerate([1, 2, 3])
    ],
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Datastreams",
    json=datastream_with_observations_body,
    headers=auth_headers(editor_token, "Create Datastream and related Observations"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    second_datastream_id = print_created("Datastream", response)
else:
    display_error_response(response)
```
