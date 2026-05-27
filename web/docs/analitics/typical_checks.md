---
title: Quality Checks
description: A guide to common data quality checks for environmental and infrastructure monitoring systems, including sensor drift, missing data, faulty sensor values and extreme events.
icon: lucide/funnel
---

# Typical Data Quality Checks for Smart Monitoring Systems

The following sections provide an overview of common data quality checks for smart monitoring systems, including sensor drift, missing data, faulty sensor values and extreme events. For each issue, we will discuss typical examples, visual and statistical checks, machine learning options and possible correction strategies.

## Missing Data

Missing data occur when expected observations are absent. This is common in wireless sensor networks because of power issues, communication failures, packet loss or maintenance interruptions.

Visual checks:

- time-series plot with gaps;
- missing-value heatmap;
- expected versus actual timestamp frequency.

Statistical checks:

- `isna()` counts;
- time difference between consecutive observations;
- detection of gaps longer than the expected sampling interval.

ML options:

- regression-based imputation;
- Kalman filtering;
- Gaussian process interpolation;
- forecasting-based imputation.

Possible correction:

- linear interpolation for short gaps;
- spline interpolation for smooth signals;
- model-based reconstruction for longer gaps;
- no correction when the gap is too long or during critical periods.

---

## Faulty Sensor Values and Outliers

Faulty values are measurements that are physically impossible or implausible because of malfunction, electronic noise, frozen readings, incorrect unit conversion or transmission errors.

Outliers are observations that deviate strongly from the rest of the dataset. They may be errors or real rare events.

Visual checks:

- time-series plot;
- histogram;
- boxplot;
- rolling median comparison.

Statistical checks:

- physical min/max thresholds;
- z-score;
- modified z-score based on median absolute deviation;
- interquartile range;
- rolling median residuals.

ML options:

- Isolation Forest;
- Local Outlier Factor;
- One-Class SVM;
- autoencoders.

Possible correction:

- replace faulty values with `NaN`;
- interpolate removed values only if gaps are short;
- apply median filtering;
- preserve a quality flag.

Important: not all outliers are errors. In risk monitoring, some outliers may represent real hazardous events.

---
## Sensor Drift

Sensor drift is a progressive deviation of the measured value from the true value. It can be caused by ageing, loss of calibration, fouling, temperature effects or electronic degradation.

Typical examples:

- a water level sensor slowly overestimates river stage;
- a temperature sensor gradually shifts upward;
- a deformation sensor accumulates bias unrelated to real displacement.

Visual checks:

- plot the full time series;
- add a rolling mean;
- compare with a reference station if available;
- inspect residuals after removing expected seasonality.

Statistical checks:

- rolling mean and rolling standard deviation;
- linear trend estimation;
- residual analysis;
- comparison with a stable baseline period.

ML options:

- regression model trained on a clean baseline period;
- residual monitoring;
- change point detection;
- autoencoder reconstruction error.

Possible correction:

- detrending;
- recalibration using a reference sensor;
- flagging data after the estimated drift onset;
- preserving both raw and corrected values.

---

## Extreme Events

Extreme events are rare but real observations associated with hazards. They must not be removed as noise.

Typical examples:

- extreme rainfall;
- flood peak;
- rapid slope displacement;
- abnormal bridge vibration during an earthquake or heavy traffic;
- heat wave.

Visual checks:

- time-series plot with alert thresholds;
- rolling accumulation;
- event-window zoom;
- exceedance plot.

Statistical checks:

- fixed thresholds;
- percentiles such as 95th or 99th percentile;
- return-period thresholds;
- rolling accumulation;
- rate of change;
- duration above threshold.

ML options:

- anomaly detection;
- classification of alert levels;
- forecasting future threshold exceedance;
- sequence models.

Treatment:

- do not correct the event;
- flag it as hazardous;
- compute event statistics;
- use it for alerting and forecasting.

---