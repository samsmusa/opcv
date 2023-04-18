import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from drf_file_upload.settings import lib_settings
from .mixins.models import TimeStampMixin

# Create your models here.

from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def exists(self, name):
        exists = os.path.lexists(self.path(name))
        if exists:
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return False


class Class(TimeStampMixin):
    name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return "name: {}".format(self.name)


class Student(TimeStampMixin):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    user_name = models.CharField(max_length=50, blank=False, unique=True)
    roll = models.IntegerField(blank=False)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return "first name: {}, last name: {}".format(self.first_name, self.last_name)


class Exam(TimeStampMixin):
    name = models.CharField(max_length=50)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return "name: {}".format(self.name)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png']
    formats = '/'.join(valid_extensions)
    if ext not in valid_extensions:
        raise ValidationError(f'File not supported! supported only {formats}')


def get_anonymous_uploaded_file_path(instance, filename):
    filename_provider_class = lib_settings.ANON_FILENAME_PROVIDER
    base_dir = lib_settings.ANON_MEDIA_DIR
    exam_id = instance.exam.id
    class_id = instance.exam.classes.id

    filename_provider = filename_provider_class()
    filename_class = filename_provider.get_filename(filename)
    file_name = os.path.splitext(filename_class)[0]
    file_ext = os.path.splitext(filename_class)[1]
    print(file_ext)
    if file_name != 'res':
        try:
            file_name = int(file_name)
        except Exception as e:
            raise ValidationError('file name must be integer or res')
    _filename = f'{exam_id}/{class_id}/inputs/{filename_class}'

    return os.path.join(base_dir, _filename)


class OMRUpload(TimeStampMixin):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False,
                            storage=OverwriteStorage(),
                            upload_to=get_anonymous_uploaded_file_path,
                            validators=[validate_file_extension])

    def __str__(self):
        return self.exam.name + self.file.name


class OMRResult(TimeStampMixin):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    mark = models.IntegerField()
    image = models.CharField(max_length=200, blank=True, null=True)
