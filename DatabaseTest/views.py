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
    def post(self, request):
        if "testid" in request.data:
            
            average = []
            db_name = []
            test_name = ''
            test_query=[]
            TimeOfTest=[]
            Descriptions=''
            Nb_Query = []
            
            for dbtest in DatabaseTest.objects.filter(Test_id=request.data["testid"]):
                
                test = Test.objects.filter(id=request.data["testid"])[0]
                
                db_name.append(str(dbtest.DB_id))
                test_name = str(dbtest.Test_id)
                average.append(int(dbtest.Test_Duration)/int(test.repetition))
                Nb_Query.append(int(test.repetition))
                test_query.append(dbtest.query)
                TimeOfTest.append(dbtest.Test_Duration)
                Descriptions=test.description

            body = {"NB_Query":Nb_Query,"average": average, "db_name": db_name, "test_name": test_name,"test_query": test_query,"Test_Duration": TimeOfTest, "Descriptions":Descriptions}

            return Response(status=status.HTTP_202_ACCEPTED, data=body)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetProgress(APIView):
    def post(self, request):
        if "id" in request.data:
            if Test.objects.filter(id=request.data["id"]).exists():
                qrs = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
                test = Test.objects.filter(id=request.data["id"])[0]
                rep = int(test.repetition)
                qrsdone = qrs.aggregate(Sum('Progress'))
                prog = ((qrsdone['Progress__sum'])/(rep*len(qrs)))*100
                test.Progress = prog
                if(prog == 100):
                    test.Status = 0
                test.save()
                body = {"prog": round(prog)}
            return Response(status = status.HTTP_202_ACCEPTED,data=body)
        return Response(status = status.HTTP_400_BAD_REQUEST)
#GetProgress: dbtest.Progress/test.progress * 100 -> return Progress , dbtest time