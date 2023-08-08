from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from .models import Refbook, RefbookVersion


class RefbooksAPITest(APITestCase):
    def setUp(self) -> None:
        Refbook.objects.create(code="MS1", name=" ", description="")
        Refbook.objects.create(code="ICD-10", name=" -10", description="")
        Refbook.objects.create(code="ICD-12", name=" -12", description="")
        RefbookVersion.objects.create(refbook_id='1', version='1.0', date="2023-09-08")
        RefbookVersion.objects.create(refbook_id='2', version='1.0', date="2023-01-07")
        RefbookVersion.objects.create(refbook_id='2', version='1.1', date="2023-05-08")
        RefbookVersion.objects.create(refbook_id='3', version='0.1', date="2023-01-01")

    def test_refbooks(self):
        resp = self.client.get(reverse('refbooks'))
        self.assertEquals(resp.status_code, HTTP_200_OK)
        content = resp.json()
        print(content)
        self.assertEquals(len(content.get("refbooks")), 3)
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
                    {
                        'id': '3',
                        'code': 'ICD-12',
                        'name': ' -12'
                    },
                ]
            } == content
        )

    def test_refbooks_with_date(self):
        resp = self.client.get(reverse('refbooks'), data={"date": "2023-05-08"})
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
