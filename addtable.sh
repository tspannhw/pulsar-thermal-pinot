docker exec -it pinot-controller bin/pinot-admin.sh AddTable   \
  -tableConfigFile /config/table.json -schemaFile /config/schema.json  \
  -exec
