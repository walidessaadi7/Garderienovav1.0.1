from django.urls import path
from . import views 
from accounts import views as accounts_views 
from .views import (
    create_center,
    center_success,
    center_info_view,
    owner_centers_list,
    create_director_general,
    assign_director_to_center,
    create_educator,
    educator_list,
    edit_educator,
    delete_educator,
    import_children_csv  
)

urlpatterns = [
    # Hna kan-asta3mlo accounts_views bash njbdo l-function li kayna f accounts app
    path('owner/', accounts_views.owner_dashboard, name='owner_dashboard'),
    path('center/create/', views.create_center, name='create_center'),
    path('center/success/<uuid:center_id>/', views.center_success, name='center_success'),
    path('center/details/<uuid:center_id>/', views.center_info_view, name='center_details'),
    path('my-centers/', views.owner_centers_list, name='owner_centers_list'),
    path('add-director/', views.create_director_general, name='add_director_general'),
    path('center/<uuid:center_id>/assign-director/', views.assign_director_to_center, name='assign_director'),
    path('educators/new/', views.create_educator, name='create_educator'),
    path('educators/', views.educator_list, name='educator_list'),
    path('educator/edit/<uuid:pk>/', views.edit_educator, name='edit_educator'),
    path('educator/delete/<uuid:pk>/', views.delete_educator, name='delete_educator'),
    path('import-children/', import_children_csv, name="import_children_csv"),
    path('parent/children/', views.children_list, name="children_list"),
     #--------group----------
    # path("groups/add/", group_add_view, name="group_add"),

]