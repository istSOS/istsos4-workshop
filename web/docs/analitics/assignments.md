---
title: Assignments
description: Explore practical exercises and assignments to apply the concepts of data quality control and analytics in smart monitoring systems.
icon: lucide/briefcase-business
---

# Assignments
This section contains exercises and assignments related to the concepts covered in the workshop. These assignments are designed to reinforce your understanding of the material and provide hands-on experience with the tools and techniques discussed.

Design and register a SensorThings/istSOS4 monitoring setup for this cases. 
Then run the real-time generator and send the simulated observations to the correct Datastreams.

Each generated row has this form:

```python
[phenomenonTime, value_1, value_2, value_3]
```

The generator does **not** assign quality flags. Each value starts as raw data (`0`) and your code must classify it using the thresholds below.

| Quality Code | Meaning | Rule |
|---:|---|---|
| 0 | raw | value not yet checked |
| 1 | sensible | value inside statistical thresholds |
| 2 | suspect | value outside statistical thresholds but still inside plausibility thresholds |
| 3 | alarm | value outside plausibility thresholds |
| -999 | invalid | Observation with value out of physical limits |

The logical steps are:

1. Create a Thing and a Sensor for each case.
2. Create a Datastream for each parameter, with the correct unit of measurement and observed property.
3. Run the generator and send the generated observations to the correct Datastreams with the quality flags assigned based on the thresholds provided in the case descriptions.
4. Create a dashboard or visualization to monitor the incoming data and quality flags in real time.
5. Set up alerts or notifications for when alarm conditions are detected.


## Case 1 - River level monitoring

You have been hired by a regional civil protection unit to monitor the Maggia River at Bignasco, in Valle Maggia. The objective is to provide an early indication of potentially dangerous hydrological conditions near the village and downstream communities. The station is installed on a bridge or riverbank section and simulates a compact hydrometric node combining an ultrasonic water-level sensor, a water temperature probe and an optical turbidity probe.

**Location:** Bignasco, Valle Maggia, Canton Ticino, Switzerland  
**Thing to register in istSOS4:** `Hydrometric station MAG-BIG-01`  
**Sensor:** Ultrasonic river gauge with water temperature and optical turbidity probes

| Parameter | Meaning | Unit | Physical limit | Plausibility threshold | Statistical threshold |
|---|---|---:|---:|---:|---:|
| `water_level_m` | River stage relative to a local staff gauge datum | m | 0 – 6 | 0.05 – 4.5 | 0.2 – 2.2 |
| `water_temperature_c` | Water temperature | °C | -5 – 35 | 0 – 28 | 4 – 18 |
| `turbidity_ntu` | Optical turbidity | NTU | 0 – 1000 | 0 – 600 | 0 – 80 |

See [Notebook River level](https://raw.githubusercontent.com/istSOS/istsos4-workshop/refs/heads/main/workshop/jupyter/content/notebooks/assignment_01_river_level_monitoring.ipynb)

## Case 2 - Slope stability monitoring

You have been hired by a municipality in Vallemaggia to monitor a potentially unstable slope above a mountain road near Cevio. The objective is to detect acceleration of ground movement and changes in water-related soil conditions that could precede shallow landslides or rockfall-prone instability. The monitoring node is installed on a protected pole anchored near the road cut and combines a tilt unit with soil moisture and pore pressure probes.

**Location:** Road slope above Cevio, Vallemaggia, Canton Ticino, Switzerland  
**Thing to register in istSOS4:** `Slope monitoring station CEV-SLOPE-01`  
**Sensor:** Low-cost GNSS/tiltmeter node with soil moisture and pore pressure probes

| Parameter | Meaning | Unit | Physical limit | Plausibility threshold | Statistical threshold |
|---|---|---:|---:|---:|---:|
| `tilt_deg` | Slope inclination change from reference orientation | degree | -15 – 15 | -8 – 8 | -1.5 – 1.5 |
| `soil_moisture_pct` | Volumetric soil water content | % | -10 – 120 | 0 – 100 | 15 – 55 |
| `pore_pressure_kpa` | Pore water pressure | kPa | -20 – 120 | -5 – 80 | 0 – 25 |

See [Slope Stability notebook](https://raw.githubusercontent.com/istSOS/istsos4-workshop/refs/heads/main/workshop/jupyter/content/notebooks/assignment_02_slope_stability_monitoring.ipynb)


## Case 3 - Bridge structural monitoring

You have been hired to monitor the pedestrian suspension bridge Ponte Tibetano Carasc, between Monte Carasso and Sementina. The objective is to identify abnormal vibration and deformation patterns that may occur during strong wind or unusual dynamic loading. The node is fixed near the bridge deck and simulates a structural health monitoring device combining an accelerometer, a deck displacement sensor and a temperature probe.

**Location:** Ponte Tibetano Carasc, Monte Carasso–Sementina, Canton Ticino, Switzerland  
**Thing to register in istSOS4:** `Bridge structural node CARASC-BRG-01`  
**Sensor:** Structural health monitoring node with accelerometer, displacement sensor and cable temperature probe

| Parameter | Meaning | Unit | Physical limit | Plausibility threshold | Statistical threshold |
|---|---|---:|---:|---:|---:|
| `vertical_acceleration_g` | Vertical dynamic acceleration of the deck | g | -3 – 3 | -1.5 – 1.5 | -0.25 – 0.25 |
| `deck_displacement_mm` | Deck displacement relative to a local reference | mm | -120 – 120 | -80 – 80 | -15 – 15 |
| `cable_temperature_c` | Cable or deck temperature | °C | -40 – 90 | -25 – 65 | -5 – 35 |

See [Bridge Structural notebook](https://raw.githubusercontent.com/istSOS/istsos4-workshop/refs/heads/main/workshop/jupyter/content/notebooks/assignment_03_bridge_structural_monitoring.ipynb)

## Case 4 — Urban rainfall monitoring

You have been hired by the city technical office to monitor intense urban rainfall in Lugano, close to the Cassarate catchment and a dense urban drainage area. The objective is to support early warning for pluvial flooding and sewer overload. The node is installed on a public building roof and simulates a rain gauge combined with sensors describing accumulated rainfall and drainage saturation.

**Location:** Lugano city centre / Cassarate urban catchment, Canton Ticino, Switzerland  
**Thing to register in istSOS4:** `Urban rainfall station LUG-RAIN-01`  
**Sensor:** Tipping-bucket rain gauge with drainage level sensor

| Parameter | Meaning | Unit | Physical limit | Plausibility threshold | Statistical threshold |
|---|---|---:|---:|---:|---:|
| `rainfall_intensity_mm_h` | Short-term rainfall intensity | mm/h | 0 – 300 | 0 – 180 | 0 – 35 |
| `cumulated_rainfall_mm` | Cumulated rainfall since the beginning of the event | mm | 0 – 400 | 0 – 250 | 0 – 45 |
| `drain_level_pct` | Urban drainage filling level | % | 0 – 150 | 0 – 120 | 0 – 70 |

See [Urban Rainfall notebook](https://raw.githubusercontent.com/istSOS/istsos4-workshop/refs/heads/main/workshop/jupyter/content/notebooks/assignment_04_urban_rainfall_monitoring.ipynb)