# ~/projects/django-web-app/merchex/merchex/urls.py
from django.contrib import admin
from django.urls import path
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('hello/', views.hello),
    path('about-us/', views.about),
    path('dashboard/', views.statistiques,  name='dashboard'),
    path('listes/', views.tables, name='listes'),
    path('historique/', views.historique, name='historique'),
    path('quota/',views.quota, name='quota'),
    path('tables/', views.upload_files, name='upload_files'),  # This should match the form action
    path('download_pdf/<str:ville>/<str:type_de_vue>/', views.download_pdf, name='download_pdf'),
    path('list/', views.list_generated, name='list_generated'),
    path('quotas/', views.quota_list, name='quota_list'),
    path('update_quota/', views.update_quota, name='update_quota'),
    path('delete_quota/', views.delete_quota, name='delete_quota'),
    path('add_quota/', views.add_quota, name='add_quota'),
    path('upload-excel-historique/', views.upload_excel_historique, name='upload_excel_historique'),
    path('delete-historique/', views.delete_historique, name='delete_historique'),
    path('AgentsAffichage/', views.AgentsAffichage, name='AgentsAffichage'),
    path('agents/edit/<int:agent_id>/', views.edit_agent, name='edit_agent'),
    path('agents/delete/<int:agent_id>/', views.delete_agent, name='delete_agent'),  
    path('agents/', views.AgentsAffichage, name='AgentsAffichage'), 
    path('upload_excel/', views.upload_excel_agents, name='upload_excel'), 
    path('delete_all_agents/', views.delete_all_agents, name='delete_all_agents'),
      # Liste et affichage des demandes
    path('demandes/', views.demandes_affichage, name='demandes_affichage'),
    
    # Formulaire de modification d'une demande
    path('demandes/edit/<int:demande_id>/', views.edit_demande, name='edit_demande'),
    
    # Suppression d'une demande
    path('demandes/delete/<int:demande_id>/', views.delete_demande, name='delete_demande'),
    
    # Téléchargement d'un fichier Excel
    path('upload_excel_Demandes/', views.upload_excelDemandes, name='upload_excel_Demandes'),
    
    # Suppression de toutes les demandes
    path('delete_all_demandes/', views.delete_all_demandes, name='delete_all_demandes'),
    

    
    
]
