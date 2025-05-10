#!/bin/bash

# Replace relative paths with absolute paths
script_dir="$(dirname "$0")"

# Parse CLI arguments
if [ "$#" -lt 3 ]; then
  echo "Usage: $0 -c config_path cluster_name" >&2
  exit 1
fi

while [[ "$1" == "-c" || "$1" == "--config" ]]; do
  case "$1" in
    -c|--config)
      config_path="$2"
      shift 2
      ;;
    *)
      echo "Usage: $0 -c config_path cluster_name" >&2
      exit 1
      ;;
  esac
done

cluster_name="$1"

if [ -z "$config_path" ]; then
  echo "Error: Config path is required. Use -c or --config to specify the config path." >&2
  exit 1
fi

if [ -z "$cluster_name" ]; then
  echo "Error: Cluster name is required." >&2
  exit 1
fi

# Convert config path to absolute path
config_path="$(realpath "$config_path")"

echo "Creating cluster with name: $cluster_name"
echo "Using config file: $config_path"

kube_namespace="kube-system"

if ! kind create cluster --name "$cluster_name" --config "$config_path"; then
  echo "Error: Failed to create cluster." >&2
  exit 1
fi

kubectl cluster-info --context kind-$cluster_name

# Add hosts to the coredns
kubectl patch configmap coredns -n $kube_namespace --type merge --patch "$(cat "$script_dir/coredns-patch.yaml")"
kubectl rollout restart deployment coredns -n $kube_namespace

NODE_NAME=$(kind get nodes --name $cluster_name | head -n 1)
docker exec "$NODE_NAME" bash -c "echo '127.0.0.1 prometheus.local public.ca-server.com backup-storage.local' >> /etc/hosts"

# Install the ingress controller
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml

# Wait for the ingress controller to be ready
sleep 15

helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add longhorn https://charts.longhorn.io
helm repo update 

# install csi
# install hostpath csi driver (not fully compatible with velero)
# chmod +x "$script_dir/hostpath/install-hostpath.sh"
# "$script_dir/hostpath/install-hostpath.sh"

# install longhorn csi driver
# longhorn block storage arch is not compatible with docker container (so not compatible with kind)
# helm upgrade -i longhorn longhorn/longhorn \
#   --namespace longhorn-system \
#   -f "$script_dir/longhorn/longhorn-values.yaml" \
#   --create-namespace \
#   --wait
# kubectl apply -f longhorn/longhorn-volume-snapshot-class.yaml


# Install velero
helm upgrade -i minio bitnami/minio \
  --namespace velero \
  -f "$script_dir/velero/minio-values.yaml" \
  --create-namespace

helm upgrade -i velero vmware-tanzu/velero \
  --namespace velero \
  --set-file credentials.secretContents.cloud="$script_dir/velero/credentials-velero" \
  -f "$script_dir/velero/velero-values.yaml" \
  --create-namespace 

# Install prometheus
helm upgrade -i prometheus bitnami/kube-prometheus \
  --namespace monitoring \
  -f "$script_dir/monitoring/prometheus-values.yaml" \
  --create-namespace



