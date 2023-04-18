from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(
    r"anonymous-upload",
    views.OMRFileUploadView,
    basename="OMR-upload",
)

router.register(
    r"class",
    views.ClassView,
    basename="class-view",
)
router.register(
    r"student",
    views.StudentView,
    basename="student-view",
)

urlpatterns = [
    path('result/', views.OmrResultView.as_view(), name='omr-result'),
    path('resultlist/', views.ResultList.as_view(), name='omr-result-list'),
    path('exam/', views.ExamView.as_view(), name='exam-result'),
    path("", include(router.urls)),
]
