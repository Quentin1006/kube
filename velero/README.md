# Velero

## Concepts

### Backups

On peut faire des `Backup` sur demande

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: full-cluster-backup
  namespace: velero # Velero is only watching CRs on its namespace
spec:
  includedNamespaces:
    - 'my-namespace'
  ttl: 72h0m0s
  storageLocation: default
  hooks: {}
  snapshotVolumes: false
``` 

> on peut aussi utiliser le cli `velero` depuis n'importe quel host avec un kubeconfig qui pointe vers le cluster pour faire le backup `velero backup create test-backup` 



ou via `Schedule`, le schedule va s'occuper de créer le CR Backup quand le schedule correspond

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: 0 0 * * *
  skipImmediately: false
  template:
    includedResources:
      - 
    includedNamespaces:
      - minio
    snapshotVolumes: false
    storageLocation: default
    ttl: 24h0m0s
# created by the controller
status:
  lastBackup: "2025-05-05T10:00:17Z"
  phase: Enabled
```

Par défaut, La commande backup va faire un snapshot de tous les volumes persistents pour les `includedNamespaces`, on peut l'éviter avec un `--snapshot-volumes=false` ou `snapshotVolumes: false`

Par défaut velero fait un backup complet du namespace, on peut choisir les ressources qu'on veut backuper, pour pouvoir backuper les contenus des volumes il faut avoir activé les VolumeSnapshot ainsi qu'un VolumeSnapshotLocationet avoir activé la propriété snapshotVolumes



#### BackupStorageLocation



## Notes

Pour configurer velero avec un minio (accessible à l'intéreiur du cluster ou via ingress) on doit utiliser le provider aws et les aws_credentials doivent matcher les logins minio