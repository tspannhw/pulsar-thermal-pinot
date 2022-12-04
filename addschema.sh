docker exec -it pinot-controller bin/pinot-admin.sh AddSchema   \
  -schemaFile /config/schema.json \
  -exec
