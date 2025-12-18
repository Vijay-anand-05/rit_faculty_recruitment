from django.urls import path, include
from applications.urls import main_fr_urls
from applications.views import main_fr_views, admin_views

urlpatterns = [
   path("admin-login/", admin_views.admin_login, name="admin_login"),
   path("admin-dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),
   path("admin-logout/", admin_views.admin_logout, name="admin_logout"),

   path("admin-home/", main_fr_views.admin_home, name="admin_home"),
   path("logs/", admin_views.logs, name="logs"),
   path("logs/admin-logs/", admin_views.admin_logs, name="admin_logs"),
]
