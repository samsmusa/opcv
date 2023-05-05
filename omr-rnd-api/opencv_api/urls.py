from django.urls import path

from .views import StudentView, OmrResultView, new, exam, OmrScan

urlpatterns = [
    path('api/students/', StudentView.as_view(), name='students'),
    path('api/omr-sheet/', OmrResultView.as_view(), name='omr-sheet'),
    path('api/omr-scan/', OmrScan.as_view(), name='omr-scan'),
    # path('', new, name='new'),
    # path('exam/', exam, name='exm'),
    # path('results/', exam, name='result'),
    # path('scan/', exam, name='scan'),
]
