from django.urls import path
from . import views

urlpatterns=[
    path("list_typeengin/",views.liste_typeengin,name="liste_typeengin"),
    path('add_typeengin/', views.ajouter_typeengin, name='type_add'),
    path("delete_add_typeengin/<int:TypeEngin_id>/", views.delete_add_typeengin, name="delete_add_typeengin"),
    path('typeengin_edit/<int:TypeEngin_id>/', views.editTypeEngin, name='type_edit'),
    path('listvehicule/', views.vehicule_list, name='vehicule_list'),
    path('vehicule_edit/<int:Vehicule_id>/', views.editVehicule, name='vehicule_edit'),
    path('vehicule_add/', views.addVehicule, name='vehicule_add'),
    path('vehicule_del/<int:Vehicule_id>/', views.deleteVehicule, name='vehicule_del'),
    path('add_intervention/', views.add_intervention, name='add_intervention'),
    path('list_intervention/', views.list_intervention, name='list_intervention'),
    path('Intervention_edit/<int:Intervention_id>/', views.editIntervention, name='intervention_edit'),
    path('Intervention_delete/<int:Intervention_id>/', views.deleteIntervention, name='intervention_delete'),
    path('materiel_list/', views.listMateriel, name='materiel_list'),
    path('materiel_add/', views.addMateriel, name='materiel_add'),
    path('materiel_edit/<int:Materiel_id>/', views.editMateriel, name='materiel_edit'),
    path('materiel_delete/<int:Materiel_id>/', views.deleteMateriel, name='materiel_delete'),

]
