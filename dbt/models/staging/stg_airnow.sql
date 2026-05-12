-- Staging model for AirNow parquet data
select *
from read_parquet('../data/airnow_*.parquet')
