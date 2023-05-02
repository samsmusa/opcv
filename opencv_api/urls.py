from django.urls import path

from omr_checker.views import SheetUpload
from .views import StudentView, OmrResultView

urlpatterns = [
    path('students/', StudentView.as_view(), name='students'),
    path('omr-sheet/', OmrResultView.as_view(), name='omr-sheet'),
    path('omr-upload/', SheetUpload.as_view(), name='omr-sheet-upload'),
]
