#!/bin/bash
source ./wine_scraper/venv/bin/activate
python3 ./wine_scraper/generate_schema.py
python3 ./wine_scraper/fix_schema.py <./wine_scraper/wine-schema.json >./transformer-service/model/src/main/resources/schema/wine_dto.json
deactivate
cd ./transformer-service/model/
mvn clean generate-sources
