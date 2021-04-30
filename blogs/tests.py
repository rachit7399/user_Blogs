from authentication.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from blogs.models import Tags

class BlogsTest(APITestCase):

    fixtures = ['dump.json']
    
    def test_create_blog(self):
        data = File(open('C://Users//Shilpa Bundela//Desktop//Rachit//Projects//Django/sampleimgtiger.jpeg', 'rb'))
        upload_file = SimpleUploadedFile('data.dump', data.read(),content_type='multipart/form-data')
        self.tags = Tags.objects.get_or_create(name = "python")
        user = User.objects.get_or_create(email = "abc@gmail.com")[0]
        _data = {
            "user" : user.uid,
            "title": "demo titile",
            "content": "hello this is my Demo blog",
            "tags": self.tags[0].uid,
            "media": upload_file
        }
        _response = self.client.post("/blogs/",
                                     data=_data,
                                     format='multipart')

        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_201_CREATED)

    def test_list_blog(self):
        
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NzY1NTU4LCJqdGkiOiI4YzYyYzVlMDRjMzk0NzJlYjNmMGMyZWJjMWE4Y2E3NyIsInVpZCI6ImUzNjczNDk5LWNlZGMtNDY4ZC1iNDVlLWY2ZDA4M2M3ZGMyYSJ9.NPIcAU7dPGsLm35xoTBMdllmm332Z9VifWZanIMI81k"
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        _response = self.client.get("/blogs/", format='json')
        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_200_OK)


    def test_retrieve(self):
        _response = self.client.get("/blogs/6188be91-2044-4acb-b110-bb76968db3af/", format='json')
        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_200_OK)

    def test_update(self):
        user = User.objects.get_or_create(email = "abc@gmail.com")[0]
        _data = {
            "user" : user.uid,
            "title": "updated title",
            "content": "hello this is my updated Demo blog",
        }
        _response = self.client.put("/blogs/6188be91-2044-4acb-b110-bb76968db3af/", data=_data, format='multipart')
        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_200_OK)

    def test_all_activity(self):
        _response = self.client.get("/blogs/e3673499-cedc-468d-b45e-f6d083c7dc2a/all_activity/", format='json')
        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_200_OK)


    def test_all_leaderboard(self):
        _response = self.client.get("/blogs/learderboard/", format='json')
        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_200_OK)

    def test_comment(self):
        # import pdb; pdb.set_trace()
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NzY1NTU4LCJqdGkiOiI4YzYyYzVlMDRjMzk0NzJlYjNmMGMyZWJjMWE4Y2E3NyIsInVpZCI6ImUzNjczNDk5LWNlZGMtNDY4ZC1iNDVlLWY2ZDA4M2M3ZGMyYSJ9.NPIcAU7dPGsLm35xoTBMdllmm332Z9VifWZanIMI81k"
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            "comment": "nice blog"
        }
        _response = client.post("/blogs/589d40e4-04f3-4211-ad64-4e01511209b7/comment/", data = data)
        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_200_OK)

    def test_like(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NzY1NTU4LCJqdGkiOiI4YzYyYzVlMDRjMzk0NzJlYjNmMGMyZWJjMWE4Y2E3NyIsInVpZCI6ImUzNjczNDk5LWNlZGMtNDY4ZC1iNDVlLWY2ZDA4M2M3ZGMyYSJ9.NPIcAU7dPGsLm35xoTBMdllmm332Z9VifWZanIMI81k"
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        _response = client.get("/blogs/589d40e4-04f3-4211-ad64-4e01511209b7/like/")
        _data = _response.json()
        self.assertEqual(_response.status_code, status.HTTP_200_OK)
    