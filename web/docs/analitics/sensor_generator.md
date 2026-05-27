---
title: Virtual Sensor Generator
description: A reusable generator of synthetic sensor data for testing quality control procedures and alarm systems in smart monitoring systems.
icon: lucide/monitor-speaker
---

## Virtual Sensor Generator
For testing or demonstration purposes, it can be useful to have a generator of synthetic sensor data that simulates realistic features such as random noise, slow drift, and periods of anomalous values. This allows us to test quality control procedures or rise alarm without relying on real sensor data.

The file [sensor_stream_generators.py](https://raw.githubusercontent.com/istSOS/istsos4-workshop/refs/heads/main/workshop/jupyter/content/notebooks/scripts/sensor_stream_generators.py) contains a reusable generator of synthetic sensor data. 

This generator simulates a multi-parameter sensor stream, producing one row of data at each call to the `read()` method. The generated data includes realistic features such as random noise, slow drift, and periods of anomalous values that can be used to test quality control procedures or rise alarm.

You can instantiate one of the predefined cases by name:

```python
from scripts.sensor_stream_generators import RealTimeSensorGenerator

generator = RealTimeSensorGenerator("river_level")
```

You can also define one custom case using the same structure as the predefined `CASE_PARAMETERS` entries:

```python
my_case_parameters = {
    "temperature_c": {
        "base": 20.0,
        "noise": 0.2,
        "drift": 0.01,
        "statistical": (15.0, 25.0),
        "plausible": (-10.0, 45.0),
        "alarm_direction": "high",
        "alarm_target": 50.0,
    }
}

generator = RealTimeSensorGenerator(
    case_name="custom_case",
    case_parameters=my_case_parameters,
    step_seconds=30,  # real waiting time between two generated rows. Use 30 for the workshop.
    alarm_after_seconds=600,  # Number of seconds from the start before the first alarm begins.
    alarm_duration_seconds=180,  # Duration of each alarm event.
    alarm_repeat_seconds=900,  # If None, the alarm happens only once. If set to a number, a new alarm starts every alarm_repeat_seconds
    suspect_probability=0.1,  # Probability of a slight statistical anomaly during normal periods.
    seed=None  # Optional seed for reproducible simulations.
)
```

Parameter meanings:

| Parameter | Meaning |
|---|---|
| `base` | Initial normal value and baseline used by the synthetic signal. |
| `noise` | Standard deviation of the random measurement noise added at each step. |
| `drift` | Linear baseline change added at each generated step to simulate slow sensor or environmental drift. |
| `statistical` | Expected normal range. Values outside this range but inside `plausible` can be treated as suspicious. |
| `plausible` | Physically plausible range. Values outside this range can be treated as alarms. |
| `alarm_direction` | Direction used during alarm periods: `high`, `low`, or `high_abs` for absolute positive/negative excursions. |
| `alarm_target` | Optional target value generated during alarm periods. If omitted, the alarm is generated outside the plausible range. |

Once the generator is instantiated, you can call `read()` to get a new synthetic observation at each step. The `status()` method provides information about the current state of the generator, such as whether it is in a normal, suspicious, or alarm period. Additionally, you can use the `sleep=Falase` option in `read()` to generate data without waiting for the real time step, which can be useful for testing or batch generation:

Reading one observation with real-time waiting:

```python
for _ in range(10):
    observation = generator.read()
    print(f"{observation} - {generator.status()}")
```

Reading one observation without waiting:

```python
for _ in range(10):
    observation = generator.read(sleep=False)
    print(f"{observation} - {generator.status()}")
```