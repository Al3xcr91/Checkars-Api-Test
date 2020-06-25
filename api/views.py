from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from api import serializers
from api import models
import requests
import json
from django.shortcuts import get_object_or_404
from requests.auth import HTTPBasicAuth


class ApiView(APIView):

    def put(self, request, pk):
        serializer = serializers.ApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Primera pegada al site con Get para recuperar los datos con el car_id
        # r = requests.get(f'http://localhost:8000/test/api/v1/site/{pk}/')
        r = requests.get(f'https://al3xcr91.pythonanywhere.com/test/api/v1/site/{pk}/')
        if r.status_code >= 400:
            return Response({'Error msg': 'El car_id es invalido', 'api': r.url}, status=400)
        # Se recuperan los datos
        car_data_site = r.json()
        print(f'Primera API Get car_data_site : {car_data_site}')
        mlid = car_data_site['mlid']
        _id = car_data_site['_id']
        body = {'precio': serializer.data['precio'], 'kilometros': serializer.data['kilometros']}
        #Segunda pegada al site/_id con Put y hace la actualización de precio y km en el site con el _id
        # r = requests.put(f'http://localhost:8000/test/api/v1/site-by-id/{_id}/', data=body)
        r = requests.put(f'https://al3xcr91.pythonanywhere.com/test/api/v1/site-by-id/{_id}/', data=body)
        if r.status_code >= 400:
            return Response({'Error msg': 'El _id es inválido', 'api': r.url}, status=400)
        #Primera pegada al sitio de Meli con Get para recuperar el seller_id y el status
        # r = requests.get(f'http://localhost:8000/test/api/v1/meli/{mlid}/')
        r = requests.get(f'https://al3xcr91.pythonanywhere.com/test/api/v1/meli-api/{mlid}/')
        if r.status_code >= 400:
            return Response({'Error msg': 'el mlid no existe', 'api': r.url}, status=400)
        # Se recuperan los datos
        meli_data = r.json()
        seller_id = meli_data['seller_id']
        status = meli_data['status']
        body = {'mlid': mlid, 'status': status, 'seller_id': seller_id, 'precio': serializer.data['precio'], 'kilometros': serializer.data['kilometros']}
        if status != 'active':
            return Response({'Warning': 'La publicación no está activa en Meli', 'api': r.url}, status=400)
        token = get_auth_token(seller_id)
        #Segunda pegada al sitio de Meli con Put para actualizar precio y km con el mlid
        # r = requests.put(f'http://localhost:8000/test/api/v1/meli/{mlid}/?access_token={token}', data=body)
        r = requests.put(f'https://al3xcr91.pythonanywhere.com/test/api/v1/meli/{mlid}/?access_token={token}', data=body)
        response = Response(serializer.data)
        if r.status_code >= 400:
            return Response({'Error msg': 'El seller_id es inválido', 'api': r.url}, status=400)
        return response

def get_auth_token(seller_id):
    #Esto es para pasarle un Token
    return "Placeholder"


# class CheckarsSiteViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Checkars Cars site to be viewed.
#     """
#     queryset = models.CheckarsSite.objects.all()
#     serializer_class = serializers.CheckarsSiteSerializer


# class CheckarsSiteViewSetById(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Checkars Cars site to be viewed or edited.
#     """
#     queryset = models.CheckarsSiteByID.objects.all()
#     serializer_class = serializers.CheckarsSiteSerializerById


# class MeliItemView(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Meli Item site to be viewed or edited.
#     """
#     queryset = models.MeliItem.objects.all()
#     serializer_class = serializers.MeliItemSerializer