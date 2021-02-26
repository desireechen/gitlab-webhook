Version Service is an app deployed in OpenShift which is an enterprise Kubernetes application platform. 

# One-time Setup

## Create Helm chart with the name "updater"
This command creates a chart directory along with the common files and directories used in a Helm chart. 
```
helm create updater
```

## Create new project in OpenShift
```
oc login

oc new-project repository-update-svc --description="Repository Update Service"
oc project repository-update-svc

oc logout
```

# Local Testing
For local testing, the `Dockerfile` and `docker-compose.yml` files are required.
```
docker-compose -f docker-compose.yml up -d --build
```

# Moving to Production

## Deploy in OpenShift
Need to create a route to make the service accessible outside of OpenShift.
```
oc create -f route.yaml
oc delete route/version-service  # Optional, use this to re-create route, if required.

docker build -t registry.singapore.net/data-engineering/version-service .
docker push registry.singapore.net/data-engineering/version-service

helm install -f updater/values.yaml version-service updater --namespace=repository-update-svc
helm uninstall version-service --namespace repository-update-svc
```

Landing page: https://version-service.okd.tekong.singapore.net/docs

Request URL: https://version-service.okd.tekong.singapore.net/message

## To upgrade a release
Need to build Docker image, push it to the image registry, delete pod (so that a new pod containing Docker container with new image can start).
```
docker build -t registry.singapore.net/data-engineering/version-service .
docker push registry.singapore.net/data-engineering/version-service

oc delete pods --all

helm upgrade version-service updater
```
The last command upgrades a release `version-service` to a new version of a chart known as `updater`.

For convenience when developing service, a Bash script `Tekong.sh` has been created which contains the commands for upgrading a release. 

# Useful OpenShift commands
```
oc project
oc status
oc get routes
oc get services
oc get deployments
oc describe deployments
oc get pods
oc logs -f <name-of-pod>
oc delete pod/<name-of-pod>
```