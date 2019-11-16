from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Database
from Type.models import Type
from django.http import JsonResponse
from DatabaseTest.models import DatabaseTest
import pyorient


# Create your views here.
class AddDatabaseView(APIView):

    def post(self, request):
            connection = False
            if "name" in request.data and "user" in request.data and "dbtype" in request.data and "password" in request.data and "host" in request.data and "port" in request.data:
                #test connection
               if request.data["dbtype"] == "OrientDB":
                try:
                    client = pyorient.OrientDB(request.data["host"], int(request.data["port"])) 
                    session_id = client.connect(request.data["user"],request.data["password"])
                except :
                    return Response(status = status.HTTP_400_BAD_REQUEST)
                
                if (connection == True):
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
       

class UpdateDatabaseView(APIView):
    def post(self, request):
        if "id" in request.data:
            db = Database.objects.filter(id=request.data["id"])
            if "name" in request.data:
                db.update(name = request.data["name"])
            if "host" in request.data:
                db.update(host = request.data["host"])
            if "port" in request.data:
                db.update(port = request.data["port"])
            if "user" in request.data:
                db.update(username = request.data["user"])
            if "password" in request.data:
                db.update(password = request.data["password"])
            if "dbtype" in request.data:
                dtype = Type.objects.filter(typename=request.data["dbtype"]).first()
                if DatabaseTest.objects.filter(DB_id = request.data["id"]).exists():
                    DatabaseTest.objects.filter(DB_id = request.data["id"]).delete()
                db.update(dbtype = dtype)
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class GetDatabaseView(APIView):
    def post(self, request):
        if "id" in request.data:
            return JsonResponse(list(Database.objects.filter(id=request.data["id"]).values()),safe = False)
        return Response(status = status.HTTP_400_BAD_REQUEST)