from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static  
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('project/<str:pk>', views.project, name='project'),
    path('room/<str:pk>/<str:public>', views.room, name='room'),
    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    path('profile-page/<str:pk>/', views.profile, name="profile-page"),
    path('test', views.test, name='test'),
    path('images', views.images, name='images'),
    # path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room")
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  