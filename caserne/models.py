from django.db import models
# Importer le module models de Django pour créer des tables de base de données  
from django.db.models.signals import m2m_changed
# m2m_changed → signal qui se déclenche quand une relation ManyToMany change
from django.dispatch import receiver
# receiver → permet de “capturer” cet événement



# ==================================================
# TYPE ENGIN
# ==================================================

class TypeEngin(models.Model):
    # models.Model est la classe de base de Django qui permet 
    # de transformer une classe Python en table de base de données

    nom_type = models.CharField(max_length=50)
    description = models.TextField()
    nb_personnel_requis = models.IntegerField()

    def __str__(self):
        return self.nom_type
    # __str__ définit la représentation texte d’un objet pour l’affichage dans Django


# ==================================================
# VEHICULE
# ==================================================

class Vehicule(models.Model):

    STATUT_CHOICES = [
        ('Disponible', 'Disponible'),
        ('En intervention', 'En intervention'),
        ('Indisponible', 'Indisponible'),
    ]

    code_radio = models.CharField(max_length=20)
    type_engin = models.ForeignKey(TypeEngin, on_delete=models.CASCADE)
    immatriculation = models.CharField(max_length=30)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='Disponible')
    km = models.IntegerField()

    def __str__(self):
        return self.code_radio


# ==================================================
# INTERVENTION
# ==================================================

class Intervention(models.Model):

    TYPE_SINISTRE_CHOICES = [
        ('Incendie', 'Incendie'),
        ('Secours à personne', 'Secours à personne'),
        ('Accident', 'Accident'),
    ]
    # Définir une liste de valeurs possibles (choix limités) pour un champ
    # Première stocké dans la base de donnée , deuxième affiché dans le formulaire

    numero_rapport = models.CharField(max_length=30)
    type_sinistre = models.CharField(max_length=30,choices=TYPE_SINISTRE_CHOICES)
    # avec ces champs ---->  Incendie , Secours à personne ,  Accident
    date_appel = models.DateTimeField()
    duree = models.IntegerField()
    adresse = models.CharField(max_length=255)
    vehicules = models.ManyToManyField(Vehicule)

    def __str__(self):
        return self.numero_rapport
    # pour éviter d'afficher comme ca <Rapport object (1)>


# ==================================================
# MATERIEL
# ==================================================

class Materiel(models.Model):
    nom = models.CharField(max_length=50)
    quantite = models.IntegerField()
    date_revision = models.DateField()

    def __str__(self):
        return self.nom


# ==================================================
# SIGNAL AUTOMATIQUE VEHICULE
# ==================================================

@receiver(m2m_changed, sender=Intervention.vehicules.through)
# “Django, écoute les changements sur la relation ManyToMany.”
# “quelque chose a changé dans ManyToMany”
# donc Django écoute cette table Intervention.vehicules.through
def update_vehicle_status(sender, instance, action, **kwargs):
    # instance → l’intervention concernée
    # Dès qu’un véhicule est ajouté ou retiré d’une intervention, exécute cette fonction.”

    if action == "post_add":
        instance.vehicules.update(statut="En intervention")

    if action == "post_remove":
        instance.vehicules.update(statut="Disponible")



class reclamation(models.Model):
    description = models.CharField(max_length=50)


