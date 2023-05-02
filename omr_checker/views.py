import zipfile

import pandas as pd
import requests
from django.db import transaction, DatabaseError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.conf import settings
from pathlib import Path

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
def get_input_output_path(data):
    class_id = data.get("class_id")
    exam_id = data.get("exam_id")
    _exam = get_object_or_404(models.Exam, pk=exam_id)
    _class = get_object_or_404(models.Class, pk=class_id)
    exam_id = _exam.id
    class_id = _class.id
    file = f"{exam_id}/{class_id}/inputs/"
    output = f"{exam_id}/{class_id}/outputs/"
    return file, output, _exam, _class


class OmrResultView(mixins.CreateModelMixin, generics.GenericAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.OMRCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                file, outfile, _exam, _class = get_input_output_path(serializer.validated_data)
                question_count = serializer.validated_data.get("question_count")
                data = entry_point_for_args(
                    {'input_paths': [f'{settings.MEDIA_ROOT}/files/{file}'],
                     'output_dir': f'{settings.MEDIA_ROOT}/files/{outfile}',
                     'autoAlign': True,
                     'setLayout': False}
                )

                df = pd.DataFrame(data).iloc[:question_count, :].astype(str)
                s = df.pop('res')

                def compare_to_series(col, series):
                    return (series.values == col).sum().astype(int)

                result = df.apply(lambda x: compare_to_series(x, s), axis=0)

                with transaction.atomic():
                    omr_results = []
                    for roll, mark in result.items():
                        _student = get_object_or_404(models.Student, roll=roll)
                        old = models.OMRResult.objects.filter(exam=_exam, student=_student).first()
                        if old:
                            old.delete()
                        omr_results.append(models.OMRResult(exam=_exam, student=_student, mark=mark,
                                                            image=f'files/{outfile}/CheckedOMRs/{roll}.jpg'))

                    models.OMRResult.objects.bulk_create(omr_results)

                response = [{'roll': roll, 'marks': mark} for roll, mark in result.items()]
                serialized_data = serializers.OMRResultSerializer(data=response, many=True)
                if serialized_data.is_valid():
                    return Response(serialized_data.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status": "failed", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OMRFileUploadView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    parser_class = [FileUploadParser, MultiPartParser]
    permission_classes = []
    serializer_class = serializers.OMRUploadFileSerializer

    def get_queryset(self):
        return models.OMRUpload.objects.all()


class ExamView(generics.ListCreateAPIView):

    def get_queryset(self):
        return models.Exam.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return serializers.ExamSerializerPost
        return serializers.ExamSerializerGet


class ClassView(ModelViewSet):
    serializer_class = serializers.ClassSerializer

    def get_queryset(self):
        return models.Class.objects.all()


class StudentView(ModelViewSet):

    # parser_classes = (FormParser,)
    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return serializers.StudentSerializerPost
        return serializers.StudentSerializer

    def get_queryset(self):
        return models.Student.objects.all()


class ResultList(generics.ListAPIView):
    queryset = models.OMRResult.objects.all()
    serializer_class = serializers.OMRResultSerializerFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam', 'student']


class SheetUpload(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.SheetUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            url = 'https://www.jgcbd.edu.bd/api/get-exam-name-lists'
            file = data['file']
            exam_id = data['exam_id']
            all_exam = requests.get(url).json()
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall('folder name')
                kl = zip_ref.namelist()
            return Response({'detail': 'ok', 'data': all_exam}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
