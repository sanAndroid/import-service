
IMAGE_NAME=vectorizer:latest
DEPLOYMENT_YAML=vectorizer.yaml

# Use Minikube's Docker daemon
use-minikube-docker:
	eval $$(minikube -p minikube docker-env)

# Build inside Minikube
build:
	eval $$(minikube -p minikube docker-env) && docker build -t $(IMAGE_NAME) .

# Apply the deployment to cluster
deploy:
	kubectl apply -f $(DEPLOYMENT_YAML)

# Rebuild and redeploy
redeploy: build deploy

# Reset docker env to local
reset-docker-env:
	eval $$(minikube docker-env -u)
