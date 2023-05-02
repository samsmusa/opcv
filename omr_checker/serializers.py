import mimetypes
from pathlib import Path

from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from . import models
from .settings import lib_settings


class UploadFileValidationMixin:
    def validate_file(self, value):
        if not self.is_supported_file(value.name):
            raise ValidationError("invalid-file-format")
        if not self.respects_filesize_limit(value.size):
            raise ValidationError("file-too-large")
        return value

    def is_supported_file(self, file):
        allowed_formats = lib_settings.ALLOWED_FORMATS

        if not allowed_formats:
            return True

        mimetype = mimetypes.guess_type(file)[0]
        return mimetype in allowed_formats

    def respects_filesize_limit(self, size):
        max_file_size = lib_settings.MAX_FILE_SIZE
        if not max_file_size:
            return True
        return size <= max_file_size


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


class SheetUploadSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['zip'])])
