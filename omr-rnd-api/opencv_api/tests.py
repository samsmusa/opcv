from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
# from django.test import TestCase

from .models import StudentName
from .serializers import StudentNameSerializer


class BaseViewTest(APITestCase):
    """This class defines the test suite for the bucketlist model."""
    client = APIClient()

    @staticmethod
    def create_student( first_name="", last_name=""):
        if first_name != "" and last_name != "":
            StudentName.objects.create(first_name=first_name, last_name=last_name)

    def setUp(self):
        """Define the test client and other test variables."""
        self.create_student("like glue", "sean paul")
        self.create_student("simple song", "konshens")
        self.create_student("love is wicked", "brick and lace")
        self.create_student("jam rock", "damien marley")


class GetStudentsListTest(BaseViewTest):

    def test_get_students_list(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            # reverse("students-list", kwargs={"version": "v1"})
            reverse("students-list")
        )
        # fetch the data from db
        expected = StudentName.objects.all()
        serialized = StudentNameSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

