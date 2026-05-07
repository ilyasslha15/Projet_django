# Il configure ton application Django
from django.apps import AppConfig


class CaserneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "caserne"

    def ready(self):
        import caserne.models  # active les signals
        # fonction spéciale qui s’exécute au démarrage de l’application


   # un code qui s’exécute automatiquement quand quelque chose se passe
 
   # Exemple :

   # ajouter véhicule → changer statut
   #supprimer → mettre à jour