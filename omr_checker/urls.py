from django.urls import path
from . import views

urlpatterns = [
    path('result/', views.OmrResultView.as_view(), name='omr-result'),
]
