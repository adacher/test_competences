# Test de compétences

Versions utilisées

Docker
```
Client: Docker Engine - Community
 Cloud integration: 1.0.12
 Version:           20.10.5
 API version:       1.41
 Go version:        go1.13.15
 Git commit:        55c4c88
 Built:             Tue Mar  2 20:13:00 2021
 OS/Arch:           darwin/amd64
 Context:           default
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          20.10.12
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.16.12
  Git commit:       459d0df
  Built:            Mon Dec 13 11:46:12 2021
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v1.4.12
  GitCommit:        7b11cfaabd73bb80907dd23182b9347b4245eb5d
 runc:
  Version:          1.0.2
  GitCommit:        52b36a2dd837e8462de8e01458bf02cf9eea47dd
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

Minikube
```
minikube version: v1.25.2
commit: 362d5fdc0a3dbee389b3d3f1034e8023e72bd3a7
```
Kubectl
```
Client Version: version.Info{Major:"1", Minor:"23", GitVersion:"v1.23.4", GitCommit:"e6c093d87ea4cbb530a7b2ae91e54c0842d8308a", GitTreeState:"clean", BuildDate:"2022-02-16T12:30:48Z", GoVersion:"go1.17.6", Compiler:"gc", Platform:"darwin/amd64"}
Server Version: version.Info{Major:"1", Minor:"23", GitVersion:"v1.23.3", GitCommit:"816c97ab8cff8a1c72eccca1026f7820e93e0d25", GitTreeState:"clean", BuildDate:"2022-01-25T21:19:12Z", GoVersion:"go1.17.6", Compiler:"gc", Platform:"linux/amd64"}
```

Terraform
```
Terraform v1.1.6
on darwin_amd64
```

Helm
```
version.BuildInfo{Version:"v3.8.0", GitCommit:"d14138609b01886f544b2025f5000351c9eb092e", GitTreeState:"clean", GoVersion:"go1.17.6"}
```

Virtualbox
```
Oracle VM VirtualBox VM Selector v6.1.32
```


------------------------------------------------------------------------------------------


**Walkthrough : Deploiement kubernetes**

Initialisation du cluster k8s via minikube via virtualbox.
```
minikube start --driver=virtualbox
```

Activation de l'addon ingress.
```
minikube addons enable ingress
```

Vérifier le context kubectl, il faut obtenir minikube.
```
kubectl config current-context
minikube

Si minikube n'est pas affiché, lancer la commande :
kubectl config use-context minikube
```

Paramètrage du shell, pour que minikube et docker partagent le même environnement.
Sans cela, il n'est pas possible de récupérer les images docker lors du deploiement.
```
eval $(minikube -p minikube docker-env)
```

Élévation des droits sur les fichiers entypoints.sh .
```
chmod +x flask-premier/entrypoint.sh
chmod +x flask-random/entrypoint.sh
```

Création des images Docker.
```
make build
```

Initialisation de terraform puis création de l'environnement kubernetes demandé.
```
cd terraform
terraform init
terraform apply -var-file="terraform.tfvars"
```

Premier déploiement des services via Helm.
```
cd ..
helm install "entrytestchart" helm-deployment/ -f helm-deployment/values.yaml --set timestamp="`date +'%s'`"
```

Une fois le déploiement effectué :
```
kubectl get ingress -n namespace-test
Copier la valeur de l'addresse IP affichée en de dessous de ADDRESS.
(L'adresse met quelques secondes a se génerer, relancer la commande jusqu'a ce qu'elle soit affichée).
Ouvrir le fichier /etc/hosts avec les droits roots (ex : sudo vim /etc/hosts).
# Écrire à la dernière ligne:
IP_ADDRESS entry-test.info
```

**Test des routes :**

Pod contenant la route premier  :

```
curl entry-test.info:30000/premier
curl entry-test.info:30000/premier?number=10
curl entry-test.info:30000/health
curl entry-test.info:30000/ping
curl entry-test.info:30000/metrics
```

Pod contenant la route random :
```
curl entry-test.info:30001/random
curl entry-test.info:30001/health
curl entry-test.info:30001/ping
curl entry-test.info:30001/metrics
```

Vérification des propriétés du namespace :
```
kubectl describe namespace  namespace-test
```

Vérification des déploiements :
```
kubectl get deployments -n namespace-test
kubectl describe deployment <deployment-name> -n namespace-test
```

Vérification de l'ingress :
```
kubectl get ingress -n namespace-test
ubectl describe ingress <ingress-name> -n namespace-test
```

Vérification des services :
```
kubectl get services -n namespace-test
kubectl describe service <service-name> -n namespace-test
```

Vérification des pods :
```
kubectl get pods -n namespace-test 
kubectl describe pod <pod-name> -n namespace-test
```

Vérification de la configMap :
```
kubectl get configMap -n namespace-test 
kubectl describe configMap <configMap-name> -n namespace-test
```

À utiliser pour re-déloyer les applications si besoin :
```
helm upgrade "entrytestchart" helm-deployment/ -f helm-deployment/values.yaml --set timestamp="`date +'%s'`"
```


**Walkthrough : Déploiement local, uniquement via Docker.**

Ouvrir un nouveau terminal, pour éviter un conflit de ports entre un service k8s par défaut et le nginx-proxy.

Élévation des droits sur les fichiers entypoints.sh (Si pas déjà fait).
```
chmod +x flask-premier/entrypoint.sh
chmod +x flask-random/entrypoint.sh
```

Construction des images et démarrage des containers.
Il faut accepter la création d'un network par défaut lorsque demandé par docker. (écrire yes).
```
make
```

Test api Premier :
```
curl localhost:33330/premier
curl localhost:33330/premier?number=10
curl localhost:33330/health
curl localhost:33330/ping
curl localhost:33330/metrics
```

Test api Random :
```
curl localhost:44440/random
curl localhost:44440/health
curl localhost:44440/ping
curl localhost:44440/metrics
```

**Débug :**

Si le container flask-random n'arrive pas a joindre la route /premier du container flask-premier, vérifier si les containers partagent le même réseau :
```
docker inspect -f '{{range $key, $value := .NetworkSettings.Networks}}{{$key}} {{end}}' flask-random
docker inspect -f '{{range $key, $value := .NetworkSettings.Networks}}{{$key}} {{end}}' flask-premier
docker inspect -f '{{range $key, $value := .NetworkSettings.Networks}}{{$key}} {{end}}' nginx-proxy
```




