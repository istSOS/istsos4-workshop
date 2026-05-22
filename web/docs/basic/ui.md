---
title: Exploring the User Interface
description: Learn how to navigate the istSOS4 user interface and create the SensorThings entities required for a sensor configuration.
icon: lucide/app-window
---

# Exploring the User Interface

This tutorial explains how to use the istSOS4 user interface to create and connect the entities required for a sensor configuration.

The user interface lets us work with the platform visually, without sending API requests manually. In this workflow, we will create and associate the main SensorThings entities:

- **Thing**
- **Location**
- **Sensor**
- **Observed Property**
- **Datastream**

By the end of the tutorial, the selected sensor group will be fully configured and ready to receive observations.

## User Interface Overview

The istSOS4 user interface provides access to the available services and resources through a web-based environment.

Using the interface, we can inspect existing entities, create new ones, and manage their relationships through a guided workflow. This helps us understand how the different parts of the SensorThings data model are connected.

For this tutorial, open the user interface at: <https://istsos.org/gui>

### :lucide-play: Login

Sign in to the user interface using the administrator credentials:

- **Username:** `admin`
- **Password:** `admin`

<div align="center">
  <img src="../images/ui/login-form.png" alt="Login form" style="border: 1px solid #000;" />
</div>

After logging in, the main dashboard is displayed.

<div align="center">
  <img src="../images/ui/main-dashboard.png" alt="Main dashboard" style="border: 1px solid #000;" />
</div>

From the dashboard, we can start creating the entities associated with our sensor group.

### :lucide-play: Create the Sensor Entities

To create a new set of entities, start from the map.

Right-click on the map to open the context menu, then select **Add New**.

<div align="center">
  <img src="../images/ui/add-new.png" alt="Add new entity from the map menu" style="border: 1px solid #000;" />
</div>

The creation wizard opens. For this tutorial, keep **Associated Entities** selected.

This option allows us to create or select the entities related to the sensor step by step.

### :lucide-play: Create the Thing

The first entity to configure is the **Thing**.

A Thing represents the physical or logical object associated with the observations. In this tutorial, it represents the sensor group that we are going to configure.

Select **New Thing** and complete the fields as follows:

- **Name:** `GROUP_<number>`
- **Description:** `Environmental sensor located in the SUPSI building`

The `<number>` must match the number of the selected `SENSOR_<number>`.

For example, if you are working with `SENSOR_3`, the Thing name should be:

`GROUP_3`

<div align="center">
  <img src="../images/ui/thing.png" alt="Create a new Thing" style="border: 1px solid #000;" />
</div>

After completing the fields, click **Next**.

### :lucide-play: Select the Location

Next, associate the Thing with a **Location**.

For this tutorial, use the existing Location that represents the room. From the selection list, choose:

`SUPSI`

<div align="center">
  <img src="../images/ui/location.png" alt="Select the Location" style="border: 1px solid #000;" />
</div>

After selecting the Location, click **Next**.

### :lucide-play: Create the Sensor

Now configure the **Sensor**.

The Sensor describes the device or procedure used to produce the observations. In this case, we are creating the sensor associated with the internal temperature measurement.

Select **New Sensor** and complete the fields as follows:

- **Name:** `IT_SENSOR_GROUP_<number>`
- **Encoding Type:** `application/json`
- **Metadata:** `IT`
- **Description:** `Internal temperature channel of GROUP_<number>`

For example, if you are working with `GROUP_3`, the Sensor name should be:

`IT_SENSOR_GROUP_3`

<div align="center">
  <img src="../images/ui/sensor.png" alt="Create a new Sensor" style="border: 1px solid #000;" />
</div>

After completing the Sensor information, click **Next**.

### :lucide-play: Select the Observed Property

The **Observed Property** defines what the Sensor measures.

For this tutorial, select the existing Observed Property:

`internal:temperature`

This property is used because the sensor we are configuring measures internal temperature.

<div align="center">
  <img src="../images/ui/observed-property.png" alt="Select the Observed Property" style="border: 1px solid #000;" />
</div>

After selecting the Observed Property, click **Next**.

### :lucide-play: Create the Datastream

The next step is to create the **Datastream**.

A Datastream connects the **Thing**, **Sensor**, and **Observed Property**. It describes the stream of observations collected for a specific measured property.

Select **New Datastream** and complete the fields as follows:

- **Name:** `IT_GROUP_<number>`
- **Observation Type:** `http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement`
- **Description:** `Internal air temperature measured by GROUP_<number>`
- **Unit of Measurement:**
    - **Name:** `name`
    - **Value:** `Degree Celsius`
    - **Name:** `symbol`
    - **Value:** `°C`
- **Properties:**
  - **Name:** `samplingFrequency`
  - **Value:** `PT5M`
- **Network:** `DDT_network`

For example, if you are working with `GROUP_3`, the Datastream name should be:

`IT_GROUP_3`

<div align="center">
  <img src="../images/ui/datastream.png" alt="Create a new Datastream" style="border: 1px solid #000;" />
</div>

After completing all Datastream fields, click **Next**.

### :lucide-play: Review and Finish

In the **Review** section, check the entities that will be created or associated.

Before completing the process, verify that:

- the Thing uses the correct group number;
- the Location is set to `SUPSI`;
- the Sensor refers to the internal temperature channel;
- the Observed Property is set to `internal:temperature`;
- the Datastream is connected to `DDT_network`.

Then enter a **Commit Message** that clearly describes the operation, for example:

`IT for GROUP_<number>`

<div align="center">
  <img src="../images/ui/review.png" alt="Review the entity configuration" style="border: 1px solid #000;" />
</div>

After reviewing the configuration and entering the commit message, click **Finish** to complete the creation process.

### :lucide-play: Repeat the Process for the Other Observed Properties

After creating the Datastream for internal temperature, repeat the same workflow for the remaining observed properties.

The remaining observed properties are listed below.

For each Observed Property, create a dedicated **Sensor** and a dedicated **Datastream**.  
The `unitOfMeasurement` value must be entered in the **Datastream**, because it is a Datastream key that describes the unit used by the observations in that specific data stream.

- `internal:air:humidity`

  ```json
  "unitOfMeasurement": {
    "name": "Percent",
    "symbol": "%"
  }
  ```

- `internal:pressure`

  ```json
  "unitOfMeasurement": {
    "name": "Hectopascal",
    "symbol": "hPa"
  }
  ```

- `internal:lux`

  ```json
  "unitOfMeasurement": {
    "name": "Lux",
    "symbol": "lx"
  }
  ```

- `external:wall:temperature`

  ```json
  "unitOfMeasurement": {
    "name": "Degree Celsius",
    "symbol": "°C"
  }
  ```

- `external:water:temperature`

  ```json
  "unitOfMeasurement": {
    "name": "Degree Celsius",
    "symbol": "°C"
  }
  ```

- `sensor:battery`

  ```json
  "unitOfMeasurement": {
    "name": "Battery level fraction",
    "symbol": "1"
  }
  ```

For each property, adapt the Sensor and Datastream names according to the measurement type while keeping the same group number.

For example, if you are working with `GROUP_3`, every Datastream should refer to `GROUP_3` and clearly describe the specific measurement it represents.

Before clicking **Finish**, always check the **Review** section and make sure that:

- the correct Observed Property has been selected;
- the Sensor name matches the selected property;
- the Datastream name is clear and consistent;
- the Datastream is associated with the correct Thing and Network;
- the Commit Message describes the operation clearly.

After all observed properties have been configured, the sensor group is fully described in the system and ready to receive observations.