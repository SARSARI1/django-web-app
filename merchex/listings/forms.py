# ~/projects/django-web-app/merchex/listings/forms.py
from django import forms
from .models import Agent  # Make sure the Agent model is imported


class UploadFilesForm(forms.Form):
    agents_file = forms.FileField(label='Téléchargez le fichier des agents')
    historique_file = forms.FileField(label='Téléchargez le fichier historique')
    demandes_file = forms.FileField(label='Téléchargez le fichier des demandes')
   

class CalculForm(forms.Form):
    date_debut_sejour = forms.DateField(label='Date début séjour', widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin_sejour = forms.DateField(label='Date fin séjour', widget=forms.DateInput(attrs={'type': 'date'}))

from .models import Quota

class QuotaForm(forms.ModelForm):
    class Meta:
        model = Quota
        fields = ['ville', 'type_de_vue', 'quota_value']


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(
        label='Fichier Excel',
        help_text='Sélectionnez un fichier Excel (.xlsx)',
        required=True
    )

# lgoin forms.py
from django import forms
from .models import Profile

class SignUpForm(forms.ModelForm):
    # Add placeholders and class for styling
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Entrez votre mot de passe', 
            'class': 'form-control'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Entrez votre nom d’utilisateur', 
            'class': 'form-control'
        })
    )

    class Meta:
        model = Profile
        fields = ['username', 'password']


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['matricule', 'nom_prenom', 'date_naissance', 'sit_fam', 'date_embauche', 'nombre_enf', 'date_debut_retraite']
        widgets = {
            'matricule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Matricule'}),
            'nom_prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Nom et Prénom'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Date de Naissance', 'type': 'date'}),
            'sit_fam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter la situation familiale'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Date d\'Embauche', 'type': 'date'}),
            'nombre_enf': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Nombre d\'Enfants'}),
            'date_debut_retraite': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter Date de Début de Retraite', 'type': 'date'}),
        }

        labels = {
            'matricule': 'Matricule',
            'nom_prenom': 'Nom et Prénom',
            'date_naissance': 'Date de Naissance',
            'sit_fam': 'Situation Familiale',
            'date_embauche': 'Date d\'Embauche',
            'nombre_enf': 'Nombre d\'Enfants',
            'date_debut_retraite': 'Date de Début de Retraite',
        }


from django import forms
from .models import Demande

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['numero_demande', 'ville', 'nom_agent', 'prenom_agent', 'matricule', 'date_demande', 'date_debut_sejour', 'date_fin_sejour', 'type_de_vue', 'nombre_nuites']

    
        

from django import forms

class UploadExcelFileDemandesForm(forms.Form):
    demandes_file = forms.FileField(label='Fichier de demandes')

class UploadFilesFormLibre(forms.Form):
    agents_file = forms.FileField(label='Téléchargez le fichier des agents')
    historique_file_first = forms.FileField(label='Téléchargez le fichier historique 1')
    historique_file_second = forms.FileField(label='Téléchargez le fichier historique 2')
    demandes_file = forms.FileField(label='Téléchargez le fichier des demandes')
    date_debut_sejour = forms.DateField(label='Date début séjour', widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin_sejour = forms.DateField(label='Date fin séjour', widget=forms.DateInput(attrs={'type': 'date'}))
   


class AffectationForm(forms.Form):
    affectation_file = forms.FileField(label="Fichier d'affectation")
