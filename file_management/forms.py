from django import forms
from .models import File, Folder, Project, Asset, Comment

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'name']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
