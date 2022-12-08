#### Pulsar - Pinot - Weather

#### Weather Function builds topics


#### Build Pinot Schema

````

docker exec -it pinot-controller bin/pinot-admin.sh JsonToPinotSchema \
  -timeColumnName ts \
  -metrics "pressure_in,temp_c,temp_f,wind_mph,relative_humidity,pressure_mb"\
  -dimensions "station_id,location,latitude,longitude" \
  -pinotSchemaName=weather \
  -jsonFile=/data/weather.json \
  -outputDir=/config
  
  
````

#### Load Pinot Schema and Table

````

docker exec -it pinot-controller bin/pinot-admin.sh AddSchema   \
  -schemaFile /config/weatherschema.json \
  -exec

````

````
curl -X POST "http://localhost:9000/tables" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"tableName\": \"weather\", \"tableType\": \"REALTIME\", \"segmentsConfig\": { \"timeColumnName\": \"ts\", \"schemaName\": \"weather\", \"replication\": \"1\", \"replicasPerPartition\": \"1\" }, \"ingestionConfig\": { \"batchIngestionConfig\": { \"segmentIngestionType\": \"APPEND\", \"segmentIngestionFrequency\": \"DAILY\" } }, \"tableIndexConfig\": { \"loadMode\": \"MMAP\", \"streamConfigs\": { \"streamType\": \"pulsar\", \"stream.pulsar.topic.name\": \"persistent://public/default/aircraftweather2\", \"stream.pulsar.bootstrap.servers\": \"pulsar://Timothys-MBP:6650\", \"stream.pulsar.consumer.type\": \"lowlevel\", \"stream.pulsar.fetch.timeout.millis\": \"10000\", \"stream.pulsar.consumer.prop.auto.offset.reset\": \"largest\", \"stream.pulsar.consumer.factory.class.name\": \"org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory\", \"stream.pulsar.decoder.class.name\": \"org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder\", \"realtime.segment.flush.threshold.rows\": \"0\", \"realtime.segment.flush.threshold.time\": \"1h\", \"realtime.segment.flush.threshold.segment.size\": \"5M\" } }, \"tenants\": {}, \"metadata\": {}}"
````

#### Pulsar Schmea

````
{
  "type" : "record",
  "name" : "Weather",
  "namespace" : "dev.pulsarfunction.weather",
  "fields" : [ {
    "name" : "dewpoint_c",
    "type" : "double"
  }, {
    "name" : "dewpoint_f",
    "type" : "double"
  }, {
    "name" : "dewpoint_string",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "heat_index_c",
    "type" : "int"
  }, {
    "name" : "heat_index_f",
    "type" : "int"
  }, {
    "name" : "heat_index_string",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "icon_url_base",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "icon_url_name",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "latitude",
    "type" : "double"
  }, {
    "name" : "location",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "longitude",
    "type" : "double"
  }, {
    "name" : "ob_url",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "observation_time",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "observation_time_rfc822",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "pressure_in",
    "type" : "double"
  }, {
    "name" : "pressure_mb",
    "type" : "double"
  }, {
    "name" : "pressure_string",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "relative_humidity",
    "type" : "int"
  }, {
    "name" : "station_id",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "temp_c",
    "type" : "double"
  }, {
    "name" : "temp_f",
    "type" : "double"
  }, {
    "name" : "temperature_string",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "ts",
    "type" : "long"
  }, {
    "name" : "two_day_history_url",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "uuid",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "visibility_mi",
    "type" : "double"
  }, {
    "name" : "weather",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "wind_degrees",
    "type" : "int"
  }, {
    "name" : "wind_dir",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "wind_kt",
    "type" : "int"
  }, {
    "name" : "wind_mph",
    "type" : "double"
  }, {
    "name" : "wind_string",
    "type" : [ "null", "string" ],
    "default" : null
  } ]
}
````

#### Example Data

#### Start Flink in Docker

* See https://github.com/streamnative/flink-example/blob/main/docs/sql-example.md

````
./bin/start-cluster.sh
./bin/sql-client.sh
````

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
`ts` DOUBLE,
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
  'topics' = 'persistent://public/default/aircraftweather2',
  'format' = 'json',
  'admin-url' = 'http://Timothys-MBP:8080',
  'service-url' = 'pulsar://Timothys-MBP:6650'
)


````
