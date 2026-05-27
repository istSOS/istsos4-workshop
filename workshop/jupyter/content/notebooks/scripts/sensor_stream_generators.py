"""
Reusable real-time sensor stream generators for istSOS4 workshop assignments.

The generator simulates one multi-parameter sensor. Students import this module,
instantiate the generator for their assignment, and call read() inside a loop.

Each call returns one row:

    [phenomenonTime, value_1, value_2, value_3]

The column names are available with:

    generator.cols()

You can use a predefined case:

    generator = RealTimeSensorGenerator("river_level")

Or pass one custom case with the same structure as CASE_PARAMETERS["river_level"]:

    generator = RealTimeSensorGenerator(my_case_parameters)

Quality flags are NOT produced by the generator. Students should classify values
in their notebook and then push observations to istSOS4.
"""

from __future__ import annotations

import random
import time
from datetime import datetime, timezone
from typing import Dict, Iterator, List, Optional, Sequence, Union

Number = Union[int, float]
ParameterConfig = Dict[str, Union[Number, str, Sequence[Number], None]]
CaseParameters = Dict[str, ParameterConfig]


PARAMETER_MEANINGS: Dict[str, str] = {
    "base": "Initial normal value and baseline used by the synthetic signal.",
    "noise": "Standard deviation of the random measurement noise added at each step.",
    "drift": "Linear baseline change added at each generated step to simulate slow sensor or environmental drift.",
    "statistical": "Expected normal range. Values outside this range but inside plausible are classified as suspicious by quality_flag().",
    "plausible": "Physically plausible range. Values outside this range are classified as alarm by quality_flag().",
    "alarm_direction": "Direction used during alarm periods: high, low, or high_abs for absolute positive/negative excursions.",
    "alarm_target": "Optional target value generated during alarm periods. If omitted, the alarm is generated outside the plausible range.",
}


CASE_PARAMETERS: Dict[str, CaseParameters] = {
    "river_level": {
        "water_level_m": {
            "base": 0.85,
            "noise": 0.06,
            "drift": 0.015,
            "statistical": (0.20, 2.20),
            "plausible": (0.05, 4.50),
            "alarm_direction": "high",
            "alarm_target": 5.10,
        },
        "water_temperature_c": {
            "base": 10.5,
            "noise": 0.20,
            "drift": 0.015,
            "statistical": (4.0, 18.0),
            "plausible": (0.0, 28.0),
            "alarm_direction": "high",
            "alarm_target": 29.5,
        },
        "turbidity_ntu": {
            "base": 18.0,
            "noise": 3.0,
            "drift": 0.25,
            "statistical": (0.0, 80.0),
            "plausible": (0.0, 600.0),
            "alarm_direction": "high",
            "alarm_target": 720.0,
        },
    },
    "slope_stability": {
        "tilt_deg": {
            "base": 0.20,
            "noise": 0.04,
            "drift": 0.008,
            "statistical": (-1.5, 1.5),
            "plausible": (-8.0, 8.0),
            "alarm_direction": "high",
            "alarm_target": 9.2,
        },
        "soil_moisture_pct": {
            "base": 32.0,
            "noise": 1.2,
            "drift": 0.20,
            "statistical": (15.0, 55.0),
            "plausible": (0.0, 100.0),
            "alarm_direction": "high",
            "alarm_target": 108.0,
        },
        "pore_pressure_kpa": {
            "base": 8.0,
            "noise": 0.7,
            "drift": 0.18,
            "statistical": (0.0, 25.0),
            "plausible": (-5.0, 80.0),
            "alarm_direction": "high",
            "alarm_target": 92.0,
        },
    },
    "bridge_structural": {
        "vertical_acceleration_g": {
            "base": 0.00,
            "noise": 0.018,
            "drift": 0.000,
            "statistical": (-0.25, 0.25),
            "plausible": (-1.50, 1.50),
            "alarm_direction": "high_abs",
            "alarm_target": 1.85,
        },
        "deck_displacement_mm": {
            "base": 1.5,
            "noise": 0.45,
            "drift": 0.05,
            "statistical": (-15.0, 15.0),
            "plausible": (-80.0, 80.0),
            "alarm_direction": "high_abs",
            "alarm_target": 96.0,
        },
        "cable_temperature_c": {
            "base": 12.0,
            "noise": 0.30,
            "drift": 0.03,
            "statistical": (-5.0, 35.0),
            "plausible": (-25.0, 65.0),
            "alarm_direction": "high",
            "alarm_target": 72.0,
        },
    },
    "urban_rainfall": {
        "rainfall_intensity_mm_h": {
            "base": 2.0,
            "noise": 1.0,
            "drift": 0.35,
            "statistical": (0.0, 35.0),
            "plausible": (0.0, 180.0),
            "alarm_direction": "high",
            "alarm_target": 210.0,
        },
        "cumulated_rainfall_mm": {
            "base": 0.0,
            "noise": 0.35,
            "drift": 1.2,
            "statistical": (0.0, 45.0),
            "plausible": (0.0, 250.0),
            "alarm_direction": "high",
            "alarm_target": 290.0,
        },
        "drain_level_pct": {
            "base": 25.0,
            "noise": 2.5,
            "drift": 0.55,
            "statistical": (0.0, 70.0),
            "plausible": (0.0, 120.0),
            "alarm_direction": "high",
            "alarm_target": 135.0,
        },
    },
}


class RealTimeSensorGenerator:
    """Real-time multi-parameter sensor generator.

    Parameters
    ----------
    case_name:
        One of the predefined cases: river_level, slope_stability,
        bridge_structural, urban_rainfall. If case_parameters is provided,
        this is only used as the custom case label.
    case_parameters:
        Optional custom parameter configuration with the same structure used by
        CASE_PARAMETERS[case_name]. The first-level keys are observation names.
        Each observation configuration supports:
        - base: initial normal value and baseline.
        - noise: random noise standard deviation.
        - drift: baseline change per generated step.
        - statistical: expected normal range, as (min, max).
        - plausible: physically plausible range, as (min, max).
        - alarm_direction: high, low, or high_abs.
        - alarm_target: optional value used during alarm periods.
    step_seconds:
        Real waiting time between two generated rows. Use 30 for the workshop.
    alarm_after_seconds:
        Seconds from the start before the first alarm begins.
    alarm_duration_seconds:
        Duration of each alarm event.
    alarm_repeat_seconds:
        If None, the alarm happens only once. If set to a number, a new alarm
        starts every alarm_repeat_seconds after the beginning of the previous one.
        Example: alarm_after_seconds=600, alarm_duration_seconds=180,
        alarm_repeat_seconds=900 creates alarms at 10-13 min, 25-28 min, etc.
    suspect_probability:
        Probability of a slight statistical anomaly during normal periods.
    seed:
        Optional seed for reproducible simulations.
    """

    def __init__(
        self,
        case_name: Union[str, CaseParameters],
        *,
        case_parameters: Optional[CaseParameters] = None,
        step_seconds: int = 30,
        alarm_after_seconds: int = 600,
        alarm_duration_seconds: int = 180,
        alarm_repeat_seconds: Optional[int] = None,
        suspect_probability: float = 0.08,
        seed: Optional[int] = None,
    ) -> None:
        if isinstance(case_name, dict):
            if case_parameters is not None:
                raise ValueError("Pass either case_name or case_parameters, not both")
            parameters = case_name
            case_label = "custom"
        else:
            case_label = case_name
            parameters = case_parameters

        if parameters is None and case_label not in CASE_PARAMETERS:
            raise ValueError(f"Unknown case_name: {case_name}. Available: {list(CASE_PARAMETERS)}")
        parameters = parameters or CASE_PARAMETERS[case_label]
        self._validate_case_parameters(parameters)
        if step_seconds <= 0:
            raise ValueError("step_seconds must be > 0")
        if alarm_after_seconds < 0:
            raise ValueError("alarm_after_seconds must be >= 0")
        if alarm_duration_seconds <= 0:
            raise ValueError("alarm_duration_seconds must be > 0")
        if alarm_repeat_seconds is not None and alarm_repeat_seconds <= 0:
            raise ValueError("alarm_repeat_seconds must be None or > 0")

        self.case_name = case_label
        self.case_parameters = parameters
        self.step_seconds = step_seconds
        self.alarm_after_seconds = alarm_after_seconds
        self.alarm_duration_seconds = alarm_duration_seconds
        self.alarm_repeat_seconds = alarm_repeat_seconds
        self.suspect_probability = suspect_probability
        self.seed = seed
        self.step_index = 0
        self.elapsed_seconds = 0
        self._state: Dict[str, float] = {
            name: float(cfg["base"]) for name, cfg in self.case_parameters.items()
        }
        self._last_status = "normal"

    def cols(self) -> List[str]:
        """Return the column names of the generated row."""
        return ["phenomenonTime", *self.case_parameters.keys()]

    def parameter_meanings(self) -> Dict[str, str]:
        """Return the meaning of each configuration field."""
        return dict(PARAMETER_MEANINGS)

    def status(self) -> str:
        """Return the status of the last generated row: normal, suspicious, or alarm."""
        return self._last_status

    def read(self, sleep: bool = True) -> List[Union[str, float]]:
        """Return one generated row as [time, value_1, value_2, value_3].

        Set sleep=False while testing to avoid waiting 30 seconds.
        """
        if sleep:
            time.sleep(self.step_seconds)

        row_status = self._current_status()
        rng = random.Random((self.seed or random.randrange(1_000_000_000)) + self.step_index * 7919)
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        values: List[float] = []

        for i, (name, cfg) in enumerate(self.case_parameters.items()):
            if row_status == "alarm":
                value = self._alarm_value(cfg, rng, parameter_index=i)
            else:
                value = self._normal_value(name, cfg, rng)
                if rng.random() < self.suspect_probability:
                    value = self._slightly_outside_statistical(cfg, rng)
                    row_status = "suspicious"

            self._state[name] = value
            values.append(round(value, 3))

        self._last_status = row_status
        self.step_index += 1
        self.elapsed_seconds += self.step_seconds
        return [timestamp, *values]

    def stream(self) -> Iterator[List[Union[str, float]]]:
        """Infinite real-time stream."""
        while True:
            yield self.read(sleep=True)

    def _current_status(self) -> str:
        if self.elapsed_seconds < self.alarm_after_seconds:
            return "normal"

        if self.alarm_repeat_seconds is None:
            alarm_elapsed = self.elapsed_seconds - self.alarm_after_seconds
            return "alarm" if 0 <= alarm_elapsed < self.alarm_duration_seconds else "normal"

        cycle_elapsed = (self.elapsed_seconds - self.alarm_after_seconds) % self.alarm_repeat_seconds
        return "alarm" if cycle_elapsed < self.alarm_duration_seconds else "normal"

    def _normal_value(self, name: str, cfg: ParameterConfig, rng: random.Random) -> float:
        previous = self._state[name]
        baseline = float(cfg["base"]) + float(cfg.get("drift", 0.0) or 0.0) * self.step_index
        # Autoregressive behaviour: smooth evolution, not independent white noise.
        value = previous * 0.80 + baseline * 0.20 + rng.gauss(0, float(cfg.get("noise", 1.0) or 1.0))
        lo, hi = cfg["plausible"]
        return max(lo, min(hi, value))

    @staticmethod
    def _slightly_outside_statistical(cfg: ParameterConfig, rng: random.Random) -> float:
        lo, hi = cfg["statistical"]
        width = hi - lo
        if rng.random() < 0.5:
            return lo - rng.uniform(0.02, 0.10) * width
        return hi + rng.uniform(0.02, 0.10) * width

    @staticmethod
    def _alarm_value(cfg: ParameterConfig, rng: random.Random, parameter_index: int = 0) -> float:
        target = cfg.get("alarm_target")
        direction = cfg.get("alarm_direction", "high")
        if target is not None:
            if direction == "high_abs" and rng.random() < 0.5:
                return -abs(target) + rng.gauss(0, abs(target) * 0.04)
            return float(target) + rng.gauss(0, abs(float(target)) * 0.04)

        lo, hi = cfg["plausible"]
        width = hi - lo
        if direction == "low":
            return lo - rng.uniform(0.05, 0.20) * width
        if direction == "high_abs":
            sign = -1 if rng.random() < 0.5 else 1
            return sign * (max(abs(lo), abs(hi)) + rng.uniform(0.05, 0.20) * width)
        return hi + rng.uniform(0.05, 0.20) * width

    @staticmethod
    def _validate_case_parameters(parameters: CaseParameters) -> None:
        if not parameters:
            raise ValueError("case_parameters must define at least one observation")

        required_fields = ("base", "noise", "statistical", "plausible")
        valid_alarm_directions = {"high", "low", "high_abs"}

        for name, cfg in parameters.items():
            missing = [field for field in required_fields if field not in cfg]
            if missing:
                raise ValueError(f"{name} is missing required fields: {missing}")

            for field in ("statistical", "plausible"):
                values = cfg[field]
                if not isinstance(values, Sequence) or isinstance(values, str) or len(values) != 2:
                    raise ValueError(f"{name}.{field} must be a two-value sequence: (min, max)")
                lo, hi = values
                if not isinstance(lo, (int, float)) or not isinstance(hi, (int, float)):
                    raise ValueError(f"{name}.{field} values must be numeric")
                if lo >= hi:
                    raise ValueError(f"{name}.{field} minimum must be lower than maximum")

            for field in ("base", "noise", "drift", "alarm_target"):
                if field in cfg and cfg[field] is not None and not isinstance(cfg[field], (int, float)):
                    raise ValueError(f"{name}.{field} must be numeric")

            direction = cfg.get("alarm_direction", "high")
            if direction not in valid_alarm_directions:
                raise ValueError(f"{name}.alarm_direction must be one of {sorted(valid_alarm_directions)}")


class RiverLevelGenerator(RealTimeSensorGenerator):
    def __init__(self, **kwargs) -> None:
        super().__init__("river_level", **kwargs)


class SlopeStabilityGenerator(RealTimeSensorGenerator):
    def __init__(self, **kwargs) -> None:
        super().__init__("slope_stability", **kwargs)


class BridgeStructuralGenerator(RealTimeSensorGenerator):
    def __init__(self, **kwargs) -> None:
        super().__init__("bridge_structural", **kwargs)


class UrbanRainfallGenerator(RealTimeSensorGenerator):
    def __init__(self, **kwargs) -> None:
        super().__init__("urban_rainfall", **kwargs)


def make_generator(case_name: str, **kwargs) -> RealTimeSensorGenerator:
    """Factory function useful when the case name is stored in a variable."""
    return RealTimeSensorGenerator(case_name, **kwargs)


def quality_flag(value: Number, statistical: Sequence[Number], plausible: Sequence[Number]) -> int:
    """Example QC helper for notebooks.

    Returns:
    1 = sensible, 2 = suspicious, 3 = alarm.
    Raw value 0 should be used before applying this check.
    """
    stat_min, stat_max = statistical
    plaus_min, plaus_max = plausible
    if value < plaus_min or value > plaus_max:
        return 3
    if value < stat_min or value > stat_max:
        return 2
    return 1
