from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from .models import Refbook, RefbookVersion, RefbookElement


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


class RefbookElementsAPITest(APITestCase):
    def setUp(self) -> None:
        Refbook.objects.create(code="MS1", name=" ", description="")
        Refbook.objects.create(code="ICD-10", name=" -10", description="")

        RefbookVersion.objects.create(refbook_id='1', version='1.0', date="2023-08-09")
        RefbookVersion.objects.create(refbook_id='2', version='1.0', date="2023-01-07")
        RefbookVersion.objects.create(refbook_id='2', version='1.1', date="2023-08-09")
        RefbookVersion.objects.create(refbook_id='2', version='1.2', date="2023-12-08")

        RefbookElement.objects.create(version_id='1', code='c1', value='123')
        RefbookElement.objects.create(version_id='2', code='b1', value='1234')
        RefbookElement.objects.create(version_id='3', code='b2', value='12345')
        RefbookElement.objects.create(version_id='3', code='b2-1', value='12345-1')
        RefbookElement.objects.create(version_id='4', code='b3', value='123456')

    def test_refbook_elements(self):
        resp = self.client.get(reverse('refbook_elements', kwargs={"id": 2}))
        self.assertEquals(resp.status_code, HTTP_200_OK)
        content = resp.json()
        print(content)
        self.assertEquals(len(content.get("elements")), 2)
        self.assertTrue(
            {
                'elements': [
                    {'code': 'b2', 'value': '12345'},
                    {'code': 'b2-1', 'value': '12345-1'},
                ]
            } == content
        )

    def test_refbook_elements_with_version(self):
        resp = self.client.get(reverse('refbook_elements', kwargs={"id": 2}), data={'version': 1.0})
        self.assertEquals(resp.status_code, HTTP_200_OK)
        content = resp.json()
        print(content)
        self.assertEquals(len(content.get("elements")), 1)
        self.assertTrue(
            {
                'elements': [
                    {'code': 'b1', 'value': '1234'},
                ]
            } == content
        )
