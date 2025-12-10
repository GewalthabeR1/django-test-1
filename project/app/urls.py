from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('redirect-home/', views.redirect_home, name='redirect_home'),
    path('redirect-post/<int:pk>/', views.redirect_to_post, name='redirect_to_post'),
]