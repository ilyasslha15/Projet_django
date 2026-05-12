from django import forms
# Importer le module forms de Django pour pouvoir créer des formulaires
from django.contrib.auth.models import User
from caserne.models import Vehicule

class TypeEnginForm(forms.Form):
    # C’est un formulaire Django

    nom_type = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    #widget=forms.TextInput
    #👉 dit à Django : “affiche ce champ comme une zone de texte HTML

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    nb_personnel_requis = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )



class VehiculeForm(forms.Form):

    code_radio = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    immatriculation = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    statut = forms.ChoiceField(
        choices=[
            ('Disponible', 'Disponible'),
            ('En intervention', 'En intervention'),
            ('Indisponible', 'Indisponible')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    km = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    type_engin_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )



class InterventionForm(forms.Form):

    numero_rapport = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    type_sinistre = forms.ChoiceField(
        choices=[
            ('Incendie', 'Incendie'),
            ('Secours à personne', 'Secours à personne'),
            ('Accident', 'Accident'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    adresse = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })
    )

    date_appel = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )

    duree = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    vehicules = forms.ModelMultipleChoiceField(
    # Permet de sélectionner plusieurs véhicules dans un formulaire
    queryset=Vehicule.objects.all(),
    # Collection des objets
    # “liste de tous les véhicules de la base de données”
    widget=forms.SelectMultiple(attrs={'class': 'form-control'})
)

class MaterielForm(forms.Form):

    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    quantite = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    date_revision = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class reclamation_form(forms.Form):
    description = forms.CharField(max_length=50)
