# pyasic_dashboard

_An interactive dashboard for visualizing [pyasic](https://github.com/UpstreamData/pyasic) data._

---

### Installation

`poetry install`

---

### Saving Data

Miner data can be saved to a SQLite database or CSV file. Data is preprocessed as a pandas dataframe where dicts for hashboard/fan data are flattened.

```python
import asyncio
from pyasic_dashboard.db import write_data

if __name__ == "__main__":
    asyncio.run(
        write_data(
            ip="192.168.1.75",
            data_file="miner_data.db",  # Use .csv extension to save as CSV file
            sleep_mins=1,  # Number of minutes to wait between writes
        )
    )
```

Alternatively, you can use the command `python pyasic_dashboard/db/save_data.py 192.168.1.75 miner_data.db 1`

[Example notebook](examples/example_db.ipynb)

---

### Dashboard

If you have [saved miner data to SQLite](#saving-data), you can analyze it with interactive python visualizations in a plotly [dash](https://dash.plotly.com/) app.

- `python pyasic_dashboard/app.py examples/change_power.db`
- go to `http://localhost:8050/` in your browser

##### Status

<!-- ![status](examples/status.png) -->
<img src="examples/status.png" width="75%" alt="status">

##### Hashrate

<!-- ![hashrate](examples/hashrate.png) -->
<img src="examples/status.png" width="75%" alt="hashrate">

##### Temperature

<!-- ![temperature](examples/temperature.png) -->
<img src="examples/status.png" width="75%" alt="temperature">
