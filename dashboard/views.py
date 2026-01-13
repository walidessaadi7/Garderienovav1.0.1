from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Center
from .forms import CenterCreationForm,DirectorCreationForm,AssignDirectorForm
from django.shortcuts import render, get_object_or_404
from .models import Center, Organization
from accounts.models import Educator,Director, User
from django.core.mail import send_mail #hadi mzal mkhdemti biha
from django.conf import settings
#-----------------------------------------------center__info---------------------------------------------------------------------------------
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
@login_required
def owner_centers_list(request):
    # 'select_related' kat-jib l-data dyal org u director f query whda (Performance)
    centers = Center.objects.filter(
        org__owner__user=request.user
    ).select_related('org', 'director', 'director__user')
    
    # Hna n-qdrou n-7sbo ch7al men center 3ando
    centers_count = centers.count()
    
    return render(request, 'centers_list.html', {
        'centers': centers,
        'centers_count': centers_count
    })
#---------------------------------------------------------diractor__info-----------------------------------------------------------------------
#hna dyal send email sir setting 3endak tensa
@login_required
def create_director_general(request):
    if request.method == 'POST':
        # Pass request.user bach n-rbeto l-director b l-owner
        form = DirectorCreationForm(request.POST, user=request.user)
        if form.is_valid():
            director = form.save()
            return redirect('owner_centers_list')
    else:
        form = DirectorCreationForm(user=request.user)
    
    return render(request, 'create_director.html', {'form': form})
    
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
        # Pass user to form in GET zebi hna finkenti nasiha
        form = AssignDirectorForm(instance=center, user=request.user)
    
    return render(request, 'assign_director.html', {
        'form': form,
        'center': center
    })
#---------------------------------------------------educator info-----------------------------------------------------------------
@login_required
def create_educator(request):
    # 1. Get l-Director object dyal had l-user li m-connecte daba
    # Ghadi n-asta3mlo get_object_or_404 bach ila makansh director t-tla3 404
    current_director = get_object_or_404(Director, user=request.user)

    if request.method == 'POST':
        # 2. Check: Wach had l-Director 3ndo Center m-assigné lih?
        # Hna kantsme3 l-field li smitou 'organization' f l-model dyalk aw center
        # 3la hsab l-error li tla3 lik: current_director.center
        try:
            director_center = current_director.center 
            if not director_center:
                raise AttributeError
        except AttributeError:
            messages.error(request, "Impossible d'ajouter un éducateur: Vous n'êtes assigné à aucun centre.")
            return redirect('owner_centers_list')

        # 3. Recuperation dyal l-data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        
        # 4. Create l-User
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            role_type='educator'
        )
        
        # 5. Create l-Educator linked to the Director's Center
        Educator.objects.create(
            user=new_user,
            manager=current_director,
            center=director_center, # Hna khda l-center dyal l-director login
            specialization=request.POST.get('specialization')
        )
        
        messages.success(request, f"L'éducateur {full_name} a été ajouté avec succès.")
        return redirect('educator_list')
        
    return render(request, 'create_educator.html')
@login_required
def educator_list(request):
    # Jib l-director li m-connecte
    current_director = get_object_or_404(Director, user=request.user)
    
    # Jib ga3 l-educators li taba3in lih (via manager field)
    educators = Educator.objects.filter(manager=current_director)
    
    return render(request, 'educator_list.html', {
        'educators': educators
    })