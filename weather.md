#### Pulsar - Pinot - Weather

#### Weather Function builds topics

#### Consume Weather Topic from Pulsar

````
bin/pulsar-client consume "persistent://public/default/aircraftweather2" -s test1 -n 0

----- got message -----
key:[9a88cbf5-92df-4546-bda5-a57dba7e453f], properties:[language=Java], content:{"location":"Greenwood, Greenwood County Airport, SC","station_id":"KGRD","latitude":34.24722,"longitude":-82.15472,"observation_time":"Last Updated on Dec 8 2022, 8:56 am EST","observation_time_rfc822":"Thu, 08 Dec 2022 08:56:00 -0500","weather":"Fog","temperature_string":"61.0 F (16.1 C)","temp_f":61.0,"temp_c":16.1,"relative_humidity":100,"wind_string":"Calm","wind_dir":"North","wind_degrees":0,"wind_mph":0.0,"wind_kt":0,"pressure_string":"1023.5 mb","pressure_mb":1023.5,"pressure_in":30.24,"dewpoint_string":"61.0 F (16.1 C)","dewpoint_f":61.0,"dewpoint_c":16.1,"heat_index_f":0,"heat_index_c":0,"visibility_mi":0.25,"icon_url_base":"https://forecast.weather.gov/images/wtf/small/","two_day_history_url":"https://www.weather.gov/data/obhistory/KGRD.html","icon_url_name":"fg.png","ob_url":"https://www.weather.gov/data/METAR/KGRD.1.txt","uuid":"d429a3e3-d12d-4297-9192-81a2985d8725","ts":1670520773418}

````

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

#### Pinot to Superset connection

pinot+http://192.168.1.157:8099/query?server=192.168.1.157:9000/

pinot+http://timothys-mbp:8099/query?server=http://timothys-mbp:9000/

See:  https://docs.pinot.apache.org/integrations/superset

#### Example Data - data/weather.json

````
{"location":"Union County Airport - Troy Shelton Field, SC","station_id":"K35A","latitude":34.68695,"longitude":-81.64117,"observation_time":"Last Updated on Dec 7 2022, 3:35 pm EST","observation_time_rfc822":"Wed, 07 Dec 2022 15:35:00 -0500","weather":"Overcast","temperature_string":"64.0 F (17.7 C)","temp_f":64.0,"temp_c":17.7,"relative_humidity":98,"wind_string":"Southwest at 4.6 MPH (4 KT)","wind_dir":"Southwest","wind_degrees":220,"wind_mph":4.6,"wind_kt":4,"pressure_mb":0.0,"pressure_in":30.26,"dewpoint_string":"63.1 F (17.3 C)","dewpoint_f":63.1,"dewpoint_c":17.3,"heat_index_f":0,"heat_index_c":0,"visibility_mi":10.0,"icon_url_base":"https://forecast.weather.gov/images/wtf/small/","two_day_history_url":"https://www.weather.gov/data/obhistory/K35A.html","icon_url_name":"ovc.png","ob_url":"https://www.weather.gov/data/METAR/K35A.1.txt","uuid":"5d6ac217-9c3d-4228-87d4-778cbf8561a2","ts":1670508009894}
````

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
   'catalog-service-url' = 'pulsar://Timothys-MBP:6650',
   'catalog-admin-url' = 'http://Timothys-MBP:8080'
);

USE CATALOG pulsar;

show databases;

use `public/default`;

SHOW TABLES;


CREATE TABLE airportweather3 (
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

desc aircraftweather2;

+-------------------------+--------+-------+-----+--------+-----------+
|                    name |   type |  null | key | extras | watermark |
+-------------------------+--------+-------+-----+--------+-----------+
|              dewpoint_c | DOUBLE | FALSE |     |        |           |
|              dewpoint_f | DOUBLE | FALSE |     |        |           |
|         dewpoint_string | STRING |  TRUE |     |        |           |
|            heat_index_c |    INT | FALSE |     |        |           |
|            heat_index_f |    INT | FALSE |     |        |           |
|       heat_index_string | STRING |  TRUE |     |        |           |
|           icon_url_base | STRING |  TRUE |     |        |           |
|           icon_url_name | STRING |  TRUE |     |        |           |
|                latitude | DOUBLE | FALSE |     |        |           |
|                location | STRING |  TRUE |     |        |           |
|               longitude | DOUBLE | FALSE |     |        |           |
|                  ob_url | STRING |  TRUE |     |        |           |
|        observation_time | STRING |  TRUE |     |        |           |
| observation_time_rfc822 | STRING |  TRUE |     |        |           |
|             pressure_in | DOUBLE | FALSE |     |        |           |
|             pressure_mb | DOUBLE | FALSE |     |        |           |
|         pressure_string | STRING |  TRUE |     |        |           |
|       relative_humidity |    INT | FALSE |     |        |           |
|              station_id | STRING |  TRUE |     |        |           |
|                  temp_c | DOUBLE | FALSE |     |        |           |
|                  temp_f | DOUBLE | FALSE |     |        |           |
|      temperature_string | STRING |  TRUE |     |        |           |
|                      ts | BIGINT | FALSE |     |        |           |
|     two_day_history_url | STRING |  TRUE |     |        |           |
|                    uuid | STRING |  TRUE |     |        |           |
|           visibility_mi | DOUBLE | FALSE |     |        |           |
|                 weather | STRING |  TRUE |     |        |           |
|            wind_degrees |    INT | FALSE |     |        |           |
|                wind_dir | STRING |  TRUE |     |        |           |
|                 wind_kt |    INT | FALSE |     |        |           |
|                wind_mph | DOUBLE | FALSE |     |        |           |
|             wind_string | STRING |  TRUE |     |        |           |
+-------------------------+--------+-------+-----+--------+-----------+
32 rows in set


````


#### References

* https://github.com/streamnative/pulsar-flink-patterns
* https://nightlies.apache.org/flink/flink-docs-master/docs/deployment/resource-providers/standalone/docker/
