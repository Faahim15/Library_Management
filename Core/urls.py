
from django.urls import path 
from . views import RegistrationView,UserLoginView,CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static 
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'), 
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
   
] 
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
