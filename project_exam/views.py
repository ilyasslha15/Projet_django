from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from caserne.forms import RegisterForm
from caserne.models import TypeEngin, Vehicule, Intervention, Materiel
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
    return render(request, 'registr ation/register.html', {'form': form})


