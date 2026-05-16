---
title: Air Quality Dashboard
---

Welcome to the Air Quality Dashboard! Here is the historical data pulled from AirNow and transformed via dbt.

```sql unique_cities
select 
    ReportingArea, 
    max(Latitude) as Latitude, 
    max(Longitude) as Longitude 
from air_quality.airnow_data 
group by ReportingArea
```

<GeoRouter cities={unique_cities} />

<Dropdown 
    data={unique_cities} 
    name=area 
    value=ReportingArea 
    defaultValue="Denver" 
/>

```sql air_quality
select
    DateObserved,
    HourObserved,
    ParameterName,
    AQI,
    ReportingArea,
    StateCode
from air_quality.airnow_data
where ReportingArea = '${inputs.area.value}'
```

## AQI Trend for {inputs.area.label}

<LineChart 
    data={air_quality} 
    x=DateObserved
    y=AQI 
    series=ParameterName
    title="AQI Trend (Last 7 Days)"
/>

## Raw Data
<DataTable data={air_quality} />
