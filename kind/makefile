create-basic:
	cd clusters/basic && ../../new-cluster/install.sh --config ./config.yaml basic

delete-basic:
	cd clusters/basic && ../../new-cluster/uninstall.sh basic

cb: create-basic
db: delete-basic

create-recovery:
	cd clusters/recovery && ../../new-cluster/install.sh --config ./config.yaml recovery

delete-recovery:
	cd clusters/recovery && ../../new-cluster/uninstall.sh recovery

cr: create-recovery
dr: delete-recovery
