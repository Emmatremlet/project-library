
from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),
    path('members/', views.member_list, name='member_list'),
    path('borrow/', views.borrow_create, name='borrow_create'),
]

'''
path('members/new/', views.member_create, name='member_create'),
path('members/<int:pk>/edit/', views.member_update, name='member_update'),
path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),


''',