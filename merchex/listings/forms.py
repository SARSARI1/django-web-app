# ~/projects/django-web-app/merchex/listings/forms.py
from django import forms

class UploadFilesForm(forms.Form):
    agents_file = forms.FileField(label='Téléchargez le fichier des agents')
    historique_file = forms.FileField(label='Téléchargez le fichier historique')
    demandes_file = forms.FileField(label='Téléchargez le fichier des demandes')
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