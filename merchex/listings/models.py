from django.db import models

# Create your models here.
# listings/models.py

class Band(models.Model):
    name = models.fields.CharField(max_length=100)


class DemandesTraiter(models.Model):
    numero_demande = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    nom_agent = models.CharField(max_length=100)
    prenom_agent = models.CharField(max_length=100)
    matricule = models.CharField(max_length=100)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    type_de_vue = models.CharField(max_length=100)
    A = models.IntegerField()
    D = models.IntegerField()
    S = models.IntegerField()
    P = models.FloatField()

    class Meta:
        ordering = ['-P']  # Order by 'P' in descending order


class Quota(models.Model):
    ville = models.CharField(max_length=100)
    type_de_vue = models.CharField(max_length=100)
    quota_value = models.IntegerField()

    class Meta:
        unique_together = ('ville', 'type_de_vue')  # Ensure unique combinations of ville and type_de_vue
        ordering = ['ville', 'type_de_vue']

class RejectedDemandesRetrait(models.Model):
    numero_demande = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    nom_agent = models.CharField(max_length=255)
    prenom_agent = models.CharField(max_length=255)
    matricule = models.CharField(max_length=255)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    type_de_vue = models.CharField(max_length=255)
    date_debut_retraite = models.DateField()
    date_de_la_demande = models.DateField()

    class Meta:
        verbose_name = 'Rejected Demande Retrait'
        verbose_name_plural = 'Rejected Demandes Retraits'
    
    def __str__(self):
        return f"{self.numero_demande} - {self.ville}"

class Historique(models.Model):
    ville = models.CharField(max_length=255)
    nom_agent = models.CharField(max_length=255)
    prenom_agent = models.CharField(max_length=255)
    matricule = models.CharField(max_length=50)
    date_demande = models.DateField()
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    type_de_vue = models.CharField(max_length=255)
    nombre_nuites = models.IntegerField()

    def __str__(self):
        return f'{self.ville} - {self.nom_agent} {self.prenom_agent}'