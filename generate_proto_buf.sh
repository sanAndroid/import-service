#!/bin/bash
# Just creates sources and copies the vectorize.proto => Should trigger deployment later
mvn -f ./transformer-service/app/pom.xml clean generate-sources
cp ./transformer-service/model/src/main/proto/vectorize.proto ./vectorizer/vectorize.proto
