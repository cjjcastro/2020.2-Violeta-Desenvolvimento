import json
from rest_framework.test import APITestCase
from rest_framework import status
from .models import (CategoriaViolencia, ContatoViolencia,
                     Questionario, ContatoQuestionario)
from .serializers import (CategoriaViolenciaSerializer,
                          ContatoViolenciaSerializer,
                          QuestionarioSerializer,
                          ContatoQuestionarioSerializer)


class CategoriaViolenciaTestCase(APITestCase):
    def setUp(self):
        self.cat1 = CategoriaViolencia.objects.create(
            nome_categoria='TESTE', ds_categoria='TESTE')

    def testPost(self):
        data = {
            'nome_categoria': 'NOME TESTE',
            'ds_categoria': 'DS TESTE'
        }
        response = self.client.post('/api/categoria-violencia/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testGet(self):
        # get API response
        response = self.client.get('/api/categoria-violencia/')
        # get data from DB
        posts = CategoriaViolencia.objects.all()
        # convert it to JSON
        serializer = CategoriaViolenciaSerializer(posts, many=True)
        # check the status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def testPut(self):
        data = {
            'id_categoria': self.cat1.id_categoria,
            'nome_categoria': 'NOME MODIFICADO',
            'ds_categoria': 'DS MODIFICADO'
        }
        endereco = '/api/categoria-violencia/' + \
            str(self.cat1.id_categoria) + '/'
        response = self.client.put(endereco, data)
        serializer = CategoriaViolenciaSerializer(data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDelete(self):
        response = self.client.delete(
            '/api/categoria-violencia/' + str(self.cat1.id_categoria) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ContatoViolenciaTestCase(APITestCase):
    def setUp(self):
        self.cont1 = ContatoViolencia.objects.create(
            nome_contato='TESTE', numero_contato='00000', ds_contato='TESTE')

    def testPost(self):
        data = {
            'nome_contato': 'NOME TESTE',
            'numero_contato': '00000',
            'ds_contato': 'DS TESTE'
        }
        response = self.client.post('/api/contato-violencia/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testGet(self):
        response = self.client.get('/api/contato-violencia/')
        posts = ContatoViolencia.objects.all()
        serializer = ContatoViolenciaSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def testPut(self):
        data = {
            'id_contato': self.cont1.id_contato,
            'nome_contato': 'NOME MODIFICADO',
            'numero_contato': '11111',
            'ds_contato': 'DS MODIFICADO'
        }
        endereco = '/api/contato-violencia/' + str(self.cont1.id_contato) + '/'
        response = self.client.put(endereco, data)
        serializer = ContatoViolenciaSerializer(data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDelete(self):
        response = self.client.delete(
            '/api/contato-violencia/' + str(self.cont1.id_contato) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class QuestionarioTestCase(APITestCase):
    def setUp(self):
        self.cat1 = CategoriaViolencia.objects.create(
            nome_categoria='TESTE', ds_categoria='TESTE')
        self.cat2 = CategoriaViolencia.objects.create(
            nome_categoria='TESTE2', ds_categoria='TESTE2')
        self.quest1 = Questionario.objects.create(
            categoria_violencia=self.cat1, arvore_decisao=json.dumps('teste'))

    def testPost(self):
        data = {
            'categoria_violencia': self.cat1.id_categoria,
            'arvore_decisao': json.dumps('teste')
        }
        response = self.client.post('/api/questionario/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testGet(self):
        response = self.client.get('/api/questionario/')
        posts = Questionario.objects.all()
        serializer = QuestionarioSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def testPut(self):
        data = {
            'id_questionario': self.quest1.id_questionario,
            'categoria_violencia': self.cat1.id_categoria,
            'arvore_decisao': json.dumps('teste2')
        }
        data_serializer = {
            'id_questionario': self.quest1.id_questionario,
            'categoria_violencia': self.cat1,
            'arvore_decisao': 'teste2'
        }
        endereco = '/api/questionario/' + \
            str(self.quest1.id_questionario) + '/'
        response = self.client.put(endereco, data)
        serializer = QuestionarioSerializer(data_serializer)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDelete(self):
        response = self.client.delete(
            '/api/questionario/' + str(self.quest1.id_questionario) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ContatoQuestionarioTestCase(APITestCase):
    def setUp(self):
        self.contv1 = ContatoViolencia.objects.create(
            nome_contato='TESTE', numero_contato='00000', ds_contato='TESTE')
        self.cat1 = CategoriaViolencia.objects.create(
            nome_categoria='TESTE', ds_categoria='TESTE')
        self.quest1 = Questionario.objects.create(
            categoria_violencia=self.cat1, arvore_decisao=json.dumps('teste'))
        self.contq1 = ContatoQuestionario.objects.create(
            contato_fk=self.contv1, questionario_fk=self.quest1)

    def testPost(self):
        data = {
            'contato_fk': self.contv1.id_contato,
            'questionario_fk': self.quest1.id_questionario
        }
        response = self.client.post('/api/contato-questionario/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testGet(self):
        response = self.client.get('/api/contato-questionario/')
        posts = ContatoQuestionario.objects.all()
        serializer = ContatoQuestionarioSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def testDelete(self):
        response = self.client.delete(
            '/api/contato-questionario/' + str(self.contq1.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testPut(self):
        data = {
            'id': self.contq1.pk,
            'contato_fk': self.contv1.id_contato,
            'questionario_fk': self.quest1.id_questionario
        }
        data_serializer = {
            'id': self.contq1.pk,
            'contato_fk': self.contv1,
            'questionario_fk': self.quest1
        }
        endereco = '/api/contato-questionario/' + str(self.contq1.pk) + '/'
        response = self.client.put(endereco, data)
        serializer = ContatoQuestionarioSerializer(data_serializer)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
