import imp
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from .scripts.homepage import HomePageView,Ip_and_device_type

# from .scripts import inventoryCollection
from .views import *


urlpatterns = [
    
    url(r'^HomePageView',HomePageView.as_view(),name="HomePageView"),
    url(r'^Ip_and_device_type',Ip_and_device_type,name='Ip_and_device_type'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



