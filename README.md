# pulsar-thermal-pinot
Apache Pulsar - Apache Pinot - Thermal Sensor Data


### Access Docker Container

````

docker exec -it pinot-controller /bin/bash

````

### Build a Schema From Data

````

docker exec -it pinot-controller bin/pinot-admin.sh JsonToPinotSchema \
  -timeColumnName ts \
  -metrics "temperature,humidity,co2,totalvocppb,equivalentco2ppm,pressure,temperatureicp,cputempf"\
  -dimensions "host,ipaddress" \
  -pinotSchemaName=thermal \
  -jsonFile=/data/thermal.json \
  -outputDir=/config
  
````

#### Consume Data in Pulsar

````

bin/pulsar-client consume "persistent://public/default/thermalsensors" -s "thrmlsnosconsumer" -n 0

````

### Data

````

{
 "uuid": "thrml_qsx_20221121215610",
 "ipaddress": "192.168.1.179",
 "cputempf": 115,
 "runtime": 0,
 "host": "thermal",
 "hostname": "thermal",
 "macaddress": "e4:5f:01:7c:3f:34",
 "endtime": "1669067770.6400402",
 "te": "0.0005550384521484375",
 "cpu": 4.5,
 "diskusage": "102676.2 MB",
 "memory": 9.7,
 "rowid": "20221121215610_8e753591-cb7c-4e1c-886d-85cb3dba6c50",
 "systemtime": "11/21/2022 16:56:15",
 "ts": 1669067775,
 "starttime": "11/21/2022 16:56:10",
 "datetimestamp": "2022-11-21 21:56:14.404291+00:00",
 "temperature": 27.9069,
 "humidity": 24.89,
 "co2": 698.0,
 "totalvocppb": 0.0,
 "equivalentco2ppm": 65535.0,
 "pressure": 102048.65,
 "temperatureicp": 82.0
}

````

#### Add our schema

````

docker exec -it pinot-controller bin/pinot-admin.sh AddSchema   \
  -schemaFile /config/thermalschema.json \
  -exec
  
  
docker exec -it pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/thermaltable.json -schemaFile /config/thermalschema.json  \
  -exec
  
````

#### Add Table Via Swagger UI / Curl

````

curl -X POST "http://localhost:9000/tables" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"tableName\": \"thermal\", \"tableType\": \"REALTIME\", \"segmentsConfig\": { \"timeColumnName\": \"ts\", \"schemaName\": \"thermal\", \"replication\": \"1\", \"replicasPerPartition\": \"1\" }, \"ingestionConfig\": { \"batchIngestionConfig\": { \"segmentIngestionType\": \"APPEND\", \"segmentIngestionFrequency\": \"DAILY\" } }, \"tableIndexConfig\": { \"loadMode\": \"MMAP\", \"streamConfigs\": { \"streamType\": \"pulsar\", \"stream.pulsar.topic.name\": \"persistent://public/default/thermalsensors\", \"stream.pulsar.bootstrap.servers\": \"pulsar://192.168.1.157:6650\", \"stream.pulsar.consumer.type\": \"lowlevel\", \"stream.pulsar.fetch.timeout.millis\": \"10000\", \"stream.pulsar.consumer.prop.auto.offset.reset\": \"smallest\", \"stream.pulsar.consumer.factory.class.name\": \"org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory\", \"stream.pulsar.decoder.class.name\": \"org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder\", \"realtime.segment.flush.threshold.rows\": \"0\", \"realtime.segment.flush.threshold.time\": \"1h\", \"realtime.segment.flush.threshold.segment.size\": \"5M\" } }, \"tenants\": {}, \"metadata\": {}}"

````

#### References

* https://github.com/tspannhw/FLiP-Pi-DeltaLake-Thermal
* https://github.com/tspannhw/FLiP-Pi-Thermal
* https://github.com/tspannhw/FLiP-Pi-Thermal/blob/main/cloudsensors.md
* https://docs.pinot.apache.org/integrations/superset
* https://dev.startree.ai/docs/pinot/recipes/pulsar
* https://dev.startree.ai/docs/pinot/recipes/infer-schema-json-data
* https://github.com/startreedata/pinot-recipes/blob/main/recipes/json-nested/README.md
* https://medium.com/apache-pinot-developer-blog/building-a-climate-dashboard-with-apache-pinot-and-superset-d3ee8cb7941d
* https://dev.startree.ai/docs/pinot/recipes/pulsar
* https://github.com/startreedata/pinot-recipes/tree/main/recipes/pulsar
* https://github.com/apache/pinot/blob/master/pinot-tools/src/main/resources/examples/stream/airlineStats/airlineStats_schema.json


