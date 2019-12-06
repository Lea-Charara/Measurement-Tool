from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Test.models import Test
from Database.models import Database
from .models import DatabaseTest
from django.http import JsonResponse

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
            if "testid" in request.data and "query" in request.data:
                if DatabaseTest.objects.filter(query=request.data["query"]).exists():
                    DatabaseTest.objects.filter(name=request.data["query"]).delete()
                    return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)

class RemoveDBTestView_byTest_id(APIView):
    def delete(self, request):
            if "testid" in request.data:
                if DatabaseTest.objects.filter(Test_id=request.data["testid"]).exists():
                    DatabaseTest.objects.filter(Test_id=request.data["testid"]).delete()
                    return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)
class GetAllDBTestsView(APIView):

    def get(self, request):
        dbtst = list(DatabaseTest.objects.all().values())
        return JsonResponse(dbtst,safe = False)
            

class GetDBTestView(APIView):
    def post(self, request):
        if "testid" in request.data:
            if DatabaseTest.objects.filter(Test_id_id = request.data["testid"]).exists():
                dbtst = list(DatabaseTest.objects.filter(Test_id_id = request.data["testid"]).values())
                return JsonResponse(dbtst,safe = False)
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class GetTimes(APIView):
    def post(self,request):
        if "testid" in request.data:
            if DatabaseTest.objects.filter(Test_id_id = request.data["testid"]).exists():
                dbtst = list(DatabaseTest.objects.filter(Test_id_id = request.data["testid"]).values()) 
                Max=0
                Min=1.7976931348623157e+308
                average=0
                for i in range (len(dbtst)):
                    Values = dbtst[i].Test_Duration

                    if Values < Min and Values != 0:
                        Min = Values
                    if Values > Max and Values !=0:
                        Max = Values
                    
                    average+=Values
                average = average /len(dbtst)
                List = [Min, Max, average]
                return JsonResponse(List,safe=False)
            return Response(status = status.HTTP_400_BAD_REQUEST)

