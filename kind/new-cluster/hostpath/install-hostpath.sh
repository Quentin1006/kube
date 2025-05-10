script_dir="$(dirname "$0")"
SNAPSHOTTER_BRANCH=release-6.3
SNAPSHOTTER_VERSION=v6.3.3

kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/$SNAPSHOTTER_BRANCH/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/$SNAPSHOTTER_BRANCH/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/$SNAPSHOTTER_BRANCH/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml

kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/$SNAPSHOTTER_VERSION/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/$SNAPSHOTTER_VERSION/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml

chmod +x $script_dir/hostpath/deploy.sh
$script_dir/hostpath/deploy.sh

kubectl apply -f $script_dir/hostpath/storage-class.yaml
kubectl apply -f $script_dir/hostpath/volume-snapshot-class.yaml