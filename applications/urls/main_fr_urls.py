from django.urls import path, include
from applications.urls import application_form_urls, admin_fr_urls

urlpatterns = [
    path("", include(application_form_urls)),
    path("admin/", include(admin_fr_urls)),
]
