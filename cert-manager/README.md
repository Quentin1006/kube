## Gestionnaire de Certificats

Le gestionnaire de certificats (Cert Manager) est un module complémentaire pour Kubernetes qui automatise la gestion et l'émission des certificats TLS. Il s'intègre avec diverses autorités de certification (CAs) telles que Let's Encrypt et HashiCorp Vault pour demander, renouveler et gérer les certificats pour vos charges de travail Kubernetes.

### Comment ça fonctionne

1. **Configuration de l'Issuer/ClusterIssuer** :
   - Cert Manager utilise des ressources `Issuer` ou `ClusterIssuer` pour définir comment les certificats doivent être obtenus. Ces ressources spécifient l'autorité de certification et le mécanisme de défi (par exemple, HTTP-01, DNS-01).

2. **Demande de certificat** :
   - Une ressource `Certificate` est créée pour demander un certificat pour un domaine spécifique. Cert Manager utilise l'`Issuer` ou le `ClusterIssuer` référencé dans la ressource `Certificate` pour gérer la demande.
   - Le moyen le plus simple est d'ajouter une annotation dans la ressource Ingress pour demander automatiquement un certificat. Par exemple :
     ```yaml
     metadata:
       annotations:
         cert-manager.io/cluster-issuer: "letsencrypt-prod"
     ```

3. **Validation du défi** :
   - Pour les défis ACME (par exemple, HTTP-01 ou DNS-01), Cert Manager crée des ressources temporaires (par exemple, des pods, des ingress ou des enregistrements DNS) pour prouver la propriété du domaine à l'autorité de certification.

4. **Émission du certificat** :
   - Une fois le défi validé, l'autorité de certification émet le certificat. Cert Manager stocke le certificat dans un secret Kubernetes, qui peut ensuite être utilisé par vos applications.

5. **Renouvellement automatique** :
   - Cert Manager surveille l'expiration des certificats et les renouvelle automatiquement avant leur expiration.

### Fonctionnalités clés
- Prend en charge plusieurs autorités de certification (par exemple, Let's Encrypt, HashiCorp Vault, Venafi).
- Automatise l'émission et le renouvellement des certificats.
- Prend en charge divers mécanismes de défi (HTTP-01, DNS-01, et autres).
- S'intègre parfaitement avec les ressources Kubernetes Ingress et autres.

### Exemple d'utilisation
- Vous pouvez utiliser Cert Manager pour provisionner automatiquement des certificats TLS pour vos ressources Kubernetes Ingress, garantissant une communication sécurisée pour vos applications.

## Notes

- Dans Kind, même si un service est exposé via NodePort, il ne sera accessible que depuis le "localhost" du conteneur Docker dans lequel il se trouve.
- Pour le défi ACME HTTP-01, l'issuer doit être configuré avec une URL publique externe.

- On peut ajouter des entrées dns du dns privé du cluster en modifiant le configmap (existe t-il une solution moins invasive ?)

- En ajoutant l'option `fallthrough` dans la config dns du cluster on permet de pas bloquer le traffic sur une certaine addresse ip si le nom de domaine ne matche pas

```yaml
data:
  Corefile: |
    .:53 {
        ...
        hosts {
          # run ip route from a pod to get the ip
          10.244.0.1 public.ca-server.com
          fallthrough
        }
        ...
      }
```

Pour redémarrer coredns: 
```sh
kubectl rollout restart deployment coredns -n kube-system
```

- Le fichier resolv.conf configure la résolution DNS sur un système. Il spécifie les serveurs DNS, le parametre `ndots` permet d'indiquer au client dns de tenter de résoudre le domaine en compeltant avec tous les suffixes du parametre search si le nombre de "." dans le domaine à résoudre contient moins de points que la valeur de ndots
ex : 
search: svc.cluster
ndots: 3 
domaine à résoudre: hello.fr

Le dns tentera de résoudre hello.fr.svc.cluster

En revanche si ndots: 0

Le dns essayera uniquement de résoudre hello.fr

- Pour chaque nouveau pod créé, le plugin Network créera un `veth` sur le host du node
En lancant la commande `tcpdump -i <veth-id> -nn` sur le host on peut suivre tous les appels réseaux effectués depuis le pod

- En executant `ip netns exec <cni-id> ip addr` on peut récupérer l'ip du pod qui est associé à la cni

- Pour voir la table de routage on peut executer la commande ip route

- Décrypter un certificat : `openssl x509 -in certname.crt -text -noout`

- Ajouter un certificat sur la machine 
  ```sh
   # When decrypting the certificate, it needs to have the property CA:TRUE
   # there are multiple dest on linux depending on the distribution
   cp <certname>.crt /usr/local/share/ca-certificates
   update-ca-certificates
  ```

