from django import forms
from .models import File, Folder, Project, Asset, Comment

class FileUploadForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.none())

    class Meta:
        model = File
        fields = ['file', 'name', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FileUploadForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(owner=user)

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
