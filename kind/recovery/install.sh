kube_namespace="kube-system"

kind create cluster --name recovery --config ./config.yaml

kubectl cluster-info --context kind-recovery

# Add hosts to the coredns
kubectl patch configmap coredns -n $kube_namespace --type merge --patch "$(cat coredns-patch.yaml)"
kubectl rollout restart deployment coredns -n $kube_namespace


NODE_NAME=$(kind get nodes --name my-cluster | head -n 1)
docker exec "$NODE_NAME" bash -c "echo '127.0.0.1 prometheus.local public.ca-server.com backup-storage.local' >> /etc/hosts"

# Install the ingress controller
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml

# install csi
chmod +x ./install-hostpath.sh
./install-hostpath.sh


# Install velero
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update 

helm upgrade -i minio bitnami/minio \
  --namespace velero \
  -f ./velero/minio-values.yaml \
  --create-namespace

helm upgrade -i velero vmware-tanzu/velero \
  --namespace velero \
  --set-file credentials.secretContents.cloud=./velero/credentials-velero \
  -f ./velero/velero-values.yaml \
  --create-namespace 


# Install prometheus
helm upgrade -i prometheus bitnami/kube-prometheus \
  --namespace monitoring \
  -f ./monitoring/prometheus-values.yaml \
  --create-namespace



