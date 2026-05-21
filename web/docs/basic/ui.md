---
title: Exploring the User Interface
description: Learn how to navigate the istSOS4 user interface and access the main features through the web application.
icon: lucide/app-window
---

# Exploring the User Interface

In this tutorial, we will learn how to use the istSOS4 user interface to create the entities required for our sensor.

The user interface allows us to interact with the platform visually, without sending API requests manually. We will use it to create and connect the main SensorThings entities: **Thing**, **Location**, **Sensor**, **Observed Property**, and **Datastream**.

## User Interface Overview

The istSOS4 user interface provides access to the available services and resources through a web-based environment.

Using the interface, we can inspect existing entities, create new ones, and manage their relationships in a guided workflow. This makes it easier to understand how the different parts of the system are connected.

In this tutorial, we will access the user interface at:

<https://istsos.org/gui>

## Login

First, we need to sign in to the user interface using the administrator credentials:

- **Username:** `admin`
- **Password:** `admin`

<div align="center">
  <img src="../images/ui/login-form.png" alt="Login form" />
</div>

After logging in, we are redirected to the main dashboard.

<div align="center">
  <img src="../images/ui/main-dashboard.png" alt="Main dashboard" />
</div>

From the dashboard, we can start creating the entities associated with our sensor.

## Create Entities for Our Sensors

To create a new set of entities, we start from the map.

Right-click on the map to open the context menu, then select **Add New**.

<div align="center">
  <img src="../images/ui/add-new.png" alt="Add new entity from the map menu" />
</div>

The creation wizard opens. For this tutorial, we will use **Associated Entities**, which is already selected by default.

This option allows us to create or select the entities related to our sensor step by step.

## Step 1: Create the Thing

The first entity we need to configure is the **Thing**.

A Thing represents the physical or logical object associated with the observations. In our case, it represents the group sensor that we are going to configure.

Select **New Thing** and fill in the fields as follows:

- **Name:** `GROUP_<number>`
- **Description:** `Environmental sensor located in the SUPSI building`

The `<number>` must match the number of the selected `SENSOR_<number>`.

For example, if we are working with `SENSOR_3`, the Thing name should be:

`GROUP_3`

<div align="center">
  <img src="../images/ui/thing.png" alt="Add new entity from the map menu" />
</div>

Once the fields are completed, click **Next**.

## Step 2: Select the Location

Next, we need to associate the Thing with a **Location**.

For this tutorial, we can use an existing Location that represents our room. From the selection list, choose:

`SUPSI`

<div align="center">
  <img src="../images/ui/location.png" alt="Add new entity from the map menu" />
</div>

After selecting the Location, click **Next**.

## Step 3: Create the Sensor

Now we configure the **Sensor**.

The Sensor describes the device or procedure used to produce the observations. In this case, we are creating the sensor related to the internal temperature measurement.

Select **New Sensor** and fill in the fields as follows:

- **Name:** `IT_SENSOR_GROUP_<number>`
- **Encoding Type:** `application/json`
- **Metadata:** `IT`
- **Description:** `Internal temperature channel of GROUP_<number>`

For example, if we are working with `GROUP_3`, the Sensor name should be:

`IT_SENSOR_GROUP_3`

<div align="center">
  <img src="../images/ui/sensor.png" alt="Add new entity from the map menu" />
</div>

Once the Sensor information is completed, click **Next**.

## Step 4: Select the Observed Property

The **Observed Property** defines what the Sensor measures.

For this tutorial, select the existing Observed Property:

`internal:temperature`

We use this property because the sensor we are configuring measures the internal temperature.

<div align="center">
  <img src="../images/ui/observed-property.png" alt="Add new entity from the map menu" />
</div>

After selecting the Observed Property, click **Next**.

## Step 5: Create the Datastream

The next step is to create the **Datastream**.

A Datastream connects the **Thing**, **Sensor**, and **Observed Property**. It describes the stream of observations that will be collected for a specific measured property.

Select **New Datastream** and fill in the fields as follows:

- **Name:** `IT_GROUP_<number>`
- **Observation Type:** `http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement`
- **Description:** `Internal air temperature measured by GROUP_<number>`
- **Unit of Measurement:**
    - **Name:** `samplingFrequency`
    - **Value:** `PT5M`
- **Network:** `DDT_network`

For example, if we are working with `GROUP_3`, the Datastream name should be:

`IT_GROUP_3`

<div align="center">
  <img src="../images/ui/datastream.png" alt="Add new entity from the map menu" />
</div>

Once all the Datastream fields are completed, click **Next**.

## Step 6: Review and Finish

In the **Review** section, we can check all the entities that will be created or associated.

Before finishing, verify that the configured entities are correct:

- the Thing uses the correct group number;
- the Location is set to `SUPSI`;
- the Sensor refers to the internal temperature channel;
- the Observed Property is `internal:temperature`;
- the Datastream is connected to `DDT_network`.

Finally, enter a **Commit Message** describing the operation, for example:

`IT for GROUP_<number>`

<div align="center">
  <img src="../images/ui/review.png" alt="Add new entity from the map menu" />
</div>

After reviewing the configuration and entering the commit message, click **Finish** to complete the creation process.


## Step 7: Repeat the Process for the Other Observed Properties

After creating the Datastream for the internal temperature, we need to repeat the same workflow for the remaining observed properties.

For each property, we create or select the corresponding **Sensor**, choose the appropriate **Observed Property**, and create a new **Datastream** connected to the same group.

The remaining observed properties are:

- `internal:air:humidity`
- `internal:pressure`
- `internal:lux`
- `external:wall:temperature`
- `external:water:temperature`
- `sensor:battery`

For each of these properties, we should adapt the Sensor and Datastream names according to the measurement type, while keeping the same group number.

For example, if we are working with `GROUP_3`, each Datastream should refer to `GROUP_3` and describe the specific measurement it represents.

Before clicking **Finish**, always check the **Review** section to make sure that:

- the correct Observed Property has been selected;
- the Sensor name matches the selected property;
- the Datastream name is clear and consistent;
- the Datastream is associated with the correct Thing and Network;
- the Commit Message describes the operation clearly.

Once all the observed properties have been configured, our group sensor will be fully described in the system and ready to receive observations.