import json

from django.test import TestCase, Client
from rest_framework import status

class TestCreateGenericObject(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_create_fails(self):
        data = {'city': 'bad city'}
        response = self.client.post('/synthetic/', content_type='application/json',
            data=json.dumps(data))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self):
        data = {'city': 'London', 'temperature': 18}
        response = self.client.post('/synthetic/', content_type='application/json',
            data=json.dumps(data))

        assert response.status_code == status.HTTP_201_CREATED


class TestUpdateGenericObject(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

        data = {'city': 'London', 'temperature': 18}
        response = self.client.post('/synthetic/', content_type='application/json',
            data=json.dumps(data))

        self.obj = response.json()

    def test_update_succeeds(self):
        pk = self.obj['id']
        data = {'city': 'London', 'temperature': 18}
        response = self.client.patch('/synthetic/detail/{}/'.format(pk),
            content_type='application/json', data=json.dumps(data))

        assert response.status_code == status.HTTP_202_ACCEPTED

    def test_update_fails(self):
        data = {'city': 'nowhere'}

        pk = self.obj['id']
        response = self.client.patch('/synthetic/detail/{}/'.format(pk),
            content_type='application/json', data=json.dumps(data))

        #import rpdb;rpdb.set_trace()
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestListGenericModel(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

        data = {'city': 'London', 'temperature': 18}
        response = self.client.post('/synthetic/', content_type='application/json',
            data=json.dumps(data))

        self.obj = response.json()

    def test_list(self):
        response = self.client.get('/synthetic/')
        obj = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert int(obj['total'] == 1)

        for pk in obj['items'].keys():
            assert pk == '1'
            item = obj['items'][pk]
            assert item['city']
            assert item['temperature']
            assert item['taken_at']


class TestDeleteGenericObject(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.data = {'city': 'London', 'temperature': 18}

        response = self.client.post('/synthetic/', content_type='application/json',
            data=json.dumps(self.data))
        self.obj = response.json()

    def test_delete(self):
        response = self.client.delete('/synthetic/detail/{}/'.format(self.obj['id']))
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = self.client.get('/synthetic/')
        obj = response.json()
        assert self.obj['id'] not in obj
