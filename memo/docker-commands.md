# Commandes Docker et Docker Compose - Référence rapide

Ce fichier centralise toutes les commandes Docker utiles pour le projet OC Lettings.

---

## Table des matières
1. [Vérification de l'installation](#1-vérification-de-linstallation)
2. [Gestion des images](#2-gestion-des-images)
3. [Gestion des conteneurs](#3-gestion-des-conteneurs)
4. [Docker Compose](#4-docker-compose)
5. [Logs et débogage](#5-logs-et-débogage)
6. [Docker Hub](#6-docker-hub)
7. [Nettoyage](#7-nettoyage)
8. [Commandes spécifiques au projet](#8-commandes-spécifiques-au-projet)

---

## 1. Vérification de l'installation

```bash
# Vérifier la version de Docker
docker --version

# Vérifier la version de Docker Compose
docker-compose --version

# Vérifier que Docker fonctionne
docker run hello-world
```

---

## 2. Gestion des images

### Lister les images

```bash
# Lister toutes les images locales
docker images

# Lister avec filtrage
docker images | grep oc-lettings
```

### Construire une image

```bash
# Construire depuis le Dockerfile du dossier courant
docker build -t oc-lettings .

# Construire avec un tag spécifique
docker build -t sebgris/oc-lettings:latest .

# Construire avec plusieurs tags
docker build -t sebgris/oc-lettings:latest -t sebgris/oc-lettings:v1.0 .

# Construire sans utiliser le cache (rebuild complet)
docker build --no-cache -t oc-lettings .
```

### Télécharger/Pousser une image

```bash
# Télécharger une image depuis Docker Hub
docker pull sebgris/oc-lettings:latest

# Télécharger l'image Python officielle
docker pull python:3.13-slim
```

### Supprimer une image

```bash
# Supprimer une image par nom
docker rmi oc-lettings

# Supprimer une image par ID
docker rmi abc123

# Forcer la suppression (même si utilisée par un conteneur arrêté)
docker rmi -f oc-lettings
```

### Tagger une image

```bash
# Ajouter un tag à une image existante
docker tag oc-lettings sebgris/oc-lettings:latest

# Tagger avec le hash du commit
docker tag oc-lettings sebgris/oc-lettings:abc1234
```

---

## 3. Gestion des conteneurs

### Lister les conteneurs

```bash
# Conteneurs en cours d'exécution
docker ps

# Tous les conteneurs (y compris arrêtés)
docker ps -a

# Format personnalisé
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Créer et lancer un conteneur

```bash
# Lancer en mode détaché (arrière-plan)
docker run -d -p 8000:8000 --name oc-lettings-app oc-lettings

# Lancer avec des variables d'environnement
docker run -d -p 8000:8000 --name oc-lettings-app \
  -e SECRET_KEY=ma-cle-secrete \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  oc-lettings

# Lancer avec un volume (persistance des données)
# ⚠️ ATTENTION: Sur Windows, le montage de volumes SQLite peut causer
# l'erreur "attempt to write a readonly database". Dans ce cas,
# n'utilisez pas l'option -v et utilisez la base incluse dans l'image.
docker run -d -p 8000:8000 --name oc-lettings-app \
  -e SECRET_KEY=ma-cle-secrete \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  -v ./oc-lettings-site.sqlite3:/app/oc-lettings-site.sqlite3 \
  oc-lettings

# Lancer en mode interactif (pour debug)
docker run -it --rm oc-lettings bash
```

**Note Windows CMD** : Remplacer `\` par `^` ou tout mettre sur une seule ligne.

### Arrêter/Démarrer un conteneur

```bash
# Arrêter un conteneur
docker stop oc-lettings-app

# Démarrer un conteneur arrêté
docker start oc-lettings-app

# Redémarrer un conteneur
docker restart oc-lettings-app
```

### Supprimer un conteneur

```bash
# Supprimer un conteneur arrêté
docker rm oc-lettings-app

# Forcer la suppression (même s'il tourne)
docker rm -f oc-lettings-app

# Supprimer tous les conteneurs arrêtés
docker container prune
```

### Exécuter une commande dans un conteneur

```bash
# Ouvrir un shell bash dans le conteneur
docker exec -it oc-lettings-app bash

# Exécuter une commande Django
docker exec oc-lettings-app python manage.py migrate

# Voir les variables d'environnement
docker exec oc-lettings-app env
```

---

## 4. Docker Compose

### Lancer les services

```bash
# Lancer tous les services définis dans docker-compose.yml
docker-compose up

# Lancer en arrière-plan (mode détaché)
docker-compose up -d

# Reconstruire l'image avant de lancer
docker-compose up --build

# Reconstruire et lancer en arrière-plan
docker-compose up --build -d
```

### Arrêter les services

```bash
# Arrêter les services (garde les conteneurs)
docker-compose stop

# Arrêter et supprimer les conteneurs
docker-compose down

# Arrêter, supprimer conteneurs ET volumes
docker-compose down -v
```

### Reconstruire

```bash
# Reconstruire sans cache
docker-compose build --no-cache

# Reconstruire un service spécifique
docker-compose build web
```

### Autres commandes utiles

```bash
# Voir le statut des services
docker-compose ps

# Voir les logs de tous les services
docker-compose logs

# Suivre les logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f web

# Exécuter une commande dans un service
docker-compose exec web python manage.py shell
```

---

## 5. Logs et débogage

### Voir les logs

```bash
# Logs d'un conteneur
docker logs oc-lettings-app

# Suivre les logs en temps réel
docker logs -f oc-lettings-app

# Afficher les 100 dernières lignes
docker logs --tail 100 oc-lettings-app

# Logs avec timestamps
docker logs -t oc-lettings-app
```

### Inspecter un conteneur

```bash
# Informations détaillées sur un conteneur
docker inspect oc-lettings-app

# Voir l'adresse IP du conteneur
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' oc-lettings-app

# Voir les variables d'environnement
docker inspect -f '{{.Config.Env}}' oc-lettings-app
```

### Statistiques

```bash
# Utilisation CPU/mémoire en temps réel
docker stats

# Stats d'un conteneur spécifique
docker stats oc-lettings-app
```

### Vérifier l'OS d'une image

```bash
# Voir sur quel OS est basée une image
docker run --rm python:3.13-slim cat /etc/os-release
```

---

## 6. Docker Hub

### Authentification

```bash
# Se connecter à Docker Hub
docker login

# Se déconnecter
docker logout
```

### Pousser une image

```bash
# 1. S'assurer que l'image est taguée avec votre username
docker tag oc-lettings sebgris/oc-lettings:latest

# 2. Pousser l'image
docker push sebgris/oc-lettings:latest

# Pousser tous les tags d'une image
docker push sebgris/oc-lettings --all-tags
```

### Télécharger une image

```bash
# Télécharger la dernière version
docker pull sebgris/oc-lettings:latest

# Télécharger une version spécifique
docker pull sebgris/oc-lettings:abc1234
```

---

## 7. Nettoyage

### Supprimer les ressources inutilisées

```bash
# Supprimer les conteneurs arrêtés
docker container prune

# Supprimer les images non utilisées (dangling)
docker image prune

# Supprimer TOUTES les images non utilisées
docker image prune -a

# Supprimer les volumes non utilisés
docker volume prune

# Supprimer les réseaux non utilisés
docker network prune
```

### Nettoyage complet

```bash
# Supprimer tout ce qui n'est pas utilisé (attention !)
docker system prune

# Inclure les volumes (attention aux données !)
docker system prune --volumes

# Supprimer absolument tout (images, conteneurs, volumes, réseaux)
docker system prune -a --volumes
```

### Voir l'espace utilisé

```bash
# Espace disque utilisé par Docker
docker system df

# Vue détaillée
docker system df -v
```

---

## 8. Commandes spécifiques au projet

### Workflow complet de développement

```bash
# 1. Lancer l'application avec Docker Compose
docker-compose up --build -d

# 2. Vérifier que ça fonctionne
curl http://localhost:8000

# 3. Voir les logs si problème
docker-compose logs -f

# 4. Arrêter quand terminé
docker-compose down
```

### Workflow pour pousser sur Docker Hub

```bash
# 1. Se connecter
docker login

# 2. Construire avec le bon tag
docker build -t sebgris/oc-lettings:latest .

# 3. Pousser
docker push sebgris/oc-lettings:latest

# 4. (Optionnel) Ajouter un tag avec le hash du commit
git rev-parse --short HEAD  # Récupérer le hash, ex: abc1234
docker tag sebgris/oc-lettings:latest sebgris/oc-lettings:abc1234
docker push sebgris/oc-lettings:abc1234
```

### Lancer sans Docker Compose

```bash
# Supprimer l'ancien conteneur si existe
docker rm -f oc-lettings-app

# Lancer le conteneur (sans volume - recommandé sur Windows)
docker run -d -p 8000:8000 --name oc-lettings-app \
  -e SECRET_KEY=votre-cle-secrete \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  sebgris/oc-lettings:latest

# ⚠️ Note: L'option -v pour monter la base SQLite est déconseillée sur Windows
# car elle peut causer l'erreur "attempt to write a readonly database"

# Accéder à http://localhost:8000
```

---

## Tableau récapitulatif des commandes les plus utilisées

| Action | Commande |
|--------|----------|
| Lancer l'app | `docker-compose up -d` |
| Lancer avec rebuild | `docker-compose up --build -d` |
| Arrêter l'app | `docker-compose down` |
| Voir les logs | `docker-compose logs -f` |
| Voir les conteneurs | `docker ps` |
| Construire l'image | `docker build -t oc-lettings .` |
| Pousser sur Docker Hub | `docker push sebgris/oc-lettings:latest` |
| Entrer dans le conteneur | `docker exec -it oc-lettings-web bash` |
| Nettoyer tout | `docker system prune -a` |
