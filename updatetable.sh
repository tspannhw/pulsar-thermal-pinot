docker exec -it pinot-controller-pulsar bin/pinot-admin.sh ChangeTableState -tableName events -state disable  9000 -exec

docker exec -it pinot-controller-pulsar bin/pinot-admin.sh ChangeTableState -tableName events -state drop  9000 -exec

docker exec -it pinot-controller-pulsar bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json -schemaFile /config/schema.json  \
  -exec
