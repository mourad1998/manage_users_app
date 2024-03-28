from django.urls import path
from app_users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('users', views.userApi),  
    path('user/<int:user_id>', views.userApi),
    
    path('profiles', views.profileApi), 
    path('profile/<int:profile_id>', views.profileApi),  
    
    path('profile/', views.profileByUsernameApi),

]