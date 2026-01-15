
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Center
from .forms import CenterCreationForm,DirectorCreationForm,AssignDirectorForm
from django.shortcuts import render, get_object_or_404
from .models import Center, Organization
from accounts.models import Educator,Director, User
from django.core.mail import send_mail #hadi mzal mkhdemti biha
from django.conf import settings
import csv
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from dashboard.models import Center, Child
from accounts.models import Parent, User
from django.db import transaction
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
def edit_educator(request, pk):
    # 1. Jib l-educator
    educator = get_object_or_404(Educator, pk=pk)
    # 2. Jib l-user li taba3 lih (bach l-ma3loumat t-ban f l-inputs)
    user_to_edit = educator.user

    if request.method == 'POST':
        # --- Update User Info ---
        user_to_edit.username = request.POST.get('username')
        user_to_edit.full_name = request.POST.get('full_name')
        user_to_edit.email = request.POST.get('email')
        
        # Password (ila dkhlo l-director)
        new_password = request.POST.get('password')
        if new_password:
            user_to_edit.set_password(new_password)
        
        user_to_edit.save()

        # --- Update Educator Info ---
        educator.specialization = request.POST.get('specialization')
        educator.save()

        return redirect('educator_list')

    # 3. Sift l-variables b-jouj l-template
    context = {
        'educator': educator,
        'user_to_edit': user_to_edit
    }
    return render(request, 'edit_educator.html', context)
# views.py
@login_required
def delete_educator(request, pk):
    # 1. Jib l-director li m-connecti daba
    current_director = get_object_or_404(Director, user=request.user)
    
    # 2. Jib l-educator li 3ndo had l-PK O kiy-manger-ih had l-director
    # Haka 7ta wa7ed may-qder imse7 educator dyal chi center akhor
    educator = get_object_or_404(Educator, pk=pk, manager=current_director)
    
    # 3. Mse7 l-user (ghadi imse7 m3ah l-educator automatique hit dayrin CASCADE)
    user_to_delete = educator.user
    user_to_delete.delete()
    
    return redirect('educator_list')
#----------------------------------------------child o parent dyalo---------------------------------

def import_children_csv(request):
    form = CSVUploadForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST" and form.is_valid():
        csv_file = form.cleaned_data["file"]
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        errors = []
        added_children = 0

        # Director's Center
        center = request.user.director.center

        with transaction.atomic():  # All or nothing
            for i, row in enumerate(reader, start=2):  # start=2 to count header
                email = row.get("parent_email")
                if not email:
                    errors.append(f"Line {i}: Missing parent email")
                    continue

                # Parent: create if not exists
                parent, created = Parent.objects.get_or_create(
                    user__email=email,
                    defaults={
                        "user": User.objects.create(
                            username=email,
                            email=email,
                            full_name=row.get("parent_full_name","No Name"),
                            role_type="parent"
                        ),
                        "home_address": row.get("parent_home_address",""),
                        "billing_reference": row.get("parent_billing_reference","")
                    }
                )

                # Child data validation
                try:
                    birth_date = datetime.strptime(row.get("child_birth_date",""), "%Y-%m-%d").date()
                except ValueError:
                    errors.append(f"Line {i}: Invalid birth date")
                    continue

                gender = row.get("child_gender")
                if gender not in ["M","F"]:
                    errors.append(f"Line {i}: Invalid gender (M/F)")
                    continue

                # Create Child
                Child.objects.create(
                    center=center,
                    parent=parent,
                    first_name=row.get("child_first_name",""),
                    last_name=row.get("child_last_name",""),
                    birth_date=birth_date,
                    gender=gender
                )
                added_children += 1

        if errors:
            for e in errors:
                messages.error(request, e)

        messages.success(request, f"{added_children} children imported successfully!")
        return redirect("import_children_csv")

    return render(request, "import_children.html", {"form": form})
