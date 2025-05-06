 Installation de la csi host

https://github.com/kubernetes-csi/csi-driver-host-path/blob/master/docs/deploy-1.17-and-later.md

Derriere il faut créer manuellement la storageClass et la VolumeSnpashotClass depuis le dossier ressoures/ 

Le fichier app permet de tester que le hostpath fonctionne bien ainsi que la création de volume snapshot
Le fichier restore-pvc permet de créer un nouveau pvc avec comme source le snapshot du premùier pvc

Le snapshot standard de kubernetes est une copie à un moment précis du volume, pas de synchro pas de récurrence