from django.urls import path
from . import views # views dyal dashboard
from accounts import views as accounts_views # views dyal accounts

urlpatterns = [
    # Hna kan-asta3mlo accounts_views bash njbdo l-function li kayna f accounts app
    path('owner/', accounts_views.owner_dashboard, name='owner_dashboard'),
    path('center/create/', views.create_center, name='create_center'),
    path('center/success/<uuid:center_id>/', views.center_success, name='center_success'),
    path('center/details/<uuid:center_id>/', views.center_info_view, name='center_details'),
    path('my-centers/', views.owner_centers_list, name='owner_centers_list'),
    path('add-director/', views.create_director_general, name='add_director_general'),
    path('center/<uuid:center_id>/assign-director/', views.assign_director_to_center, name='assign_director'),
   
]