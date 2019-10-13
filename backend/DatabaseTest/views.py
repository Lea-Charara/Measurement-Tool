from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Test.models import Test
from Database.models import Database
from .models import DatabaseTest


# Create your views here.
class AddDBTestView(APIView):

    def post(self, request):
        
            if "testid" in request.data and "dbid" in request.data and "query" in request.data :
                test = DatabaseTest()
                test.Test_id = Test.objects.filter(name=request.data["testid"]).first()
                test.DB_id = Database.objects.filter(name=request.data["dbid"]).first()
                test.query = request.data["query"]
                test.save()
                return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)


class RemoveDBTestView(APIView):
    def delete(self, request):
       
            if "query" in request.data:
                if DatabaseTest.objects.filter(query=request.data["query"]).exists():
                    DatabaseTest.objects.filter(name=request.data["query"]).delete()
                    return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)

class GetAllDBTestsView(APIView):

    def get(self, request):
       
            if len(DatabaseTest.objects.all()) > 0:
                DatabaseTest.objects.all()
                return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)