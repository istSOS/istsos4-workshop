"""Minimal helper functions for OGC SensorThings API / istSOS4 workshop."""
from __future__ import annotations
import requests
from typing import Any, Dict, Optional

BASE_URL = "http://127.0.0.1:8018/istsos4/v1.1"


def url(collection: str, entity_id: Optional[int] = None) -> str:
    collection = collection.strip("/")
    if entity_id is None:
        return f"{BASE_URL}/{collection}"
    return f"{BASE_URL}/{collection}({entity_id})"


def get_json(path: str, params: Optional[dict] = None) -> Any:
    r = requests.get(f"{BASE_URL}/{path.lstrip('/')}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def post_entity(collection: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    r = requests.post(url(collection), json=payload, timeout=30)
    r.raise_for_status()
    if r.content:
        return r.json()
    loc = r.headers.get("Location", "")
    return {"Location": loc}


def post_observation(datastream_id: int, phenomenon_time: str, result: Any, parameters: Optional[dict] = None) -> Dict[str, Any]:
    payload = {
        "phenomenonTime": phenomenon_time,
        "result": result,
        "Datastream": {"@iot.id": datastream_id},
    }
    if parameters:
        payload["parameters"] = parameters
    return post_entity("Observations", payload)
