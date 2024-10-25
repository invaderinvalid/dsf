from django.urls import path
from . import views
from .views import ProjectListView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('create_project/', views.create_project, name='create_project'),
    path('project/<int:project_id>/upload_asset/', views.upload_asset, name='upload_asset'),
    path('asset/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('asset/<int:asset_id>/upload_new_version/', views.upload_new_version, name='upload_new_version'),
    path('files/', views.file_list, name='file_list'),
    path('files/<int:folder_id>/', views.file_list, name='file_list'),
    path('upload/', views.file_upload, name='file_upload'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('create_folder/<int:parent_id>/', views.create_folder, name='create_subfolder'),
    path('ai_categorize/<int:file_id>/', views.ai_categorize, name='ai_categorize'),
    path('move_file/<int:file_id>/', views.move_file, name='move_file'),
    path('folder_contents/<int:folder_id>/', views.folder_contents, name='folder_contents'),
]
