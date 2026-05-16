---
title: Air Quality Dashboard
---

Welcome to the Air Quality Dashboard! Here is the latest data pulled from AirNow and transformed via dbt.

```sql air_quality
select
    DateObserved,
    HourObserved,
    ParameterName,
    AQI,
    ReportingArea,
    StateCode
from air_quality.airnow_data
```

## Raw Data
<DataTable data={air_quality} />

## AQI by Parameter
<BarChart 
    data={air_quality} 
    x=ParameterName
    y=AQI 
    title="AQI by Parameter"
/>
