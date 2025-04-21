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