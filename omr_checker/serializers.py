from rest_framework import serializers


class OMRCheckSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200)
    question_count = serializers.IntegerField(max_value=60)


class OMRResultSerializer(serializers.Serializer):
    roll = serializers.IntegerField()
    marks = serializers.IntegerField()
