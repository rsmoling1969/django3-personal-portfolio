from django.urls import path
from CoblentzNumbers import views

app_name = 'CoblentzNumbers'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:shift_id>/', views.shift_detail, name='shift_detail'),
    path('create/', views.create_shift, name='create_shift'),
    path('current/', views.all_shifts, name='all_shifts'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('', views.home, name='home'),
    path('login/', views.loginuser, name='loginuser'),
]