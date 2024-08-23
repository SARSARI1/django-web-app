# ~/projects/django-web-app/merchex/merchex/urls.py
from django.contrib import admin
from django.urls import path
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('about-us/', views.about),
    path('dashboard/', views.statistiques,  name='dashboard'),
    path('listes/', views.tables, name='listes'),
    path('historique/', views.historique, name='historique'),
    path('quota/',views.quota, name='quota'),
    path('tables/', views.upload_files, name='upload_files'),  # This should match the form action
    path('proceed_without_storing/', views.proceed_without_storing, name='proceed_without_storing'),  # This should match the form action

    path('process-files/', views.process_files, name='process_files'),  # Add this line
    path('proceed-with-calculation/', views.proceed_with_calculation, name='proceed_with_calculation'),
    path('list-generated/', views.list_generated, name='list_generated'),
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
    path('upload_excel_agents/', views.upload_excel_agents, name='upload_excel_agents'), 
    path('delete_all_agents/', views.delete_all_agents, name='delete_all_agents'),
    # Liste et affichage des demandes
    
    path('demandes/', views.demande_list, name='demande_list'),
    path('demandes/add/', views.add_demande, name='add_demande'),
    path('demandes/edit/<int:demande_id>/', views.edit_demande, name='edit_demande'),
    path('demandes/<int:demande_id>/edit-data/', views.get_demande_data, name='get_demande_data'),
    path('demandes/delete/<int:demande_id>/', views.delete_demande, name='delete_demande'),
    path('demandes/delete-all/', views.delete_all_demandes, name='delete_all_demandes'),
    # urls.py
    path('demandes/upload/', views.upload_excel_demandes, name='upload_excel_demandes'),


    path('delete-all-demandes-traiter/', views.delete_all_demandes_traiter, name='delete_all_demandes_traiter'),
    path('delete-all-demandes-rejetees/', views.delete_all_demandes_rejetees, name='delete_all_demandes_rejetees'),
    path('download-pdf-demandes-traiter/', views.download_pdf_demandes_traiter, name='download_pdf_demandes_traiter'),
    path('download-pdf-rejected-demandes/', views.download_pdf_rejected_demandes, name='download_pdf_rejected_demandes'),
    path('download-excel/<str:ville>/<str:type_de_vue>/', views.download_excel, name='download_excel'),
     path('download-all-demandes-excel/', views.download_all_demandes_excel, name='download_all_demandes_excel'),
     path('download-all-rejected-demandes-excel/', views.download_all_rejected_demandes_excel, name='download_all_rejected_demandes_excel'),

    

    ##################################################
    path('libres/', views.ListsLibre, name='libres'),
   path('libres_files/', views.filter_and_rank_agents, name='libres_files'),
    path('listlibre/', views.libre_generated, name='libre_generated'),
    path('download_excel/<str:ville>/<str:type_de_vue>/', views.download_excel_libre, name='download_excel_libre'),
    path('upload_rank/', views.upload_rank, name='upload_rank'),
    path('delete_libre_traités/', views.delete_demandes_libres, name='delete_libre_traites'),
    path('download_pdf_demandes_libre/', views.download_pdf_demandes_libre, name='download_pdf_demandes_libre'),
    path('download_excel_demandes_libre/', views.download_excel_demandes_libre, name='download_excel_demandes_libre'),
    path('download_excel_rejected_demandes/', views.download_excel_rejected_demandes, name='download_excel_rejected_demandes'),
    path('download_pdf_libre/<str:ville>/<str:type_de_vue>//', views.download_pdf_libre, name='download_pdf_libre'),
    path('affecter/<str:ville>/<str:type_de_vue>/', views.affecter, name='affecter'),

    
]
