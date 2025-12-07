# Réduisez les divers problèmes sur le projet

## Personnalisation du texte pluriel dans Django Admin

**Source** : https://books.agiliq.com/projects/django-admin-cookbook/en/latest/plural_text.html

### Problème

Par défaut, Django Admin affiche le nom du modèle suivi d'un "s" pour former le pluriel. Cependant, cette approche ne fonctionne pas pour tous les modèles, notamment ceux avec des pluriels irréguliers.

### Solution

Utiliser l'attribut `verbose_name_plural` dans la classe `Meta` du modèle pour définir manuellement la forme plurielle correcte.

### Exemple de code

```python
class Category(models.Model):
    ...

    class Meta:
        verbose_name_plural = "Categories"

class Hero(Entity):
    ...

    class Meta:
        verbose_name_plural = "Heroes"
```

Cette approche permet de corriger l'affichage des noms de modèles au pluriel dans l'interface d'administration Django.
