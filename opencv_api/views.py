import os
import random
import string
import zipfile

import cv2
import numpy as np
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

# from drf_spectacular.utils import extend_schema
from api_server.settings import MEDIA_ROOT
from . import util_funcs as omr_utils
from .models import Student, OmrResult
from omr_checker import models as omr_checker_models
from .serializers import StudentNameSerializer, OmrResultSerializer
from . import serializers


class StudentView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Student.objects.all()

    serializer_class = StudentNameSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OmrResultView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = OmrResult.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = OmrResultSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        omr_answer = None
        omr_answer_roll = None
        omr_answer_set_code = None
        is_processed_res = False
        is_processed_roll = False
        is_processed_set = False

        if request.data['image_omr_region'] is not None and request.data['image_roll_set'] is not None and \
                request.data["question_count"] and request.data["roll_count"] is not None and \
                request.data["set_count"] is not None:

            try:

                fileByte1 = request.data['image_omr_region'].read()
                npimg1 = np.fromstring(fileByte1, np.uint8)
                omr_region_img = cv2.imdecode(npimg1, cv2.IMREAD_COLOR)

                fileByte2 = request.data['image_roll_set'].read()
                npimg2 = np.fromstring(fileByte2, np.uint8)
                roll_set_img = cv2.imdecode(npimg2, cv2.IMREAD_COLOR)

                if omr_region_img is not None:
                    omr_answer, c_img = omr_utils.get_omr_answers(omr_region_img, int(request.data["question_count"]))
                    if omr_answer is not None:
                        is_processed_res = True
                        request.data["is_processed_res"] = True
                        print("omr_answer: ", omr_answer)

                if roll_set_img is not None:
                    roll_img, set_img = omr_utils.divide_region(roll_set_img)

                    if roll_img is not None:
                        omr_answer_roll, c_img_roll = omr_utils.get_omr_answers_for_roll(roll_img, int(
                            request.data["roll_count"]))
                        if omr_answer_roll is not None:
                            is_processed_roll = True
                            request.data["is_processed_roll"] = True
                            roll_res = np.transpose(omr_answer_roll)
                            roll = ""
                            row = roll_res.shape[0]
                            col = roll_res.shape[1]

                            for i in range(row):
                                for j in range(col):
                                    if roll_res[i][j] == 1.0:
                                        roll += str(j)
                            print("omr_answer_roll: ", omr_answer_roll)

                    if set_img is not None:
                        omr_answer_set, c_img_set = omr_utils.get_omr_answers_for_set_code(set_img, int(
                            request.data["set_count"]))
                        if omr_answer_set_code is not None:
                            is_processed_set = True
                            request.data["is_processed_set"] = True
                            print("omr_answer_set: ", omr_answer_set)

                if omr_answer is not None and omr_answer_roll is not None and omr_answer_set is not None:
                    return Response({
                        "status": "success",
                        "omr_result": omr_answer.tolist(),
                        "Roll_process": omr_answer_roll.tolist(),
                        "Roll_Number": roll,
                        "Set_code_process": omr_answer_set.tolist()
                    }, status=status.HTTP_201_CREATED)
                else:
                    dir_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                    path = "./media/images/omr/" + dir_name
                    if not os.path.exists(path):
                        os.mkdir(path)
                    if not is_processed_res:
                        image_file_path_1 = os.path.join(MEDIA_ROOT, "images", "omr", dir_name, "omr_region_img.jpg")
                        cv2.imwrite(image_file_path_1, omr_region_img)
                    if not is_processed_roll:
                        image_file_path_2 = os.path.join(MEDIA_ROOT, "images", "omr", dir_name, "roll_img.jpg")
                        cv2.imwrite(image_file_path_2, roll_img)
                    if not is_processed_set:
                        image_file_path_3 = os.path.join(MEDIA_ROOT, "images", "omr", dir_name, "set_img.jpg")
                        cv2.imwrite(image_file_path_3, set_img)

                    return Response({
                        "status": "Invalid image, Please scan a proper image"
                    }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print("Exception", e)

        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class OmrScan(generics.CreateAPIView):
    queryset = OmrResult.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.OMRScanSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sheet_id = serializer.validated_data.get('omr_sheet_id')
            obj = get_object_or_404(omr_checker_models.OMRUpload, pk=sheet_id)
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
