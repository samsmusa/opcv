import os
import zipfile

import pandas as pd
import requests
from django.db import transaction, DatabaseError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render

from django.conf import settings
from pathlib import Path
from contextlib import closing
from zipfile import ZipFile

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import viewsets
from . import serializers
from . import models
from src.entry import entry_point


def entry_point_for_args(args):
    data = None
    for root in args["input_paths"]:
        data = entry_point(
            Path(root),
            args,
        )
    return data


# Create your views here.
# def get_input_output_path(data):
#     class_id = data.get("class_id")
#     exam_id = data.get("exam_id")
#     _exam = get_object_or_404(models.Exam, pk=exam_id)
#     _class = get_object_or_404(models.Class, pk=class_id)
#     exam_id = _exam.id
#     class_id = _class.id
#     file = f"{exam_id}/{class_id}/inputs/"
#     output = f"{exam_id}/{class_id}/outputs/"
#     return file, output, _exam, _class
#
#
# class OmrResultView(mixins.CreateModelMixin, generics.GenericAPIView):
#     # parser_classes = (MultiPartParser, FormParser)
#     serializer_class = serializers.OMRCheckSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             if serializer.is_valid():
#                 file, outfile, _exam, _class = get_input_output_path(serializer.validated_data)
#                 question_count = serializer.validated_data.get("question_count")
#                 data = entry_point_for_args(
#                     {'input_paths': [f'{settings.MEDIA_ROOT}/files/{file}'],
#                      'output_dir': f'{settings.MEDIA_ROOT}/files/{outfile}',
#                      'autoAlign': True,
#                      'setLayout': False}
#                 )
#
#                 df = pd.DataFrame(data).iloc[:question_count, :].astype(str)
#                 s = df.pop('res')
#
#                 def compare_to_series(col, series):
#                     return (series.values == col).sum().astype(int)
#
#                 result = df.apply(lambda x: compare_to_series(x, s), axis=0)
#
#                 with transaction.atomic():
#                     omr_results = []
#                     for roll, mark in result.items():
#                         _student = get_object_or_404(models.Student, roll=roll)
#                         old = models.OMRResult.objects.filter(exam=_exam, student=_student).first()
#                         if old:
#                             old.delete()
#                         omr_results.append(models.OMRResult(exam=_exam, student=_student, mark=mark,
#                                                             image=f'files/{outfile}/CheckedOMRs/{roll}.jpg'))
#
#                     models.OMRResult.objects.bulk_create(omr_results)
#
#                 response = [{'roll': roll, 'marks': mark} for roll, mark in result.items()]
#                 serialized_data = serializers.OMRResultSerializer(data=response, many=True)
#                 if serialized_data.is_valid():
#                     return Response(serialized_data.data, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             return Response({"status": "failed", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class OMRFileUploadView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
#     parser_class = [FileUploadParser, MultiPartParser]
#     permission_classes = []
#     serializer_class = serializers.OMRUploadFileSerializer
#
#     def get_queryset(self):
#         return models.OMRUpload.objects.all()
#
#
# class ExamView(generics.ListCreateAPIView):
#
#     def get_queryset(self):
#         return models.Exam.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ['POST']:
#             return serializers.ExamSerializerPost
#         return serializers.ExamSerializerGet
#
#
# class ClassView(ModelViewSet):
#     serializer_class = serializers.ClassSerializer
#
#     def get_queryset(self):
#         return models.Class.objects.all()
#
#
# class StudentView(ModelViewSet):
#
#     # parser_classes = (FormParser,)
#     def get_serializer_class(self):
#         if self.request.method in ['POST']:
#             return serializers.StudentSerializerPost
#         return serializers.StudentSerializer
#
#     def get_queryset(self):
#         return models.Student.objects.all()
#
#
# class ResultList(generics.ListAPIView):
#     queryset = models.OMRResult.objects.all()
#     serializer_class = serializers.OMRResultSerializerFilter
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['exam', 'student']


class SheetUpload(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.SheetUploadSerializer
    queryset = models.OMRUpload.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject_id = serializer.validated_data.get('subject_id')
        section_id = serializer.validated_data.get('section_id')
        exam_id = serializer.validated_data.get('exam_id')

        # Check if the zip file contains a 'result' file
        contain_result = False
        with ZipFile(serializer.validated_data['file']) as archive:
            file_names = archive.namelist()
            count = len(file_names)
            for file_name in file_names:
                base_name = os.path.basename(file_name)
                if os.path.splitext(base_name)[0] == 'result':
                    contain_result = True
                    break

        # Check if the total number of files in the zip file matches the number of students
        response = self.get_students(subject_id, section_id, exam_id)
        student_count = len(response['data'])
        if student_count != count - 1:
            raise ValidationError(
                f"Total student for this config is {student_count}, but your file contains only {count - 1} student "
                f"OMR sheet")

        if not contain_result:
            raise ValidationError("zip file doesn't contain any 'result' name file!")

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def get_students(subject_id, section_id, exam_id):
        url = f"https://www.jgcbd.edu.bd/api/get-all-students?temp_exam_master_id={exam_id}&section_id={section_id}&subject_id={subject_id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValidationError('No student found')
        return response.json()

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         data = serializer.validated_data
    #         url = 'https://www.jgcbd.edu.bd/api/get-exam-name-lists'
    #         file = data['file']
    #         exam_id = data['exam_id']
    #         all_exam = requests.get(url).json()
    #         with zipfile.ZipFile(file, 'r') as zip_ref:
    #             zip_ref.extractall('folder name')
    #             kl = zip_ref.namelist()
    #         return Response({'detail': 'ok', 'data': all_exam}, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamList(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        url = 'https://www.jgcbd.edu.bd/api/get-exam-name-lists'
        all_exam = requests.get(url).json()
        return Response(all_exam, status=status.HTTP_200_OK)


class SectionList(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        exam_id = self.kwargs['temp_exam_master_id']
        url = f'https://www.jgcbd.edu.bd/api/get-sections?temp_exam_master_id={exam_id}'
        all_exam = requests.get(url)
        if all_exam.status_code == 200:
            return Response(all_exam.json(), status=status.HTTP_200_OK)
        return Response({"success": False,
                         "code": status.HTTP_404_NOT_FOUND,
                         "msg": "Failed"}, status=status.HTTP_404_NOT_FOUND)


class SubjectList(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        exam_id = self.kwargs['temp_exam_master_id']
        url = f'https://www.jgcbd.edu.bd/api/get-subjects?temp_exam_master_id={exam_id}'
        all_exam = requests.get(url)

        if all_exam.status_code == 200:
            data = all_exam.json()
            if data is None:
                return Response({"success": True,
                                 "code": status.HTTP_200_OK,
                                 "msg": "Success", 'data': []}, status=status.HTTP_200_OK)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"success": False,
                         "code": status.HTTP_404_NOT_FOUND,
                         "msg": "Failed"}, status=status.HTTP_404_NOT_FOUND)


class OmrScan(generics.CreateAPIView):
    queryset = models.OMRUpload.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.OMRScanSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sheet_id = serializer.validated_data.get('omr_sheet_id')
            obj = get_object_or_404(models.OMRUpload, pk=sheet_id)
            file = obj.file.open()

            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall('folder_name')
                kl = zip_ref.namelist()
            print(file.name)
            return Response({"id": serializer.validated_data.get('omr_sheet_id')}, status=status.HTTP_200_OK)


def new(request):
    return render(request, 'New/index.html', {})


def exam(request):
    return render(request, 'New/index.html', {})
