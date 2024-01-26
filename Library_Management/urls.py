
from django.contrib import admin
from django.urls import path,include 
from Core.views import Home 
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include("Core.urls")),
    path('books/', include("BookApp.urls")),
    path('',Home.as_view(), name='homepage'),
    path('category/<slug:category_slug>/', Home.as_view(), name='category_wise_post'),
] 
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
