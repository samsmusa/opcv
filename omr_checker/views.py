import pandas as pd
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from django.conf import settings
from pathlib import Path
# from drf_spectacular.utils import extend_schema
from . import serializers
from src.entry import entry_point

import sys

print(sys.path)


# from src import entry
# from src.entry import entry_point
#
#
def entry_point_for_args(args):
    data = None
    for root in args["input_paths"]:
        data = entry_point(
            Path(root),
            args,
        )
    return data


# Create your views here.


class OmrResultView(mixins.CreateModelMixin, generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.OMRCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                filename = serializer.validated_data.get("content")
                question_count = int(serializer.validated_data.get("question_count"))
                filenames = filename.split('--')
                file = '/'.join(filenames) + '/inputs/'
                outfile = '/'.join(filename.split('--'))

                data = entry_point_for_args(
                    {'input_paths': [f'{settings.MEDIA_ROOT}/files/{file}'],
                     'output_dir': f'{settings.MEDIA_ROOT}/files/{outfile}/outputs',
                     'autoAlign': True,
                     'setLayout': False}
                )

                df = pd.DataFrame(data).iloc[:question_count, :].astype(str)
                s = df.pop('res')

                def compare_to_series(col, series):
                    return (series.values == col).sum().astype(int)

                result = df.apply(lambda x: compare_to_series(x, s), axis=0)
                response = [{'roll': roll, 'marks': mark} for roll, mark in result.items()]
                serialized_data = serializers.OMRResultSerializer(data=response, many=True)
                if serialized_data.is_valid():
                    return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "failed", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
