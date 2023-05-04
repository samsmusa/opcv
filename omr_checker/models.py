import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models

from omr_checker.settings import lib_settings
from .mixins.models import TimeStampMixin


# Create your models here.


class OverwriteStorage(FileSystemStorage):
    def exists(self, name):
        exists = os.path.lexists(self.path(name))
        if exists:
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return False


def get_student_result_image_file_path(instance, filename):
    filename_provider_class = lib_settings.ANON_FILENAME_PROVIDER
    base_dir = lib_settings.ANON_MEDIA_DIR
    exam_id = instance.omr_sheet.exam_id
    section_id = instance.omr_sheet.section_id
    subject_id = instance.omr_sheet.subject_id

    filename_provider = filename_provider_class()
    filename_class = filename_provider.get_filename(filename)
    # file_name = os.path.splitext(filename_class)[0]
    # file_ext = os.path.splitext(filename_class)[1]
    _filename = f'{exam_id}/{section_id}/{subject_id}/"outputs"/{filename_class}'

    return os.path.join(base_dir, _filename)


def get_sheet_upload_file_path(instance, filename):
    filename_provider_class = lib_settings.ANON_FILENAME_PROVIDER
    base_dir = lib_settings.ANON_MEDIA_DIR
    exam_id = instance.exam_id
    section_id = instance.section_id
    subject_id = instance.subject_id

    filename_provider = filename_provider_class()
    filename_class = filename_provider.get_filename(filename)
    file_name = os.path.splitext(filename_class)[0]
    file_ext = os.path.splitext(filename_class)[1]
    print(file_ext)
    if file_name != 'result':
        try:
            file_name = int(file_name)
        except Exception as e:
            raise ValidationError('file name must be integer or result')
    _filename = f'{exam_id}/{section_id}/{subject_id}/"inputs"/{filename_class}'

    return os.path.join(base_dir, _filename)


class OMRUpload(TimeStampMixin):
    exam_id = models.IntegerField(null=False, blank=False)
    section_id = models.IntegerField(null=False, blank=False)
    subject_id = models.IntegerField(null=False, blank=False)
    exam_title = models.CharField(max_length=200, null=False, blank=False)
    section_title = models.CharField(max_length=200, null=False, blank=False)
    subject_title = models.CharField(max_length=200, null=False, blank=False)
    file = models.FileField(
        blank=False, null=False,
        storage=OverwriteStorage(),
        upload_to='files/zip',
        validators=[FileExtensionValidator(allowed_extensions=['zip'])]
    )

    # file = models.FileField(blank=False, null=False,
    #                             storage=OverwriteStorage(),
    #                             upload_to=get_anonymous_uploaded_file_path,
    #                             validators=[FileExtensionValidator(allowed_extensions=['zip'])])

    def __str__(self):
        return self.exam_title + self.file.name


class OMRResult(TimeStampMixin):
    omr_sheet = models.ForeignKey(OMRUpload, on_delete=models.CASCADE)
    file = models.FileField(
        blank=False,
        null=False,
        storage=OverwriteStorage(),
        upload_to='results/csv/',
        validators=[FileExtensionValidator(allowed_extensions=['csv'])]
    )


class StudentResult(TimeStampMixin):
    name = models.CharField(max_length=200)
    roll = models.IntegerField()
    exam = models.IntegerField()
    omr_result = models.ForeignKey(OMRResult, on_delete=models.CASCADE)
    omr_sheet = models.ForeignKey(OMRUpload, on_delete=models.CASCADE)
    marks = models.IntegerField()
    file = models.ImageField(
        upload_to=get_student_result_image_file_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])]
    )
