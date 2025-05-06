# README

## Sources 

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-minikube-raft

## Vault Service

### Install the Vault Helm chart

```sh
# Add the HashiCorp Helm repository
helm repo add hashicorp https://helm.releases.hashicorp.com

# Update all the repositories to ensure helm is aware of the latest versions.
helm repo update

# Install the latest version of the Vault Helm chart with Integrated Storage.
helm dependency update vault-service
helm upgrade -i vault-service vault-service

``` 


### Intialize vault pods


```sh
kubectl exec vault-service-0 -- vault operator init \
    -key-shares=1 \
    -key-threshold=1 \
    -format=json > cluster-keys.json

```

The operator init command generates a root key that it disassembles into key shares -key-shares=1 and then sets the number of key shares required to unseal Vault -key-threshold=1. These key shares are written to the output as unseal keys in JSON format -format=json. Here the output is redirected to a file named cluster-keys.json.


```sh
# Create a variable named VAULT_UNSEAL_KEY to capture the Vault unseal key.
VAULT_UNSEAL_KEY=$(jq -r ".unseal_keys_b64[]" cluster-keys.json)
```

After initialization, Vault is configured to know where and how to access the storage, but does not know how to decrypt any of it. Unsealing is the process of constructing the root key necessary to read the decryption key to decrypt the data, allowing access to the Vault.

```sh
# Unseal Vault running on the vault-0 pod.
kubectl exec vault-service-0 -- vault operator unseal $VAULT_UNSEAL_KEY
``` 


Get the secret associated to a path in vault
token is the rootToken generated from the `cluster-keys.json`

```sh
curl --header "X-Vault-Token: <token>" http://vault.local/v1/my-app/data/main
```

## Vault Secret Operator

```sh
helm repo add hashicorp https://helm.releases.hashicorp.com

helm repo update


```