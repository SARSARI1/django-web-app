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

class Agent(models.Model):
    matricule = models.CharField(max_length=20)
    nom_prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sit_fam = models.CharField(max_length=100)
    date_embauche = models.DateField()
    nombre_enf = models.IntegerField()

    def __str__(self):
        return self.nom_prenom



class Demande(models.Model):
    site = models.CharField(max_length=100)
    numero_demande = models.CharField(max_length=100)
    agence = models.CharField(max_length=100)
    nom_etablissement_hoteliers = models.CharField(max_length=100)
    hotel_club_residence = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    nom_agent = models.CharField(max_length=100)
    prenom_agent = models.CharField(max_length=100)
    matricule = models.CharField(max_length=20)
    cat_prof = models.CharField(max_length=100)
    date_demande = models.DateField()
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    nombre_total_enfants = models.IntegerField()
    nombre_accompagnateurs = models.IntegerField()
    nombre_enfants_chambre_parents = models.IntegerField()
    total_membres_famille = models.IntegerField()
    nombre_nuites = models.IntegerField()
    nombre_chambre_double = models.IntegerField()
    nombre_chambre_single = models.IntegerField()
    type_vue = models.CharField(max_length=100)
    formule = models.CharField(max_length=100)
    montant_factures = models.DecimalField(max_digits=10, decimal_places=2)
    quote_part = models.DecimalField(max_digits=10, decimal_places=2)
    annee_facturation = models.IntegerField()
    mois_facturation = models.IntegerField()
    statut = models.CharField(max_length=100)
    date_statut = models.DateField()
    date_demande_voucher = models.DateField()
    date_envoi_voucher = models.DateField()
    nature_periode = models.CharField(max_length=100)
    saison = models.CharField(max_length=100)
    reference_paiement = models.CharField(max_length=100)
    nbr_etoiles = models.IntegerField()

    def __str__(self):
        return self.numero_demande
    
class Vue(models.Model):
    ville = models.CharField(max_length=100)
    type_vue = models.CharField(max_length=100)
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()
    quota = models.IntegerField()

    def __str__(self):
        return f"{self.ville} - {self.type_vue}"


from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

