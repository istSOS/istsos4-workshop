# Using Python notebooks

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
