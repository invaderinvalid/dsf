from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import File, Folder, Project, Asset, AssetVersion, Comment
from .forms import FileUploadForm, FolderForm, ProjectForm, AssetForm, CommentForm
from .ondemand_api import categorize_file
from django.db.models import Q
from .ai_tagging import tag_file  # You'll need to implement this function

@login_required
def file_list(request, folder_id=None):
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
        files = File.objects.filter(user=request.user, folder=folder)
        subfolders = Folder.objects.filter(user=request.user, parent=folder)
    else:
        folder = None
        files = File.objects.filter(user=request.user, folder__isnull=True)
        subfolders = Folder.objects.filter(user=request.user, parent__isnull=True)
    
    return render(request, 'file_management/file_list.html', {
        'files': files,
        'subfolders': subfolders,
        'current_folder': folder
    })

@login_required
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            
            # AI tagging
            ai_category = tag_file(file.file.path)
            file.ai_category = ai_category
            file.save()
            
            messages.success(request, f"File '{file.name}' uploaded and tagged as '{ai_category}'.")
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'file_management/file_upload.html', {'form': form})

@login_required
def create_folder(request, parent_id=None):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            if parent_id:
                parent = get_object_or_404(Folder, id=parent_id, user=request.user)
                folder.parent = parent
            folder.save()
            messages.success(request, f"Folder '{folder.name}' created successfully.")
            return redirect('file_list', folder_id=parent_id)
    else:
        form = FolderForm()
    return render(request, 'file_management/create_folder.html', {'form': form, 'parent_id': parent_id})

@login_required
def move_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    if request.method == 'POST':
        folder_id = request.POST.get('folder')
        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id, user=request.user)
            file.folder = folder
        else:
            file.folder = None
        file.save()
        messages.success(request, f"File '{file.name}' has been moved.")
        return redirect('file_list', folder_id=file.folder.id if file.folder else None)
    
    folders = Folder.objects.filter(user=request.user)
    return render(request, 'file_management/move_file.html', {'file': file, 'folders': folders})

@login_required
def ai_categorize(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    ai_category = categorize_file(file.file.path)
    file.ai_category = ai_category
    file.save()
    messages.success(request, f"File '{file.name}' has been categorized as '{ai_category}'.")
    return redirect('file_list')

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user) | Project.objects.filter(collaborators=request.user)
    return render(request, 'file_management/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner and request.user not in project.collaborators.all():
        messages.error(request, "You don't have permission to view this project.")
        return redirect('project_list')
    assets = project.assets.all()
    return render(request, 'file_management/project_detail.html', {'project': project, 'assets': assets})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, f"Project '{project.name}' created successfully.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'file_management/create_project.html', {'form': form})

@login_required
def upload_asset(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.project = project
            asset.save()
            
            # Create initial version
            AssetVersion.objects.create(asset=asset, version_number=1, file=asset.file)
            
            # AI tagging
            ai_tags = tag_file(asset.file.path)
            asset.ai_tags = ai_tags
            asset.save()
            
            messages.success(request, f"Asset '{asset.name}' uploaded successfully.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = AssetForm()
    return render(request, 'file_management/upload_asset.html', {'form': form, 'project': project})

@login_required
def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    versions = asset.versions.all().order_by('-version_number')
    comments = asset.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.asset = asset
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('asset_detail', asset_id=asset.id)
    else:
        form = CommentForm()
    
    return render(request, 'file_management/asset_detail.html', {
        'asset': asset,
        'versions': versions,
        'comments': comments,
        'form': form
    })

@login_required
def upload_new_version(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            new_asset = form.save(commit=False)
            new_version_number = asset.current_version + 1
            
            # Create new version
            AssetVersion.objects.create(
                asset=asset,
                version_number=new_version_number,
                file=new_asset.file
            )
            
            # Update asset
            asset.file = new_asset.file
            asset.current_version = new_version_number
            asset.save()
            
            # AI tagging
            ai_tags = tag_file(asset.file.path)
            asset.ai_tags = ai_tags
            asset.save()
            
            messages.success(request, f"New version (v{new_version_number}) uploaded successfully.")
            return redirect('asset_detail', asset_id=asset.id)
    else:
        form = AssetForm(instance=asset)
    return render(request, 'file_management/upload_new_version.html', {'form': form, 'asset': asset})

@login_required
def folder_contents(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    files = File.objects.filter(user=request.user, folder=folder)
    subfolders = Folder.objects.filter(user=request.user, parent=folder)
    
    return render(request, 'file_management/file_list.html', {
        'files': files,
        'subfolders': subfolders,
        'current_folder': folder
    })
