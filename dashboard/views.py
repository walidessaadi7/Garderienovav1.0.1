from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Center
from .forms import CenterCreationForm
from django.shortcuts import render, get_object_or_404
from .models import Center, Organization

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