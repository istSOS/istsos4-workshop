---
title: View data
description: Learn how to view and analyze the data collected by your sensors using the istSOS4 user interface.
icon: lucide/chart-line
---

# Viewing and Analyzing Sensor Data

In this section, we will explore how to view and analyze the data collected by your sensors using the istSOS4 user interface. After configuring your sensors and sending observations to the SensorThings API, you can use the interface to visualize the data, create charts, and gain insights from your sensor measurements.

Open the user interface at: <https://istsos.org/gui> and login with admin/admin credentials.

### :lucide-play: View Sensor Data
To view the data collected by your sensors, navigate to the **Data sources** panel of the user interface. Here, you can select the specific `Thing`, `Datastream`, or `Observed Property` you want to analyze.

Click on the things icon on the map to open the data sources panel.

![Data sources panel](../images/ui_things_data.png)

### :lucide-play: View Charts
Once you have selected a specific `Datastream`, you can view the associated observations in a chart format. Click on the chart icon to open the chart view.

![Chart view](../images/ui_chart_view.png)

### :lucide-play: Compare series
If you select the Observed propertiy dropdown, you can view the data from all datastreams associated with that othings. Selecting the one interested This allows you to compare measurements from different sensors that are observing the same phenomenon.

![Multiple datastreams](../images/ui_chart_view2.png)