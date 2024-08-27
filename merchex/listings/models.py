from django.db import models

# Create your models here.
# listings/models.py
# listings/views.py



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
    numero_demande = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    nom_agent = models.CharField(max_length=100)
    prenom_agent = models.CharField(max_length=100)
    matricule = models.CharField(max_length=100)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    type_de_vue = models.CharField(max_length=100)
    date_debut_retraite = models.DateField()
    date_de_la_demande = models.DateField()

    def __str__(self):
        return f"{self.numero_demande} - {self.nom_agent} {self.prenom_agent}"

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

class Agent(models.Model):
    matricule = models.CharField(max_length=20)
    nom_prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sit_fam = models.CharField(max_length=100)
    date_embauche = models.DateField()
    nombre_enf = models.IntegerField()
    date_debut_retraite = models.DateField(null=True, blank=True) 

    def __str__(self):
        return self.nom_prenom



class Demande(models.Model):
    numero_demande = models.CharField(max_length=255, default='DEFAULT_VALUE')
    ville = models.CharField(max_length=255)
    nom_agent = models.CharField(max_length=255)
    prenom_agent = models.CharField(max_length=255)
    matricule = models.CharField(max_length=50)
    date_demande = models.DateField()
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    type_de_vue = models.CharField(max_length=255,default='Inconnu')
    nombre_nuites = models.IntegerField()
    statut = models.CharField(max_length=255, blank=True, null=True)
    nature_periode = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nom_agent} {self.prenom_agent} ({self.matricule})"
    






from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=128, default='user')
    password = models.CharField(max_length=128, default='default_password')  # Consider hashing passwords in a real application
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    @classmethod
    def check_profile(cls, username, password):
        return cls.objects.filter(username=username, password=password).exists()


class AgentsLibre(models.Model):
    numero_demande = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    nom_agent = models.CharField(max_length=100)
    prenom_agent = models.CharField(max_length=100)
    matricule = models.CharField(max_length=100)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    type_de_vue = models.CharField(max_length=100)
    nombre_enfants = models.IntegerField()
    age = models.IntegerField()
    anciennete = models.IntegerField()
    date_embauche = models.DateField(null=True, blank=True)
    nombre_sejour = models.IntegerField()
    dernier_sejour = models.DateField()

    def __str__(self):
        return f"{self.nom_agent} {self.prenom_agent} ({self.matricule})"

