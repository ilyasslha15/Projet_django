# Register your models here.

from django.contrib import admin
from .models import Vehicule, Intervention, TypeEngin, Materiel

@admin.register(TypeEngin)
class TypeEnginAdmin(admin.ModelAdmin):
    list_display = ('nom_type', 'description', 'nb_personnel_requis')

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('code_radio', 'immatriculation', 'statut', 'type_engin', 'km')
    list_filter = ('statut', 'type_engin')


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('numero_rapport', 'type_sinistre', 'date_appel', 'duree')
    filter_horizontal = ('vehicules',)

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'date_revision')
