FROM ubuntu

RUN apt-get update && apt-get install curl iproute2 net-tools dnsutils -y

## docker run -it --rm --name=toolbox --cap-add CAP_SYS_ADMIN --cap-add NET_ADMIN --security-opt apparmor=unconfined toolbox