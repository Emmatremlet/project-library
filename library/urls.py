
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('borrow/', views.borrow_create, name='borrow_create'),
    path('<int:pk>/edit/', views.member_update, name='member_update'),
    path('<int:pk>/delete/', views.member_delete, name='member_delete'),
    path('borrow_delete/<int:pk>/', views.borrow_delete, name='borrow_delete'),
    path('borrow_return/<int:pk>/', views.borrow_return, name='borrow_return'),
    path('add_media/', views.add_media, name='add_media'),


]