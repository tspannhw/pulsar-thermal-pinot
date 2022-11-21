# pulsar-thermal-pinot
Apache Pulsar - Apache Pinot - Thermal Sensor Data

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
  
````


#### References

* https://github.com/tspannhw/FLiP-Pi-DeltaLake-Thermal
* https://github.com/tspannhw/FLiP-Pi-Thermal
* https://github.com/tspannhw/FLiP-Pi-Thermal/blob/main/cloudsensors.md
* https://docs.pinot.apache.org/integrations/superset
