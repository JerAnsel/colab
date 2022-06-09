from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static  
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('profile-page/<str:pk>/', views.profile, name="profile-page"),
    path('test', views.test, name='test'),
    path('images', views.images, name='images'),
    # path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room")
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  