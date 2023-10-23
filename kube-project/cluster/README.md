## Generate TLS certificate

```sh
mkdir certs 
openssl req -x509 -newkey rsa:4096 -days 365 -nodes -sha256 -keyout certs/tls.key -out certs/tls.crt -subj "/CN=docker-registry" -addext "subjectAltName = DNS:docker-registry"

mkdir auth
# Remplacer myuser mypasswd par le couple login/pwd
docker run --rm --entrypoint htpasswd registry:2.6.2 -Bbn myuser mypasswd > auth/htpasswd
```

## Create secret containing certificate

```sh
# create secret of type tls containing tls cert
kubectl create secret tls certs-secret --cert=./certs/tls.crt --key=./certs/tls.key

# create secret containing htpasswd file to store creds
kubectl create secret generic auth-secret --from-file=./auth/htpasswd
```

## Docker network system

### 3 types of networks 

1. none :  container is not reachable and cannot reach the outside
2. host : the container is on the same neywork than the host so it gets the same ip, this means if you start 2 nginx container with network=host, only one can start on port 80, since they share the same ip
3. bridge : A subnet is created, and every container that are on the same subnet can communicate with each other. there is one setup by default by docker but we can create as many as we want of type bridge. The container gets its own ip within the subnet 


### Routing Table

```sh
# route PRINT (powershell)
route -n
```

Exemple :

Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.18.0.1      0.0.0.0         UG    0      0        0 eth0
172.18.0.0      0.0.0.0         255.255.0.0     U     0      0        0 eth0

Destination + Genmask = range of ip address to reach
Gateway is the way to reach this range of ip, 0.0.0.0 for Gateway means they can be accessed directly with ip 

### DNS

Point to a DNS server

```sh
cat /etc/resolv.conf
```
nameserver 192.168.1.100
search mycompany.com prod.mycompany.com

search is added to the name that we are trying to reach

if we type ping web it will resolve to ping web.mycompany.web. We can set multiple search at once, resolver will try all of them

nslookup allows us to resolve name, nslookup only query the dns server not the /etc/hosts


## Network namespaces

To create network interfaces

1. Create network namespace
2. Create bridge network interface
3. Create vEth Pairs
4. Attach vEth to namespace
5. Attach vEth-br to Bridge
6. Assign ip addresses
7. Bring the interfaces up
8. Enable NAT - IP Masquerade  


```sh
# Create network namespaces
ip netns add red
ip netns add blue

# Check the interfaces on host
ip link

# check the interfaces on a namespace
ip netns exec red ip link

## Create a switch interface of type bridge
## When created it is down 
ip link add v-net-0 type bridge
## to bring it up
ip link set dev v-net-0 up

## to link the red namespace to the switch
## create the interface for red namespace 
ip link add veth-red type veth peer name veth-red-br
## interfaces are first created on the host, we move it to the namespace
ip link set veth-red netns red
## and the interface related on the switch on the host
ip link set veth-red-br master v-net-0

## assign an ip to the network interface
ip -n red addr add 192.168.15.1/24 dev veth-red

## turn the network interfaces up
ip -n red link set veth-red up
ip link set veth-red-br up

## To ba able to ping the namespace from the host we need to assign an ip to the switch
ip addr add 192.168.15.5/24 dev v-net-0

## Otherwise we should be able to communicate between 2 namespaces on the same v-net

## to forward a request on the host to a network namespace, assuming host ip is 172.17.0.3
## and network namespace has ip 192.168.1.3 in the bridge network
## We add an entry in the routing table we forward the request from a port on the host to the namespace
## A request to 172.17.0.3:8080 will be forwarded to 192.168.1.3:80
## For docker it looks like this :

iptables -t nat -A DOCKER -j DNAT --dport 8080 --to-destination 192.168.1.3:80 

```

CNI = Standard for creating network interfaces for containers


