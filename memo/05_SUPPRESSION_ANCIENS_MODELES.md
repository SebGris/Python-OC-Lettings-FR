# Suppression des anciens modèles et refactorisation complète

## Vue d'ensemble

Ce document explique la dernière étape de la refactorisation : supprimer les anciens modèles de `oc_lettings_site` et finaliser le déplacement des vues, URLs et templates.

## Étape 1 : Vider oc_lettings_site/models.py

```python
# Models have been moved to their respective apps:
# - Address, Letting -> lettings app
# - Profile -> profiles app
```

## Étape 2 : Mettre à jour admin.py

### lettings/admin.py
```python
from django.contrib import admin
from .models import Address, Letting

admin.site.register(Address)
admin.site.register(Letting)
```

### profiles/admin.py
```python
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
```

### oc_lettings_site/admin.py
```python
from django.contrib import admin
# Models have been moved to their respective apps
```

## Étape 3 : Déplacer les vues

### lettings/views.py
```python
from django.shortcuts import render
from .models import Letting

def index(request):
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)

def letting(request, letting_id):
    letting = Letting.objects.get(id=letting_id)
    context = {'title': letting.title, 'address': letting.address}
    return render(request, 'lettings/letting.html', context)
```

### profiles/views.py
```python
from django.shortcuts import render
from .models import Profile

def index(request):
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)

def profile(request, username):
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
```

### oc_lettings_site/views.py
```python
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
```

## Étape 4 : Créer les URLs avec espaces de noms

### lettings/urls.py
```python
from django.urls import path
from . import views

app_name = 'lettings'  # Espace de noms

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:letting_id>/', views.letting, name='letting'),
]
```

### profiles/urls.py
```python
from django.urls import path
from . import views

app_name = 'profiles'  # Espace de noms

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
]
```

### oc_lettings_site/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls')),  # Inclusion avec namespace
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
]
```

## Étape 5 : Déplacer les templates

### Structure des templates

```
lettings/
└── templates/
    └── lettings/
        ├── index.html      (anciennement lettings_index.html)
        └── letting.html

profiles/
└── templates/
    └── profiles/
        ├── index.html      (anciennement profiles_index.html)
        └── profile.html

templates/
├── base.html
└── index.html
```

### Mise à jour des URLs dans les templates

**Avant (ancienne syntaxe) :**
```html
{% url 'lettings_index' %}
{% url 'letting' letting_id=letting.id %}
{% url 'profiles_index' %}
{% url 'profile' username=profile.user.username %}
```

**Après (avec espaces de noms) :**
```html
{% url 'lettings:index' %}
{% url 'lettings:letting' letting_id=letting.id %}
{% url 'profiles:index' %}
{% url 'profiles:profile' username=profile.user.username %}
```

## Étape 6 : Créer la migration pour supprimer les anciennes tables

```bash
python manage.py makemigrations oc_lettings_site --name delete_old_models
```

Génère automatiquement :
```python
operations = [
    migrations.RemoveField(model_name='letting', name='address'),
    migrations.RemoveField(model_name='profile', name='user'),
    migrations.DeleteModel(name='Address'),
    migrations.DeleteModel(name='Letting'),
    migrations.DeleteModel(name='Profile'),
]
```

```bash
python manage.py migrate
```

## Étape 7 : Supprimer le related_name temporaire

Dans `profiles/models.py`, on retire `related_name='profiles_profile'` :

```python
# Avant
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles_profile')

# Après
user = models.OneToOneField(User, on_delete=models.CASCADE)
```

```bash
python manage.py makemigrations profiles
python manage.py migrate
```

## Étape 8 : Supprimer les anciens templates

```bash
rm templates/lettings_index.html
rm templates/letting.html
rm templates/profiles_index.html
rm templates/profile.html
```

## Vérification finale

```bash
python manage.py check
# System check identified no issues (0 silenced).
```

## Récapitulatif des fichiers modifiés

| Fichier | Modification |
|---------|--------------|
| `oc_lettings_site/models.py` | Vidé (commentaire seulement) |
| `oc_lettings_site/admin.py` | Vidé |
| `oc_lettings_site/views.py` | Garde uniquement `index()` |
| `oc_lettings_site/urls.py` | Utilise `include()` |
| `lettings/admin.py` | Enregistre Address et Letting |
| `lettings/views.py` | Contient `index()` et `letting()` |
| `lettings/urls.py` | Nouveau fichier avec `app_name` |
| `profiles/admin.py` | Enregistre Profile |
| `profiles/views.py` | Contient `index()` et `profile()` |
| `profiles/urls.py` | Nouveau fichier avec `app_name` |

## Concept clé : Espaces de noms (namespaces)

`app_name = 'lettings'` dans `urls.py` crée un espace de noms.

**Avantages :**
- Évite les conflits de noms entre applications
- Permet d'avoir `lettings:index` et `profiles:index` sans ambiguïté
- Convention Django recommandée pour les applications réutilisables

**Syntaxe dans les templates :**
```html
{% url 'namespace:nom_url' %}
```

## Sources

- [URL dispatcher - Django Documentation](https://docs.djangoproject.com/en/5.2/topics/http/urls/#url-namespaces)
- [include() - Django Documentation](https://docs.djangoproject.com/en/5.2/ref/urls/#include)
