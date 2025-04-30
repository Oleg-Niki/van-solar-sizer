from django.urls import path
from . import views

urlpatterns = [
    path('design/', views.design_request, name='design_request'),
]
