from django.urls import path, include, re_path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
# router.register(
#     r"anonymous-upload",
#     views.OMRFileUploadView,
#     basename="OMR-upload",
# )
#
# router.register(
#     r"class",
#     views.ClassView,
#     basename="class-view",
# )
# router.register(
#     r"student",
#     views.StudentView,
#     basename="student-view",
# )
router.register(
    r"upload-sheet",
    views.SheetUpload,
    basename="sheet-upload",
)

urlpatterns = [
    # path('api/result/', views.OmrResultView.as_view(), name='omr-result'),
    # path('api/resultlist/', views.ResultList.as_view(), name='omr-result-list'),
    # path('api/exam/', views.ExamView.as_view(), name='exam-result'),
    path('api/exam-list/', views.ExamList.as_view(), name='exam-list'),
    # path('api/upload-sheet/', views.SheetUpload.as_view(), name='sheet-upload'),
    re_path(r'^api/section-list/(?P<temp_exam_master_id>.+)/$', views.SectionList.as_view(), name='section-list'),
    re_path(r'^api/subject-list/(?P<temp_exam_master_id>.+)/$', views.SubjectList.as_view(), name='subject-list'),
    path("api/", include(router.urls)),

    path('', views.new, name='new'),
    path('exam/', views.exam, name='exm'),
    path('results/', views.exam, name='result'),
    path('scan/', views.exam, name='scan'),
]
