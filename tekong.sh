#! /bin/bash
docker build -t registry.singapore.net/data-engineering/version-service .
docker push registry.singapore.net/data-engineering/version-service

oc delete pods --all

helm upgrade version-service updater