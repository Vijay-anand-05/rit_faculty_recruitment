from django.urls import path, include
from applications.urls import main_fr_urls
from applications.views import faculty_data_views

urlpatterns = [
    path('faculty_data/', faculty_data_views.faculty_data, name='faculty_data'),
    path('faculty_data/update/', faculty_data_views.update_faculty_data, name='update_faculty_data'),
]
