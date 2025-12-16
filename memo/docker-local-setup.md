# Guide de démarrage Docker en local - OC Lettings

## Table des matières
1. [Prérequis](#1-prérequis)
2. [Générer une SECRET_KEY](#2-générer-une-secret_key)
3. [Configurer les variables d'environnement](#3-configurer-les-variables-denvironnement)
4. [Comprendre le flux de la SECRET_KEY](#4-comprendre-le-flux-de-la-secret_key)
5. [Construire et lancer l'image Docker](#5-construire-et-lancer-limage-docker)
6. [Commandes utiles](#6-commandes-utiles)
7. [Dépannage](#7-dépannage)
8. [Pusher l'image sur Docker Hub](#8-pusher-limage-sur-docker-hub)

---

## 1. Prérequis

### Installer Docker Desktop

1. Télécharger Docker Desktop : https://www.docker.com/products/docker-desktop/
2. Installer et redémarrer si nécessaire
3. Lancer Docker Desktop depuis le menu Démarrer
4. Attendre que l'icône Docker dans la barre des tâches soit verte (prêt)

### Vérifier l'installation

```bash
docker --version
docker-compose --version
```

---

## 2. Générer une SECRET_KEY

La `SECRET_KEY` est une clé secrète utilisée par Django pour :
- Signer les cookies de session
- Générer des tokens CSRF
- Autres opérations cryptographiques

**IMPORTANT** : Ne jamais partager ou commiter cette clé !

### Méthode 1 : Avec Python (recommandée)

Ouvrez un terminal et exécutez :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Résultat exemple** :
```
a3b$k9#mz!x@4p^q8w2&f5n7j0*c1v6y
```

### Méthode 2 : Avec Python (sans Django)

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Méthode 3 : Générateur en ligne

Utilisez un générateur comme : https://djecrety.ir/

---

## 3. Configurer les variables d'environnement

### Où mettre la SECRET_KEY ?

Il y a **deux options** selon comment vous lancez Docker :

---

### Option A : Fichier `.env` (recommandé pour le développement)

Le fichier `.env` est à la racine du projet. Il contient les variables d'environnement locales.

**Emplacement** : `d:\Users\sebas\Documents\VS Code\OpenClassrooms\project-13 Python-OC-Lettings-FR\.env`

**Contenu du fichier `.env`** :
```env
# Django settings
SECRET_KEY=votre-cle-secrete-generee-ici
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Sentry (optionnel)
SENTRY_DSN=
SENTRY_ENVIRONMENT=development
```

**Exemple avec une vraie clé** :
```env
SECRET_KEY=a3b$k9#mz!x@4p^q8w2&f5n7j0*c1v6y
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Note** : Le fichier `.env` est ignoré par Git (listé dans `.gitignore`) pour ne pas exposer vos secrets.

---

### Option B : Variables d'environnement directes (pour Docker run)

Si vous utilisez `docker run` directement, passez les variables avec `-e` :

```bash
docker run -d -p 8000:8000 \
  -e SECRET_KEY=votre-cle-secrete \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  oc-lettings
```

---

## 4. Comprendre le flux de la SECRET_KEY

### C'est la même SECRET_KEY partout ?

**Oui !** C'est la même variable Django. Docker ne fait que la **transmettre** au conteneur.

### Le flux de la SECRET_KEY

```
.env (fichier local)
    │
    ▼
docker-compose.yml (lit .env automatiquement)
    │
    ▼
Conteneur Docker (variable d'environnement)
    │
    ▼
Django settings.py (utilise la variable)
    │
    SECRET_KEY = os.environ.get("SECRET_KEY")
```

### Où est définie la SECRET_KEY selon l'environnement ?

| Environnement | Fichier | Valeur |
|---------------|---------|--------|
| **Développement local** | `.env` | Votre clé générée |
| **Tests CI (GitHub Actions)** | `ci-cd.yml` | `test-secret-key-for-ci` (temporaire) |
| **Production (Render)** | Secrets Render | Clé de production (jamais dans le code) |

### Pourquoi une valeur différente dans ci-cd.yml ?

```yaml
env:
  SECRET_KEY: test-secret-key-for-ci
```

C'est une clé **temporaire** uniquement pour les tests automatisés. Elle est visible dans le code mais ce n'est pas grave car :
- Les tests ne sont pas en production
- La vraie clé de production est stockée dans les secrets Render (jamais dans le code)

### Résumé

- **Docker/Docker Compose** : Ne crée pas de SECRET_KEY, il la **transmet** seulement
- **Django** : C'est lui qui **utilise** la SECRET_KEY
- **Même variable** : Partout c'est `SECRET_KEY`, seule la **valeur** change selon l'environnement

---

## 5. Construire et lancer l'image Docker

### Méthode 1 : Avec Docker Compose (simple)

C'est la méthode la plus simple car elle utilise automatiquement le fichier `.env`.

```bash
# Se placer dans le dossier du projet
cd "d:\Users\sebas\Documents\VS Code\OpenClassrooms\project-13 Python-OC-Lettings-FR"

# Construire et lancer
docker-compose up --build
```

**Explications** :
- `up` : Démarre les services définis dans `docker-compose.yml`
- `--build` : Reconstruit l'image avant de lancer (utile après des modifications)

**Pour lancer en arrière-plan** :
```bash
docker-compose up --build -d
```

**Pour arrêter** :
```bash
docker-compose down
```

---

### Méthode 2 : Avec Docker directement

#### Étape 1 : Construire l'image

```bash
docker build -t oc-lettings .
```

**Explications** :
- `build` : Construit une image à partir du Dockerfile
- `-t oc-lettings` : Nomme l'image "oc-lettings"
- `.` : Utilise le Dockerfile du dossier courant

```bash
# Vérifier que l'image est créée
docker images
```

#### Étape 2 : Lancer le conteneur

**Sur Windows (CMD)** :
```cmd
docker run -d -p 8000:8000 --name oc-lettings-app -e SECRET_KEY=votre-cle-secrete -e DEBUG=False -e ALLOWED_HOSTS=localhost,127.0.0.1 oc-lettings
```

**Sur Windows (PowerShell)** :
```powershell
docker run -d -p 8000:8000 `
  --name oc-lettings-app `
  -e SECRET_KEY=votre-cle-secrete `
  -e DEBUG=False `
  -e ALLOWED_HOSTS=localhost,127.0.0.1 `
  oc-lettings
```

**Explications** :
- `-d` : Mode détaché (arrière-plan)
- `-p 8000:8000` : Mappe le port 8000 local vers le port 8000 du conteneur
- `--name oc-lettings-app` : Nom du conteneur
- `-e VARIABLE=valeur` : Définit une variable d'environnement

---

### Étape 3 : Accéder à l'application

Ouvrez votre navigateur : **http://localhost:8000**

---

## 6. Commandes utiles

### Gestion des conteneurs

```bash
# Voir les conteneurs en cours d'exécution
docker ps

# Voir tous les conteneurs (y compris arrêtés)
docker ps -a

# Arrêter un conteneur
docker stop oc-lettings-app

# Démarrer un conteneur arrêté
docker start oc-lettings-app

# Supprimer un conteneur
docker rm oc-lettings-app

# Forcer la suppression d'un conteneur en cours
docker rm -f oc-lettings-app
```

### Logs et débogage

```bash
# Voir les logs du conteneur
docker logs oc-lettings-app

# Suivre les logs en temps réel
docker logs -f oc-lettings-app

# Entrer dans le conteneur (shell)
docker exec -it oc-lettings-app bash
```

### Gestion des images

```bash
# Lister les images
docker images

# Supprimer une image
docker rmi oc-lettings

# Supprimer les images non utilisées
docker image prune

# Pour un nettoyage complet
docker image prune -a
```

### Docker Compose

```bash
# Lancer les services
docker-compose up

# Lancer en arrière-plan
docker-compose up -d

# Reconstruire et lancer
docker-compose up --build

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f

# Reconstruire sans cache
docker-compose build --no-cache

# Arrête, supprime les conteneurs ET les volumes
docker-compose down -v
```

---

## 7. Dépannage

### Erreur : "Docker daemon is not running"

**Solution** : Lancez Docker Desktop et attendez qu'il soit prêt.

---

### Erreur : "port is already allocated"

Le port 8000 est déjà utilisé.

**Solutions** :
1. Arrêter l'autre application qui utilise le port
2. Utiliser un autre port :
   ```bash
   docker run -d -p 8080:8000 --name oc-lettings-app oc-lettings
   ```
   Puis accéder via http://localhost:8080

---

### Erreur : "name is already in use"

Un conteneur avec ce nom existe déjà.

**Solution** :
```bash
# Supprimer l'ancien conteneur
docker rm oc-lettings-app

# Ou forcer la suppression s'il tourne encore
docker rm -f oc-lettings-app
```

---

### L'application ne démarre pas (erreur 500)

Vérifiez les logs :
```bash
docker logs oc-lettings-app
```

**Causes fréquentes** :
- `SECRET_KEY` non définie → Ajoutez-la dans `.env` ou en `-e`
- `ALLOWED_HOSTS` incorrect → Vérifiez qu'il contient `localhost`

---

### Les fichiers statiques ne s'affichent pas (CSS manquant)

Le `collectstatic` n'a pas été exécuté ou WhiteNoise n'est pas configuré.

**Vérification** : Les fichiers statiques sont collectés automatiquement lors du build Docker (voir Dockerfile ligne `RUN python manage.py collectstatic --noinput`).

Si le problème persiste, reconstruisez l'image :
```bash
docker-compose build --no-cache
docker-compose up
```

---

### Erreur de base de données

Pour le développement local, la base SQLite doit être montée en volume.

Vérifiez que le fichier `oc-lettings-site.sqlite3` existe à la racine du projet.

---

## 8. Pusher l'image sur Docker Hub

### Prérequis

1. Créer un compte Docker Hub : https://hub.docker.com
2. Se connecter depuis le terminal

### Étapes

```bash
# 1. Se connecter à Docker Hub
docker login

# 2. Construire l'image avec votre username Docker Hub
docker build -t VOTRE_USERNAME/oc-lettings:latest .

# 3. Pusher l'image vers Docker Hub
docker push VOTRE_USERNAME/oc-lettings:latest
```

### Exemple concret

Si votre username Docker Hub est `sebgris` :

```bash
docker login
docker build -t sebgris/oc-lettings:latest .
docker push sebgris/oc-lettings:latest
https://python-oc-lettings-fr-vu8j.onrender.com
https://dashboard.render.com/web/srv-d50jl275r7bs739gbd60
```

### Vérification

Après le push, votre image sera visible sur :
`https://hub.docker.com/r/sebgris/oc-lettings`

### Tags multiples

Vous pouvez aussi tagger avec le hash du commit :

```bash
# Récupérer le hash court du dernier commit
git rev-parse --short HEAD
# Exemple de résultat : a4aa10a

# Construire et tagger avec le hash
docker build -t sebgris/oc-lettings:a4aa10a -t sebgris/oc-lettings:latest .

# Pusher les deux tags
docker push sebgris/oc-lettings:a4aa10a
docker push sebgris/oc-lettings:latest
```

---

## Résumé rapide

```bash
# 1. Créer/modifier le fichier .env avec votre SECRET_KEY
# 2. Lancer Docker Desktop
# 3. Construire et lancer :
docker-compose up --build

# 4. Ouvrir http://localhost:8000

# 5. Pour arrêter :
docker-compose down
```
