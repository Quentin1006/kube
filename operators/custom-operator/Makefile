# build and publish
bap:
	docker image build -t quentin1006/op-cmi:${TAG} ./service
	docker image push quentin1006/op-cmi:${TAG}

# helm upgrade
hup: hun
	helm upgrade -i custop helm

hun:
	helm uninstall custop


# clear cluster from CR cmi and config map
cc:
	kubectl delete cm/op-cmi-cr --ignore-not-found=true
	kubectl delete cm/op-cmi-cr2 --ignore-not-found=true
	kubectl delete cmi/op-cmi-cr --ignore-not-found=true
	kubectl delete cmi/op-cmi-cr2 --ignore-not-found=true

# apply CR cmi
acr: cc
	kubectl apply -f exemples/op-cmi-cr.yml

acr2: cc
	kubectl apply -f exemples/op-cmi-cr2.yml 

test:
	@echo ${TAG}

all: bap cc huzzzzzzzzzzzzzzz

