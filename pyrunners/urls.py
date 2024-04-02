from django.urls import path, include
from pyrunners import views

app_name = 'pyrunners'

urlpatterns = [
    path('', views.index, name='index'),
    path('file-list/', views.file_list, name='file_list'),
    path('add-file/', views.add_file, name='add_file'),
    path('delete-file/', views.delete_file, name='delete_file'),
    path('rename-file/', views.rename_file, name='rename_file'),
    path('load-file/', views.load_file, name='load_file'),
    path('save-file/', views.save_file, name='save_file')
]