Version Service is an app deployed in OpenShift which is an enterprise Kubernetes application platform. The service, built using FastAPI, receives a GitLab webhook, processes the webhook and sends messages to a Request Bin. 

<img width="900" alt="fastapi" src="https://user-images.githubusercontent.com/51873343/109282353-61e84800-7858-11eb-9a98-f29d6fc6521e.PNG">

POST messages in Request Bin.

<img width="300" alt="requestbin" src="https://user-images.githubusercontent.com/51873343/109282584-ad025b00-7858-11eb-95df-afeb11a8e5e1.PNG">

## One-time Setup

### Create Helm chart with the name "updater"
This command creates a chart directory along with the common files and directories used in a Helm chart. 
```
helm create updater
```

### Create new project in OpenShift
```
oc login

oc new-project repository-update-svc --description="Repository Update Service"
oc project repository-update-svc

oc logout
```

## Local Testing
For local testing, the `Dockerfile` and `docker-compose.yml` files are required.
```
docker-compose -f docker-compose.yml up -d --build
```

## Moving to Production

### Deploy in OpenShift
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

### To upgrade a release
Need to build Docker image, push it to the image registry, delete pod (so that a new pod containing Docker container with new image can start).
```
docker build -t registry.singapore.net/data-engineering/version-service .
docker push registry.singapore.net/data-engineering/version-service

oc delete pods --all

helm upgrade version-service updater
```
The last command upgrades a release `version-service` to a new version of a chart known as `updater`.

For convenience when developing service, a Bash script `Tekong.sh` has been created which contains the commands for upgrading a release. 

Below is a screenshot of the Kubernetes extension in VS code. Deployment 20 supersedes previous versions of the deployment. 

<img width="530" alt="kubernetes_extension" src="https://user-images.githubusercontent.com/51873343/109409318-caf0cc80-79cc-11eb-8bb1-1109a17a627c.PNG">

## Useful OpenShift commands
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
