from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from caserne.forms import RegisterForm,reclamation_form
from caserne.models import TypeEngin, Vehicule, Intervention, Materiel,reclamation
from django.http import JsonResponse
from django.db.models import Q
from datetime import date

@login_required
def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    vehicules_total = Vehicule.objects.count()
    vehicules_dispo = Vehicule.objects.filter(statut="Disponible").count()
    vehicules_inter = Vehicule.objects.filter(statut="En intervention").count()
    vehicules_indispo = Vehicule.objects.filter(statut="Indisponible").count()
    interventions = Intervention.objects.count()
    materiels = Materiel.objects.count()
    types_engins = TypeEngin.objects.count()
    recent_interventions = Intervention.objects.order_by('-date_appel')[:5]
    # du plus RÉCENT au plus ANCIEN seulement 5 enregistrements
    today = date.today()
    materiels_expires = Materiel.objects.filter(date_revision__lt=today)
    #Les matériaux dèja expirés
    alertes_materiel = materiels_expires.count()

    return render(request, "dashboard.html", {
        "vehicules_total": vehicules_total,
        "vehicules_dispo": vehicules_dispo,
        "vehicules_inter": vehicules_inter,
        "vehicules_indispo": vehicules_indispo,
        "interventions": interventions,
        "materiels": materiels,
        "types_engins": types_engins,
        "recent_interventions": recent_interventions,
        "materiels_expires": materiels_expires[:6],
        "alertes_materiel": alertes_materiel,
    })


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            # le mot de passe en version sécurisée (cryptée) avant de l’enregistrer
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def reclamation_list(request):
    reclamations = reclamation.objects.all()
    #objects sert a récupérer tous les objets de type TypeEngin
    return render(request, "reclamations.html", {"reclamations": reclamations})

login_required
def reclamation_add(request):
    if request.method == "POST":
        # Si l'utilisateur clique sur envoyer
        form = reclamation_form(request.POST)
        # Récuperer les données
        if form.is_valid():
            reclamation.objects.create(**form.cleaned_data)
        # **form_cleaned_data données propres
            return redirect('reclamation_list')
    else:
        form = reclamation_form()
        # Affiche vide si ce n'est pas post
        return  render(request, "reclamation_add.html", {"form": form})
    


def reclamation_delete(request,reclamation_id):
     reclamation.objects.get(id=reclamation_id).delete()
     return redirect('reclamation_list')



def reclamation_edit(request, reclamation_id):
 r = reclamation.objects.get(id=reclamation_id)

 form = reclamation_form(request.POST or None, initial={
        "description": r.description,
    })

 if form.is_valid():
        for k, v in form.cleaned_data.items():
         setattr(r, k, v)
        r.save()
        return redirect('reclamation_list')

 return render(request, "reclamation_edit.html", {"form": form})
