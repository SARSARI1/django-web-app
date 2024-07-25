# ~/projects/django-web-app/merchex/merchex/urls.py
from django.contrib import admin
from django.urls import path
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('about-us/', views.about),
    path('listes/', views.tables, name='listes'),
    path('agents/',views.agents, name='agents'),
    path('demandes/',views.demandes, name='demandes'),
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
    
]
