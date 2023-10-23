On utilise dockerhub comme registry pour helm (dans notre cas)

# Helm package

## Handle helmchart

All files startin with \_ are treated as helpers and are available for all the templates

## Test locally detemplatized helmchart

```sh
helm install --generate-name --dry-run --debug mychart/charts/mysubchart
```

## Create a push package to Dockerhub registry

```sh
# Create helm chart boilerplate
helm create mypack

# Create tgz from chart
helm package mypack

# login to dockerhub helm registry
helm registry login registry-1.docker.io -u quentin1006

# Push chart to registry
helm push mypack-0.1.0.tgz oci://registry-1.docker.io/quentin1006
```

## Import dependency

In the Chart.yaml specify the dependency like this

```yaml
# Chart.yaml

# at root level of the yaml
dependencies:
  - name: basic-chart
    version: 0.1.0
    repository: oci://registry-1.docker.io/quentin1006
```

when specifying the dependency like helm will fetch:

oci://registry-1.docker.io/quentin1006/basic-chart:0.1.0

Then run :

```sh
helm update dependency
```

to update the charts repo with the dependencies from the `Chart.yaml`
to update values relative to specific dependency update global `values.yaml`
as follow :

```yaml
# values.yaml

# ...
# should be the exact name of imported chart
basic-chart:
  key1: value1
  # ...
```
