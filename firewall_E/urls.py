from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from .scripts.extraction import extraction_policy
from .views import *

urlpatterns = [
    
    url(r'^extraction_policy',extraction_policy.as_view(),name="extraction_policy"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)