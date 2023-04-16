from rest_framework import serializers
from . import models


class StudentNameSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""
        model = models.Student
        fields = ('first_name', 'last_name', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class OmrResultSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Metaclass to map serializer's fields with the model fields."""
        model = models.OmrResult
        fields = ('id', 'image_path', 'is_processed', 'question_count', 'omr_type', 'remarks', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')

