from django.db import models


# Create your models here.


class Student(models.Model):
    """This class represents the student-name model."""
    first_name = models.CharField(max_length=255, blank=False, unique=False)
    last_name = models.CharField(max_length=255, blank=False, unique=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return "first name: {}, last name: {}".format(self.first_name, self.last_name)


class OmrResult(models.Model):
    """This class represents the omr-result model."""

    # image_path = models.ImageField(upload_to="images/omr", null=False, blank=False)
    image_path = models.CharField(max_length=255, blank=False, null=False)
    is_processed = models.BooleanField(default=False)
    question_count = models.IntegerField(default=50, blank=False, null=False)
    omr_type = models.CharField(choices=[("cropped", "Cropped"), ("full", "Full")], max_length=15, default="cropped")
    remarks = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return "is_processed name: {}, remarks: {}, image: {}".format(self.is_processed, self.remarks, self.image)

    class Meta:
        ordering = ('date_created',)
