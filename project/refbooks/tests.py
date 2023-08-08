from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from .models import Refbook


class RefbooksAPITest(APITestCase):
    def setUp(self) -> None:
        Refbook.objects.create(code="MS1", name=" ", description="")
        Refbook.objects.create(code="ICD-10", name=" -10", description="")

    def test_refbooks_with_date(self):
        resp = self.client.get(reverse('refbooks'))
        self.assertEquals(resp.status_code, HTTP_200_OK)
        content = resp.json()
        print(content)
        self.assertEquals(len(content.get("refbooks")), 2)
        self.assertTrue(
            {
                "refbooks": [
                    {
                        "id": "1",
                        "code": "MS1",
                        "name": " "
                    },
                    {
                        "id": "2",
                        "code": "ICD-10",
                        "name": " -10"
                    },
                ]
            } == content
        )
