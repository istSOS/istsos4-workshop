---
title: View data
description: Learn how to view and analyze the data collected by your sensors using the istSOS4 user interface.
icon: lucide/chart-line
---

# Viewing and Analyzing Sensor Data

In this section, we will explore how to view and analyze the data collected by your sensors using the istSOS4 user interface. After configuring your sensors and sending observations to the SensorThings API, you can use the interface to visualize the data, create charts, and gain insights from your sensor measurements.

Open the user interface at: <https://istsos.org/gui> and log in with the `admin/admin` credentials.

### :lucide-play: View Sensor Data

To view the data collected by your sensors, navigate to the **Data sources** panel of the user interface. Here, you can select the specific `Thing`, `Datastream`, or `Observed Property` you want to analyze.

Click on the things icon on the map to open the data sources panel.

![Data sources panel](../images/ui_things_data.png)

### :lucide-play: View Charts

Once you have selected a specific `Datastream`, you can view the associated observations in a chart format. Click on the chart icon to open the chart view.

![Chart view](../images/ui_chart_view.png)

### :lucide-play: Compare series

If you select the **Observed Property** dropdown, you can view the data from all datastreams associated with that `Thing`. Select the observed property you are interested in to compare measurements from different sensors observing the same phenomenon.

![Multiple datastreams](../images/ui_chart_view2.png)

### :lucide-play: Create dashboards via Grafana

You can also visualize istSOS4 observations using Grafana (<http://localhost:3000> or <https://istsos.org/grafana>). Grafana allows you to create dashboards, configure panels, apply filters, and compare time series from different datastreams.

Open Grafana and log in with the default credentials:

```txt
admin / admin
```

![Grafana login page](../images/grafana/0.png)

After logging in, open **Connections** from the left navigation menu. This page lets you add a new data source connection or manage existing connections.

![Grafana Connections page](../images/grafana/1.png)

Click **Add new connection**. In the search bar, type `supsi` and select the **istSOS4** data source plugin.

![Search istSOS4 plugin in Grafana](../images/grafana/2.png)

Open the plugin page and click **Add new data source**.

> Depending on your Grafana installation, the plugin may be shown as unsigned. Make sure the plugin comes from a trusted source before using it.

![istSOS4 Grafana plugin page](../images/grafana/3.png)

Configure the data source by setting the API endpoint of the SensorThings service.

For example, to connect to the public istSOS4 demo service, use:

```txt
https://istsos.org/v4/v1.1
```

Set the authentication method to **Anonymous**, then click **Save & test**. If the connection is valid, Grafana displays a successful connection message.

![Configure and test istSOS4 data source](../images/grafana/4.png)

After the data source has been configured, open the **Dashboards** section and click **Create dashboard**.

![Create a new Grafana dashboard](../images/grafana/5.png)

In the new dashboard screen, add a panel. You can use the default custom grid layout.

![New Grafana dashboard](../images/grafana/6.png)

Click **Configure visualization** to open the panel editor.

![Configure a new panel visualization](../images/grafana/7.png)

In the panel editor, make sure the configured istSOS4 data source is selected in the query area.

![Grafana panel editor with istSOS4 data source](../images/grafana/8.png)

Open **All visualizations** from the right side panel and select **Time series**. This visualization type is suitable for observations collected over time.

![Select the time series visualization](../images/grafana/9.png)

In the query editor, select the entity you want to query. To visualize sensor measurements, select **Observations** as the entity.

Configure the result options as follows:

- **Time range**: `phenomenonTime`
- **$orderby**: `phenomenonTime desc`
- **$select**: leave empty unless you want to restrict the returned fields
- **$top**: optional limit for the number of observations
- **$skip**: optional offset for pagination

Set the panel title to the name of the datastream you want to display. For example:

```txt
INTERNAL_TEMPERATURE_GROUP_010
```

![Configure observations query and panel title](../images/grafana/10.png)

To visualize observations from a specific datastream, add an entity filter with the following settings:

- **Related entity**: `Datastreams`
- **Entity field**: `Name`
- **Operator**: `Equals`
- **Value**: the name of the datastream, for example `INTERNAL_TEMPERATURE_GROUP_010`

The plugin generates a SensorThings API query automatically. For example, the query preview may look like this:

```txt
/Observations?$filter=Datastream/name eq 'INTERNAL_TEMPERATURE_GROUP_010' and phenomenonTime ge '${__from:date:iso}' and phenomenonTime le '${__to:date:iso}'&$orderby=phenomenonTime desc
```

The Grafana time range is automatically applied using the `phenomenonTime` property. You can change the time interval from the time picker in the top-right corner of the dashboard.

![Configure Grafana query filter and preview](../images/grafana/11.png)

To make the chart easier to read, open the panel options on the right side of the screen. In **Standard options**, set the unit of measurement to **Celsius (°C)**.

![Set the time series unit to Celsius](../images/grafana/12.png)

This makes the time series name explicit and displays the temperature values with the correct unit on the chart axis and tooltip.

When the panel is ready, click **Save dashboard**. Enter a dashboard title, for example `GROUP_010`, select the destination folder, and click **Save**.

![Save Grafana dashboard](../images/grafana/13.png)

The dashboard now displays the `INTERNAL_TEMPERATURE_GROUP_010` time series with temperature values expressed in degrees Celsius.

![Grafana dashboard with temperature time series](../images/grafana/14.png)

You can repeat the same process to add more panels and compare multiple datastreams in the same dashboard.