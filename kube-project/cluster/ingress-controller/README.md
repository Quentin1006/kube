# Ingress Controller

## Install NGINX ingress controller

[See source exemple](https://github.com/marcel-dempers/docker-development-youtube-series/tree/master/kubernetes/ingress/controller/nginx)
```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
# Check available version with CHART and APP versions
helm search repo ingress-nginx --versions

# Make sure it is compatible with kubernetes version 
# and it will too be compatible with next kube versions
CHART_VERSION="4.8.1"
APP_VERSION="1.9.1"

# In working dir
mkdir manifests && cd manifests
# Get locally the content of the manifests to install the helm chart
helm template ingress-nginx ingress-nginx \
--repo https://kubernetes.github.io/ingress-nginx \
--version ${CHART_VERSION} \
--namespace ingress-nginx \
> ./nginx-ingress.${APP_VERSION}.yaml
 
kubectl create namespace ingress-nginx
kubectl apply -f ./nginx-ingress.${APP_VERSION}.yaml

# Map traffic from port 9000 on our machine to 80 on kubernetes  through service svc/ingress-nginx-controller
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 443:9000

```
