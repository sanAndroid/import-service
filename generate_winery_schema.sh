#!/bin/bash
source ./winery_scrapers/venv/bin/activate
python3 ./winery_scrapers/generate_schema.py
python3 ./winery_scrapers/fix_schema.py <./winery_scrapers/winery-schema.json >./transformer-service/model/src/main/resources/schema/vdp_winery_dto.json
deactivate
cd ./transformer-service/model/
mvn clean generate-sources
