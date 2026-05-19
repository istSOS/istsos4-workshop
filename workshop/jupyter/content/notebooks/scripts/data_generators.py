from __future__ import annotations
from datetime import datetime, timezone, timedelta
import math, random


def temperature_stream(n=30, interval_seconds=1):
    base = datetime.now(timezone.utc)
    for i in range(n):
        t = base + timedelta(seconds=i * interval_seconds)
        value = 20 + 2 * math.sin(i / 10) + random.gauss(0, 0.2)
        yield {"phenomenonTime": t.isoformat().replace("+00:00", "Z"), "result": round(value, 3)}


def acceleration_stream(n=200, frequency_hz=50):
    base = datetime.now(timezone.utc)
    dt = 1 / frequency_hz
    for i in range(n):
        t = base + timedelta(seconds=i * dt)
        yield {
            "phenomenonTime": t.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "result": {
                "ax": round(random.gauss(0, 0.03), 4),
                "ay": round(random.gauss(0, 0.03), 4),
                "az": round(9.81 + random.gauss(0, 0.04), 4),
            },
        }
