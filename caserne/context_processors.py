from datetime import date
from .models import Materiel

# C'est un context processor — une fonction spéciale Django '
# 'qui s'exécute automatiquement sur chaque page du site.
def alertes_context(request):
    """Injecte le nombre d'alertes matériel dans tous les templates."""
    if request.user.is_authenticated:
        alertes = Materiel.objects.filter(date_revision__lt=date.today()).count()
        return {'alertes_materiel': alertes}
    return {'alertes_materiel': 0}


