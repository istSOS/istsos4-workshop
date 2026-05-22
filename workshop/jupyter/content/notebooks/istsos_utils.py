"""
Utility functions for the istSOS4 SensorThings API workshop notebooks.

Keep this file in the same directory as the notebooks so that:

    from istsos_utils import ...

works directly from Jupyter.
"""

import json
import re

import requests
from IPython.display import Markdown, display

REQUEST_TIMEOUT = 10


def display_json(data):
    """Display a Python object as formatted JSON in a notebook."""
    display(Markdown(f"```json\n{json.dumps(data, indent=2)}\n```"))


def display_error_response(response):
    """Display an API error response in a readable way."""
    try:
        result = response.json()
        display_json(result)
    except Exception:
        display(Markdown(f"```text\n{response.text}\n```"))


def get_iot_id_from_location(location_header):
    """Extract the numeric @iot.id from a SensorThings Location header."""
    match = re.search(r"\((\d+)\)", location_header or "")
    if not match:
        raise ValueError(
            f"Could not extract @iot.id from Location header: {location_header}"
        )
    return int(match.group(1))


def auth_headers(token, commit_message=None, content_type=None, accept=None):
    """Build the headers used by authenticated API requests."""
    headers = {
        "Authorization": f"Bearer {token}",
    }

    if commit_message:
        headers["Commit-message"] = commit_message

    if content_type:
        headers["Content-type"] = content_type

    if accept:
        headers["Accept"] = accept

    return headers


def print_created(entity_name, response):
    """Print a creation message and return the created @iot.id."""
    location = response.headers.get("location", "")
    print(f"{entity_name} created successfully ({location})")
    return get_iot_id_from_location(location)


def login(server_url, username, password, timeout=REQUEST_TIMEOUT):
    """Login and return (token, response_body). Return (None, None) on failure."""
    data = {
        "username": username,
        "password": password,
        "grant_type": "password",
    }

    response = requests.post(
        f"{server_url}/Login",
        data=data,
        timeout=timeout,
    )

    if response.status_code != 200:
        display_error_response(response)
        return None, None

    body = response.json()
    return body["access_token"], body


def get_or_create_network(
    server_url,
    token,
    network_name,
    timeout=REQUEST_TIMEOUT,
):
    """Return the @iot.id of an existing Network, or create it if missing."""
    response = requests.get(
        f"{server_url}/Networks",
        headers=auth_headers(token),
        params={
            "$filter": f"name eq '{network_name}'",
            "$select": "id",
        },
        timeout=timeout,
    )

    if response.status_code != 200:
        display_error_response(response)
        raise Exception("Failed to search Network")

    values = response.json().get("value", [])
    if values:
        network_id = values[0]["@iot.id"]
        print(f"Network already exists: {network_name} ({network_id})")
        return network_id

    network_body = {
        "name": network_name,
    }

    response = requests.post(
        f"{server_url}/Networks",
        json=network_body,
        headers=auth_headers(token, "Create new network"),
        timeout=timeout,
    )

    if response.status_code == 201:
        return print_created("Network", response)

    display_error_response(response)
    raise Exception("Failed to create Network")


def get_datastreams_for_thing(
    server_url,
    token,
    thing_id,
    timeout=REQUEST_TIMEOUT,
):
    """Return all Datastreams linked to a Thing."""
    response = requests.get(
        f"{server_url}/Things({thing_id})/Datastreams",
        headers=auth_headers(token, accept="application/json"),
        timeout=timeout,
    )

    if response.status_code != 200:
        display_error_response(response)
        raise Exception("Failed to retrieve Datastreams from Thing")

    return response.json().get("value", [])


def build_column_to_datastream_id(body, created_datastreams):
    """Build a CSV column -> Datastream @iot.id mapping.

    The CSV column names come from:
        body["Datastreams"][...]["properties"]["column"]

    The IDs come from the Datastreams returned by the API.
    """
    datastream_name_to_id = {
        datastream["name"]: datastream["@iot.id"]
        for datastream in created_datastreams
    }

    column_to_datastream_name = {
        datastream["properties"]["column"]: datastream["name"]
        for datastream in body["Datastreams"]
    }

    column_to_datastream_id = {}

    for column_name, datastream_name in column_to_datastream_name.items():
        if datastream_name not in datastream_name_to_id:
            raise Exception(
                f"Datastream not found on server: {datastream_name}"
            )

        column_to_datastream_id[column_name] = datastream_name_to_id[
            datastream_name
        ]

    return column_to_datastream_id


def normalize_time_column(df, time_column):
    """Convert a dataframe time column to timezone-aware UTC datetimes."""
    import pandas as pd

    if time_column not in df.columns:
        raise Exception(f"Missing required time column: {time_column}")

    df[time_column] = pd.to_datetime(
        df[time_column],
        utc=True,
        errors="coerce",
    )

    return df


def read_observations_csv(csv_path, time_column, required_value_columns=None):
    """Read and validate an observations CSV file."""
    import pandas as pd

    df = pd.read_csv(csv_path, sep=None, engine="python")

    if time_column not in df.columns:
        raise Exception(f"Missing required time column: {time_column}")

    if required_value_columns:
        missing_value_columns = [
            column_name
            for column_name in required_value_columns
            if column_name not in df.columns
        ]

        if missing_value_columns:
            raise Exception(
                f"Missing CSV value columns: {missing_value_columns}"
            )

    df = normalize_time_column(df, time_column)

    return df


def result_to_float(value):
    """Convert API or CSV numeric values to float, supporting comma decimals."""
    if value is None:
        return None

    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return None


def build_bulk_observations(df, time_column, column_to_datastream_id):
    """Build a /BulkObservations payload from a dataframe."""
    import pandas as pd

    observations = []

    for column_name, datastream_id in column_to_datastream_id.items():
        if column_name not in df.columns:
            raise Exception(f"Missing CSV column: {column_name}")

        values = pd.to_numeric(
            df[column_name].astype(str).str.replace(",", ".", regex=False),
            errors="coerce",
        )

        invalid_values = values.isna().sum()
        print(f"{column_name}: invalid numeric values = {invalid_values}")

        data_array = []

        for index, row in df.iterrows():
            phenomenon_time = row[time_column]
            result = values.iloc[index]

            if pd.isna(phenomenon_time) or pd.isna(result):
                continue

            phenomenon_time_iso = phenomenon_time.isoformat().replace(
                "+00:00", "Z"
            )

            data_array.append(
                [
                    float(result),
                    phenomenon_time_iso,
                    phenomenon_time_iso,
                    None,
                ]
            )

        observations.append(
            {
                "Datastream": {
                    "@iot.id": datastream_id,
                },
                "components": [
                    "result",
                    "phenomenonTime",
                    "resultTime",
                    "resultQuality",
                ],
                "dataArray": data_array,
            }
        )

    return observations


def preview_bulk_observations(observations, rows=3):
    """Return a compact preview of a BulkObservations payload."""
    preview = []

    for observation_group in observations:
        preview.append(
            {
                "Datastream": observation_group["Datastream"],
                "components": observation_group["components"],
                "dataArray_preview": observation_group["dataArray"][:rows],
                "total_rows": len(observation_group["dataArray"]),
            }
        )

    return preview


def post_bulk_observations(
    server_url,
    token,
    observations,
    commit_message="Create observations",
    timeout=60,
):
    """Post a BulkObservations payload and return the response."""
    response = requests.post(
        f"{server_url}/BulkObservations",
        headers=auth_headers(
            token,
            commit_message=commit_message,
            content_type="application/json",
        ),
        data=json.dumps(observations),
        timeout=timeout,
    )

    if response.status_code not in (200, 201):
        display_error_response(response)
        raise Exception("BulkObservations request failed")

    print("Bulk observations created successfully")
    return response


def get_observations(
    server_url,
    token,
    datastream_id,
    top=100,
    orderby="phenomenonTime desc",
    timeout=30,
):
    """Fetch observations for one Datastream."""

    url = (
        f"{server_url}/Datastreams({datastream_id})/Observations"
        f"?$orderby={orderby.replace(' ', '%20')}"
        f"&$top={top}"
    )

    response = requests.get(
        url,
        headers=auth_headers(token, accept="application/json"),
        timeout=timeout,
    )

    if response.status_code != 200:
        print(response.url)
        display_error_response(response)
        raise Exception("Failed to fetch observations")

    return response.json().get("value", [])
