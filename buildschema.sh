docker exec -it pinot-controller bin/pinot-admin.sh JsonToPinotSchema \
  -timeColumnName ts \
  -metrics ""\
  -dimensions "" \
  -pinotSchemaName=transit \
  -jsonFile=/data/transit.json \
  -outputDir=/config
