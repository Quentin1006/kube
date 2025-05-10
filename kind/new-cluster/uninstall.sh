# Ensure the script is run with exactly 1 argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 cluster_name" >&2
  exit 1
fi

cluster_name="$1"

kind delete cluster --name "$cluster_name"