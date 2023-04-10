from django.urls import path
from .views import StudentView, OmrResultView

urlpatterns = [
    path('students/', StudentView.as_view(), name='students'),
    path('omr-sheet/', OmrResultView.as_view(), name='omr-sheet'),
]
