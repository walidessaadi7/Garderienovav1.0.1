from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Center
from .forms import CenterCreationForm,DirectorCreationForm,AssignDirectorForm
from django.shortcuts import render, get_object_or_404
from .models import Center, Organization
from django.core.mail import send_mail #hadi mzal mkhdemti biha
from django.conf import settings

@login_required
def create_center(request):
    if request.user.role_type != 'owner':
        return redirect('login')

    organization = get_object_or_404(Organization, owner__user=request.user)

    if request.method == 'POST':
        form = CenterCreationForm(request.POST)
        if form.is_valid():
            center = form.save(commit=False)
            center.org = organization
            center.save()
            # Redirect to the success page instead of the dashboard
            return redirect('center_success', center_id=center.center_id)
    else:
        form = CenterCreationForm()

    return render(request, 'create_center.html', {
        'form': form,
        'organization': organization
    })

@login_required
def center_success(request, center_id):
    # Fetch the newly created center to show its name
    center = get_object_or_404(Center, center_id=center_id, org__owner__user=request.user)
    return render(request, 'center_congrats.html', {'center': center})
@login_required
def center_info_view(request, center_id):
    # Security Check: Njibou l-center b l-ID walakin khass darouri 
    # ikoun taba3 l-organization dial dak l-user li m-connecti.
    center = get_object_or_404(
        Center, 
        center_id=center_id, 
        org__owner__user=request.user
    )
    
    return render(request, 'center_info.html', {'center': center})

# Ila bghiti lista kamla dial les centers dial dak l-owner:
def owner_centers_list(request):
    centers = Center.objects.filter(org__owner__user=request.user)
    return render(request, 'centers_list.html', {'centers': centers})

#hna dyal send email sir setting 3endak tensa
def create_director_general(request):
    if request.method == 'POST':
        form = DirectorCreationForm(request.POST)
        if form.is_valid():
            director = form.save()
            # Mn be3d ma t-creera l-director, sift l-owner i-assignih
            return redirect('owner_centers_list') # Page fin i-assignih
    else:
        form = DirectorCreationForm()
    
    return render(request, 'create_director.html', {'form': form})
def assign_director_to_center(request, center_id):
    # Kan-jibo l-center w t-akked m-rbot b l-org dyal had l-user
    center = get_object_or_404(Center, center_id=center_id, org__owner__user=request.user)
    
    if request.method == 'POST':
        # Pass user to form in POST
        form = AssignDirectorForm(request.POST, instance=center, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('owner_centers_list')
    else:
        # Pass user to form in GET (Hna fin knti nassiha)
        form = AssignDirectorForm(instance=center, user=request.user)
    
    return render(request, 'assign_director.html', {
        'form': form,
        'center': center
    })