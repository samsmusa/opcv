import mimetypes

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from drf_file_upload.serializers import UploadFileValidationMixin
from . import models


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Class
        fields = ["id", "name"]
        read_only_fields = ["id"]


class StudentSerializer(serializers.ModelSerializer):
    class_name = ClassSerializer(read_only=True)

    class Meta:
        model = models.Student
        fields = ["id", "first_name", "last_name", "user_name", "roll", "class_name"]
        read_only_fields = ["id"]


class StudentSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = models.Student
        fields = ["id", "first_name", "last_name", "user_name", "roll", "class_name"]
        read_only_fields = ["id"]



class ExamSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = models.Exam
        fields = ["id", "name", "classes", "students"]
        read_only_fields = ["id"]


class ExamSerializerGet(serializers.ModelSerializer):
    classes = ClassSerializer(read_only=True)
    students = StudentSerializer(read_only=True, many=True)

    class Meta:
        model = models.Exam
        fields = ["id", "name", "classes", "students"]
        read_only_fields = ["id"]


class OMRCheckSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    class_id = serializers.IntegerField()
    question_count = serializers.IntegerField(max_value=60)


class OMRResultSerializer(serializers.Serializer):
    roll = serializers.IntegerField()
    marks = serializers.IntegerField()



class ExamSerializerForOmr(serializers.ModelSerializer):
    classes = ClassSerializer(read_only=True)

    class Meta:
        model = models.Exam
        fields = ["id", "name", "classes"]
        read_only_fields = ["id"]


class OMRUploadFileSerializer(UploadFileValidationMixin, serializers.ModelSerializer):
    exam_id = serializers.IntegerField(write_only=True)
    exam = ExamSerializerForOmr(read_only=True)

    class Meta:
        model = models.OMRUpload
        fields = ["id", "file", "exam", "created_at", "updated_at", "exam_id"]
        read_only_fields = ["id", "created_at", "updated_at"]


class OMRResultSerializerFilter(serializers.ModelSerializer):
    student = StudentSerializer()
    exam = ExamSerializerForOmr()
    class Meta:
        model = models.OMRResult
        fields = "__all__"

