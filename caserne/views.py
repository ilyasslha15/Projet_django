from django.shortcuts import render, redirect
from caserne.models import TypeEngin, Vehicule, Intervention, Materiel
from .forms import RegisterForm, TypeEnginForm, VehiculeForm, InterventionForm, MaterielForm
#AJOUT
from django.contrib.auth.decorators import login_required, user_passes_test

#  ADMIN ONLY
def admin_only(user):
    return user.is_staff


# ==================================================
# TYPE ENGIN
# ==================================================

@login_required
def liste_typeengin(request):
    types = TypeEngin.objects.all()
    #objects sert a récupérer tous les objets de type TypeEngin
    return render(request, "Typeengin/typeengin_list.html", {"types": types})


@user_passes_test(admin_only)
# Pour permettre uniquement aux administrateurs d'accéder à cette vue
def ajouter_typeengin(request):
    if request.method == "POST":
        # Si l'utilisateur clique sur envoyer
        form = TypeEnginForm(request.POST)
        # Récuperer les données
        if form.is_valid():
            TypeEngin.objects.create(**form.cleaned_data)
        # **form_cleaned_data données propres
            return redirect('liste_typeengin')
    else:
        form = TypeEnginForm()
        # Affiche vide si ce n'est pas post
    return render(request, "Typeengin/typeengin_add.html", {"form": form})


@user_passes_test(admin_only)
def editTypeEngin(request, TypeEngin_id):
    typeengin = TypeEngin.objects.get(id=TypeEngin_id)
    # Pour récupérer le type engin avec id = TypeEngin_id

    form = TypeEnginForm(request.POST or None, initial={
        "nom_type": typeengin.nom_type,
        "description": typeengin.description,
        "nb_personnel_requis": typeengin.nb_personnel_requis
    })
    # Si l'utilisateur a soumis le formulaire (POST) 
    # Si l'utilisateur vient juste d'ouvrir la page (GET)

    if form.is_valid():
        for k, v in form.cleaned_data.items():
            # pour chaque paire clé-valeur dans les données nettoyées
            setattr(typeengin, k, v)
            # k : clé , v : valeur
            # Mettre à jour l'objet typeengin avec les nouvelles valeurs
        typeengin.save()
        return redirect('liste_typeengin')

    return render(request, "Typeengin/typeengin_edit.html", {"form": form})


@user_passes_test(admin_only)
def delete_add_typeengin(request, TypeEngin_id):
    TypeEngin.objects.get(id=TypeEngin_id).delete()
    return redirect('liste_typeengin')



# ==================================================
# VEHICULE
# ==================================================

@login_required
def vehicule_list(request):

    type_id = request.GET.get('type')
    statut = request.GET.get('statut')

    vehicules = Vehicule.objects.all()
    #Premièrer affichage
     
    
    if type_id:
        vehicules = vehicules.filter(type_engin_id=type_id)

    if statut:
        vehicules = vehicules.filter(statut=statut)

    types = TypeEngin.objects.all()
    #Premièrer affichage

    return render(request, "Vehicule/listvehicule.html", {
        "vehicules": vehicules,
        "types": types
})


@user_passes_test(admin_only)
def addVehicule(request):
    if request.method == "POST":
        form = VehiculeForm(request.POST)
        if form.is_valid():
            Vehicule.objects.create(**form.cleaned_data)
            return redirect('vehicule_list')
    else:
        form = VehiculeForm()

    return render(request, "Vehicule/AddVehicule.html", {"form": form})


@user_passes_test(admin_only)
def editVehicule(request, Vehicule_id):
    vehicule = Vehicule.objects.get(id=Vehicule_id)

    form = VehiculeForm(request.POST or None, initial={
        "code_radio": vehicule.code_radio,
        "immatriculation": vehicule.immatriculation,
        "statut": vehicule.statut,
        "km": vehicule.km,
        "type_engin_id": vehicule.type_engin_id
    })

    if form.is_valid():
        for k, v in form.cleaned_data.items():
            setattr(vehicule, k, v)
        vehicule.save()
        return redirect('vehicule_list')

    return render(request, "Vehicule/vehiculeedit.html", {"form": form})


@user_passes_test(admin_only)
def deleteVehicule(request, Vehicule_id):
    Vehicule.objects.get(id=Vehicule_id).delete()
    return redirect('vehicule_list')


# ==================================================
# INTERVENTION (lecture autorisée)
# ==================================================

from django.contrib.auth.decorators import login_required

@login_required
def list_intervention(request):
    date = request.GET.get('date')
    type_sinistre = request.GET.get('type_sinistre')
    interventions = Intervention.objects.all().order_by('-date_appel')
    if date:
        interventions = interventions.filter(date_appel__date=date)
    if type_sinistre:
        interventions = interventions.filter(type_sinistre=type_sinistre)
    return render(request, "Intervention/intervention_list.html", {
        "interventions": interventions
    })


def add_intervention(request):
    if request.method == "POST":
        form = InterventionForm(request.POST)

        if form.is_valid(): 

            vehicules = form.cleaned_data['vehicules']

            #  Vérification : bloquer seulement la maintenance
            for v in vehicules:
                if v.statut == "Indisponible" or v.statut == "En intervention":
                    form.add_error(
                        "vehicules",
                        f"{v.immatriculation} est en maintenance ou en intervention et ne peut pas être utilisé"
                    )
                    return render(request, "Intervention/Intervention_add.html", {"form": form})
                
            #  Création de l'intervention
            intervention = Intervention.objects.create(
                numero_rapport=form.cleaned_data['numero_rapport'],
                type_sinistre=form.cleaned_data['type_sinistre'],
                adresse=form.cleaned_data['adresse'],
                date_appel=form.cleaned_data['date_appel'],
                duree=form.cleaned_data['duree']
            )

            # Association ManyToMany
            intervention.vehicules.set(vehicules)

            #  Mise à jour du statut des véhicules
            for v in vehicules:
                v.statut = "En intervention"
                v.save()

            return redirect('list_intervention')

    else:
        form = InterventionForm()

    return render(request, "Intervention/Intervention_add.html", {"form": form})


@user_passes_test(admin_only)
def editIntervention(request, Intervention_id):
    intervention = Intervention.objects.get(id=Intervention_id)

    form = InterventionForm(request.POST or None, initial={
        "numero_rapport": intervention.numero_rapport,
        "type_sinistre": intervention.type_sinistre,
        "adresse": intervention.adresse,
        "date_appel": intervention.date_appel,
        "duree": intervention.duree,
        "vehicules": intervention.vehicules.all()
    })

    if form.is_valid():
        for k, v in form.cleaned_data.items():
            if k != "vehicules":
                setattr(intervention, k, v)
        intervention.save()
        intervention.vehicules.set(form.cleaned_data['vehicules'])
        return redirect('list_intervention')

    return render(request, "Intervention/Intervention_edit.html", {"form": form})


@user_passes_test(admin_only)
def deleteIntervention(request, Intervention_id):
    intervention = Intervention.objects.get(id=Intervention_id)
    for v in intervention.vehicules.all():
        v.statut = "Disponible"
        v.save()
    intervention.vehicules.clear()
    intervention.delete()
    return redirect('list_intervention')


# ==================================================
# MATERIEL
# ==================================================

@login_required
def listMateriel(request):
    from datetime import date
    materiels = Materiel.objects.all()
    return render(request, "Materiel/materiel_list.html", {"materiels": materiels, "today": date.today()})


@user_passes_test(admin_only)
def addMateriel(request):
    if request.method == "POST":
        form = MaterielForm(request.POST)
        if form.is_valid():
            Materiel.objects.create(**form.cleaned_data)
            return redirect('materiel_list')
    else:
        form = MaterielForm()

    return render(request, "Materiel/AddMateriel.html", {"form": form})


@user_passes_test(admin_only)
def editMateriel(request, Materiel_id):
    materiel = Materiel.objects.get(id=Materiel_id)

    form = MaterielForm(request.POST or None, initial={
        "nom": materiel.nom,
        "quantite": materiel.quantite,
        "date_revision": materiel.date_revision
    })

    if form.is_valid():
        for k, v in form.cleaned_data.items():
            setattr(materiel, k, v)
        materiel.save()
        return redirect('materiel_list')

    return render(request, "Materiel/Materiel_edit.html", {"form": form})


@user_passes_test(admin_only)
def deleteMateriel(request, Materiel_id):
    Materiel.objects.get(id=Materiel_id).delete()
    return redirect('materiel_list')


