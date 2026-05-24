---
title: Temporal Queries
description: Understanding and managing temporal queries
icon: lucide/clock
---

## Temporal queries

Temporal queries extend the traditional concept of data management by allowing users to access not only the current state of information, but also its past states. In practice, this means that every modification applied to a resource is preserved together with its validity in time, making it possible to reconstruct how the data looked at any specific moment. Rather than overwriting information, the system maintains a continuous history of changes, enabling transparency and reproducibility.

![Temporal Queries](../images/traveltime_temporal_queries.png)

This concept of system-versioned tables was introduced in the SQL standard (ISO/IEC 9075-7). The core idea is that data evolves over time and that preserving this evolution is essential for several advanced use cases. These include:

- auditing and accountability, 
- forensic analysis, 
- retrospective data analytics, 
- comparison of historical states, and 
- point-in-time recovery of information.

Additionally it is worth noting that the concept applies to system-time and not to business-time. System-time refers to the actual time when changes are made to the data, while business-time refers to the time period that the data is valid for in the real world. Temporal queries typically focus on system-time, allowing users to track when changes occurred and how data evolved over time, regardless of the business context or validity period of the information.

