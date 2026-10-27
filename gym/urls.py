
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.add_member, name='add_member'),

    path(
        'members/<int:member_id>/edit/',
        views.edit_member,
        name='edit_member',
    ),

    path(
        'members/<int:member_id>/delete/',
        views.delete_member,
        name='delete_member',
    ),
]
