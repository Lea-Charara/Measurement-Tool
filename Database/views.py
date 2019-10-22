from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Database
from Type.models import Type
from django.http import JsonResponse


# Create your views here.
class AddDatabaseView(APIView):

    def post(self, request):
        
            if "name" in request.data and "user" in request.data and "dbtype" in request.data and "password" in request.data and "host" in request.data and "port" in request.data:
                db = Database()
                db.name = request.data["name"]
                db.host = request.data["host"]
                db.port = request.data["port"]
                db.user = request.data["user"]
                db.password = request.data["password"]
                dbtype = Type.objects.filter(typename=request.data["dbtype"]).first()
                db.dbtype = dbtype
                db.save()
                return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)


class RemoveDatabaseView(APIView):
    def delete(self, request):
        if "id" in request.data:
            if Database.objects.filter(pk=request.data["id"]).exists():
                Database.objects.filter(pk=request.data["id"]).delete()
                return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class GetAllDataBasesView(APIView):

    def get(self, request):
        dbs = Database.objects.all().values()
        dbs_list = list(dbs)
        return JsonResponse(dbs_list,safe = False)
       
        