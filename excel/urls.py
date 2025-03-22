from django.urls import path
from .views import *


urlpatterns = [
    path('send/', UserAPIVIEWriter.as_view(), name='user-detail'),
    path('get/', ExportUsersExcel.as_view(), name='get-user'),

    ]