


#### Airport Weather Flink SQL Table

````

CREATE CATALOG pulsar WITH (
   'type' = 'pulsar-catalog',
   'catalog-service-url' = 'pulsar://localhost:6650',
   'catalog-admin-url' = 'http://localhost:8080'
);

SHOW CURRENT DATABASE;
SHOW DATABASES;

USE CATALOG pulsar;

set table.dynamic-table-options.enabled = true;

show databases;

use `public/default`;

SHOW TABLES;


CREATE TABLE airportweather (
`dewpoint_c` DOUBLE,                      
`dewpoint_f` DOUBLE,                      
`dewpoint_string` STRING,                       
`heat_index_c` INT,                      
`heat_index_f` INT,                      
`heat_index_string` STRING,                       
`icon_url_base` STRING,                       
`icon_url_name` STRING,                       
`latitude` DOUBLE,                      
`location` STRING,                       
`longitude` DOUBLE,                      
`ob_url` STRING,                       
`observation_time` STRING,                       
`observation_time_rfc822` STRING,                       
`pressure_in` DOUBLE,                      
`pressure_mb` DOUBLE,                      
`pressure_string` STRING,                       
`relative_humidity` INT,                      
`station_id` STRING,                       
`temp_c` DOUBLE,                      
`temp_f` DOUBLE,                      
`temperature_string` STRING,                       
`two_day_history_url` STRING,                       
`visibility_mi` DOUBLE,                      
`weather` STRING,                       
`wind_degrees` INT,                      
`wind_dir` STRING,                       
`wind_kt` INT,                      
`wind_mph` DOUBLE,                      
`wind_string` STRING
) WITH (
  'connector' = 'pulsar',
  'topics' = 'persistent://public/default/aircraftweather',
  'format' = 'json',
  'admin-url' = 'http://localhost:8080',
  'service-url' = 'pulsar://localhost:6650'
)


````
