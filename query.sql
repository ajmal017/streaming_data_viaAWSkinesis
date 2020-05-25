With hrs_dataset as (
SELECT  cast(substr(ts,12,2) as integer) hr,low,high,name,ts FROM "stockdb"."data_collector_bucket_ak")
select
hrds.name company_name,
hrds.high high_stock_price,
hrds.ts data_time,
hrds.hr hour_of_day
from hrs_dataset hrds
inner join (
select distinct name,hr,max(high) over (Partition by hr,name) as rolling_max from hrs_dataset ) maxset
on
maxset.rolling_max = hrds.high
and maxset.name = hrds.name
and maxset.hr = hrds.hr
order by hrds.name,hrds.hr
