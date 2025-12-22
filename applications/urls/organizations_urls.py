from django.urls import path, include
from applications.urls import main_fr_urls
from applications.views import main_fr_views, admin_views, organizations_views

urlpatterns = [
    path("organizations/", organizations_views.organizations, name="organizations"),
]
