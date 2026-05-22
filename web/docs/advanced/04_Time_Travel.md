# Time travel, commits, and data lineage

> **Workflow position:** after `03_STA_Observations.ipynb`.  
> This notebook updates an existing `Observation` and then queries its current and historical states.

The istSOS4 time-travel extension supports reproducibility and data lineage. It makes it possible to ask:

- what does this resource look like now?
- what did this resource look like at a previous time?
- which commit explains the change?

## Time-travel parameters

| Parameter | Type | Purpose |
|---|---|---|
| `$as_of` | ISO 8601 date-time | Return the resource as it was at a specific instant |
| `$from_to` | ISO 8601 interval | Return historical states over a time interval |

## Commit entity

A `Commit` records metadata about a change.

| Property | Type | Meaning |
|---|---|---|
| `author` | string | User or authority responsible for the change |
| `encodingType` | string | Encoding type of the commit message |
| `message` | string | Explanation of the transaction |
| `date` | ISO 8601 date-time | Time when the commit was created |

## Persistent reference pattern

A reproducible request can be identified by combining:

```text
<service-url>/<version>/<request-path>?<query>&$as_of=<date-time>
```

This notebook demonstrates that pattern on an `Observation`.

> In a shared workshop instance, run this notebook immediately after notebook `03` or manually set `observation_id` to an observation you created.

### :lucide-play: Setup

Import the required libraries, define the API endpoint, and define a small helper for UTC timestamps.

When the notebook runs inside the Jupyter Docker container, the API is reachable through:

```python
IST_SOS_ENDPOINT = "http://api:5000/v4/v1.1"
```


```python
from datetime import datetime, timedelta, timezone

import requests

from istsos_utils import (
    REQUEST_TIMEOUT,
    auth_headers,
    display_error_response,
    display_json,
    login,
)

IST_SOS_ENDPOINT = "http://api:5000/v4/v1.1"


def utc_now_iso(offset_seconds=0):
    """Return the current UTC time as an ISO 8601 string accepted by the API."""
    value = datetime.now(timezone.utc) + timedelta(seconds=offset_seconds)
    value = value.replace(microsecond=0)
    return value.isoformat().replace("+00:00", "Z")
```

### :lucide-play: Login as editor

Use the same `editor` account used in notebooks `02` and `03`.

The editor is needed because this notebook modifies an existing observation before querying its history.


```python
editor_username = input("Enter your username: ")
editor_password = input("Enter your password: ")

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
        print("Your station name is prefixed with: " + prefix)
```

### :lucide-play: Retrieve the latest `Observation`

To avoid hard-coding an observation ID, the notebook retrieves the most recent observation from the server.

The returned `@iot.id` is stored in `observation_id` and reused in the following requests.

> In a multi-user workshop, this may return another participant's latest observation. Replace `observation_id` manually if needed.


```python
response = requests.get(
    f"{IST_SOS_ENDPOINT}/Observations?$orderby=phenomenonTime desc&$top=1",
    headers=auth_headers(editor_token, accept="application/json"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 200:
    observations = response.json().get("value", [])

    if not observations:
        raise Exception(
            "No Observations found. Run notebook 03_STA_Observation first."
        )

    latest_observation = observations[0]
    observation_id = latest_observation["@iot.id"]

    display_json(latest_observation)
else:
    display_error_response(response)
```

### :lucide-play: Update the `Observation`

Before applying the update, the notebook stores a timestamp just before the change.

That timestamp is later used with `$as_of` to retrieve the previous state.

The update changes:

- `result`;
- `resultQuality`.

The `Commit-message` header explains why the resource changed.


```python
datetime_before_update = utc_now_iso(offset_seconds=-1)

body = {
    "result": 10,
    "resultQuality": "100",
}

response = requests.patch(
    f"{IST_SOS_ENDPOINT}/Observations({observation_id})",
    json=body,
    headers=auth_headers(
        editor_token,
        commit_message="Corrected result and result quality",
        content_type="application/json",
    ),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code in (200, 204):
    print("Observation updated successfully")
    print(f"Timestamp before update: {datetime_before_update}")
else:
    display_error_response(response)
```

### :lucide-play: Retrieve the current state

This request retrieves the current version of the updated observation.

The `$expand=Commit` option includes the commit metadata associated with the current state.


```python
response = requests.get(
    f"{IST_SOS_ENDPOINT}/Observations({observation_id})",
    headers=auth_headers(editor_token, accept="application/json"),
    params={
        "$expand": "Commit",
    },
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 200:
    display_json(response.json())
else:
    display_error_response(response)
```

### :lucide-play: Retrieve the previous state with `$as_of`

The `$as_of` query parameter evaluates the request as if it had been executed at a specific time.

Here, the timestamp captured before the update should return the observation state before the correction.


```python
response = requests.get(
    f"{IST_SOS_ENDPOINT}/Observations({observation_id})",
    headers=auth_headers(editor_token, accept="application/json"),
    params={
        "$expand": "Commit",
        "$as_of": datetime_before_update,
    },
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 200:
    display_json(response.json())
else:
    display_error_response(response)
```

### :lucide-play: Retrieve historical states with `$from_to`

The `$from_to` query parameter retrieves all historical states over a time interval.

The interval starts just before the update and ends just after it, so the response should include the state transition caused by the correction.


```python
datetime_after_update = utc_now_iso(offset_seconds=1)
time_interval = f"{datetime_before_update}/{datetime_after_update}"

print(f"Requested interval: {time_interval}")

response = requests.get(
    f"{IST_SOS_ENDPOINT}/Observations({observation_id})",
    headers=auth_headers(editor_token, accept="application/json"),
    params={
        "$expand": "Commit",
        "$from_to": time_interval,
    },
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 200:
    display_json(response.json())
else:
    display_error_response(response)
```
