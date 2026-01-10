from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Login Page (kat-asta3mel template login.html li sayebna)
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # 2. Logout Action
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 3. L-Controller (Redirection Logic)
    # Hada hwa l-url li khass t-dir f LOGIN_REDIRECT_URL f settings.py
    path('dashboard/redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/director/', views.director_dashboard, name='director_dashboard'),
    path('dashboard/educator/', views.educator_dashboard, name='educator_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
 

   
]