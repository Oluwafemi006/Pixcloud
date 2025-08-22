from django.urls import path
from . import views
from .views import ImageListView, ImageDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ImageListView.as_view(), name='gallery-home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gallery/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('upload/', views.upload_image, name='upload'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    path('image/<int:pk>/delete/', views.delete_image, name='image-delete'),
    path('category/<int:category_id>/', views.category_images, name='category-images'),
]