from django.urls import path
from .views import (
    read_notify,
)

app_name = 'notification'

urlpatterns = [
    path('read_notify', read_notify),
]
