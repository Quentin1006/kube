# Kubernetes operator

## Publish operator

```sh
cd ./service
docker image build -t quentin1006/op-cmi:0.2.0 service
docker image push quentin1006/op-cmi:0.2.0
```

## Run helmchart

```sh
helm upgrade -i op-cmi-helm helm --namespace custom
```

## uninstall helmchart

```sh
helm uninstall op-cmi-helm --namespace custom
```
