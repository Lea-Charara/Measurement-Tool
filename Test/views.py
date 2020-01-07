from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test
from django.http import *
from django.db.models import Sum
from DatabaseTest.models import DatabaseTest
from Database.models import Database
from Type.models import Type
import json
import pyorient
import time
import psycopg2
from cassandra.cluster import Cluster

# Create your views here.
class AddTestView(APIView):

    def post(self, request):
        
            if "name" in request.data in request.data and "repetition" in request.data and "timeout" in request.data:
                if not(Test.objects.filter(name=request.data["name"]).exists()):
                    test = Test()
                    test.name = request.data["name"]
                    if("description" in request.data):
                        test.description = request.data["description"]
                    test.repetition = request.data["repetition"]
                    test.timeout = request.data["timeout"]
                    test.save()
                    return Response(status = status.HTTP_200_OK)
                return Response(status = status.HTTP_403_FORBIDDEN)
            return Response(status = status.HTTP_400_BAD_REQUEST)


class RemoveTestView(APIView):
    def delete(self, request):
            if "name" in request.data:
                if Test.objects.filter(name=request.data["name"]).exists():
                    Test.objects.filter(name=request.data["name"]).delete()
                    return Response(status = status.HTTP_200_OK)
            return Response(status = status.HTTP_400_BAD_REQUEST)

class GetAllTestsView(APIView):
    def get(self, request):
        tests = Test.objects.all().values()
        tests_list = list(tests)
        return JsonResponse(tests_list, safe=False)
        
class GetTestView(APIView):
    def post(self, request):
        if "id" in request.data:
            return JsonResponse(list(Test.objects.filter(id=request.data["id"]).values()),safe = False)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class UpdateTestView(APIView):
    def post(self,request):
        if "id" in request.data:
            test = Test.objects.filter(id=request.data["id"])
            if "name" in request.data:
                test.update(name = request.data["name"])
            if "description" in request.data:
                test.update(description = request.data["description"])
            if "repetition" in request.data:
                test.update(repetition = request.data["repetition"])
            if "timeout" in request.data:
                test.update(timeout = request.data["timeout"])
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class RemoveTestView(APIView):
    def delete(self, request):
        if "id" in request.data:
            if Test.objects.filter(pk=request.data["id"]).exists():
                Test.objects.filter(pk=request.data["id"]).delete()
                return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)



def Reset(id):
        dbtests = DatabaseTest.objects.filter(Test_id_id=id)
        for dbtest in dbtests:
            dbtest.Test_Duration = 0
            dbtest.Progress = 0
            dbtest.save()

def start(testid):
    try:
        test = Test.objects.filter(id=testid)[0]
        test.Status = 1
        test.save()
    except:
        return -2
    
    tests = DatabaseTest.objects.filter(Test_id_id=testid)
    for i in range(len(tests)):
        dbtest = tests[i]
        db = Database.objects.filter(id=dbtest.DB_id_id)[0]
        dbtype = Type.objects.filter(typename=db.dbtype).first()
        print(dbtype)
        if((str(dbtype)) == "Cassandra"):
            if(test.Status == 1):
                try:
                    cluster = Cluster([request.data["host"]],port=int(request.data["port"]))
                    session = cluster.connect()
                except:
                    return -1 
                start = time.time()
                for i in range(dbtest.Progress,test.repetition):
                    try:
                        test = Test.objects.filter(id=testid)[0]
                    except:
                        return -2
                    if(test.Status == 1):
                        timeout = int(test.timeout)*1000
                        session.execute(dbtest.query)
                        dbtest.Progress +=1
                        dbtest.save()
                    else:
                        break
                end = time.time()
                dbtest.Test_Duration += end - start
                dbtest.save()
                session.close()      
        if((str(dbtype)) == "OrientDB"):
            if(test.Status == 1):
                try:
                    client = pyorient.OrientDB(str(db.host), int(db.port)) 
                    client.db_open(str(db.name), str(db.username), str(db.password))
                except:
                    return -1
                start = time.time()
                for i in range(dbtest.Progress,test.repetition):
                    try:
                        test = Test.objects.filter(id=testid)[0]
                    except:
                        return -2
                    if(test.Status == 1):
                        timeout = int(test.timeout)*1000
                        temp = client.query(dbtest.query +" TIMEOUT "+str(timeout))
                        dbtest.Progress +=1
                        dbtest.save()
                    else :
                        break
                end = time.time()
                dbtest.Test_Duration += end - start
                dbtest.save()
                client.db_close()                       
        elif((str(dbtype)) == "Neo4j"):
            if(test.Status == 1):
                try:
                    driver = GraphDatabase.driver(uri="bolt://"+str(db.host) +":"+int(db.port), auth=(str(db.username), str(db.password)))
                except:
                    return -1
                start = time.time()
                for i in range(test.repetition):
                    try:
                        test = Test.objects.filter(id=testid)[0]
                    except:
                        return -2
                    if(test.Status == 1):
                        timeout = int(test.timeout)*1000
                        temp = driver.query(dbtest.query +" dbms.transaction.timeout= "+str(timeout))
                        dbtest.Progress +=1
                        dbtest.save()
                    else :
                        break
                end = time.time()
                dbtest.Test_Duration = end - start
                dbtest.save()
                driver.close()
        elif((str(dbtype)) == "Postgresql"):
            if(test.Status == 1):
                try:
                    connections = psycopg2.connect(database=str(db.name),user=str(db.username),password=str(db.password),host=str(db.host),port=int(db.port))
                    print("hello")
                except:
                    return -1
                start = time.time()
                for i in range(test.repetition):
                    try:
                        test = Test.objects.filter(id=testid)[0]
                    except:
                        return -2
                    if(test.Status == 1):
                        cursor = connections.cursor()
                        temp = cursor.execute(dbtest.query)
                        cursor.close()
                        dbtest.Progress +=1
                        dbtest.save()
                    else :
                        break
                end = time.time()
                dbtest.Test_Duration = end - start
                dbtest.save()
                connections.close()

class BeginTestView(APIView):
    def post(self, request):
        if "id" in request.data:
            res = start(request.data["id"])
            if(res == -1):
                return Response(status = status.HTTP_400_BAD_REQUEST)
            if (res == -2):
                return Response(status = status.HTTP_404_NOT_FOUND)
            else:
                return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)
           
    
class Restart(APIView):
    def post(self,request):
        if "id" in request.data:
            Reset(request.data["id"])
            res = start(request.data["id"])
            if(res == -1):
                return Response(status = status.HTTP_400_BAD_REQUEST)
            if (res == -2):
                return Response(status = status.HTTP_404_NOT_FOUND)
            else:
                return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)      

class StopTest(APIView):
    def post(self, request):
        if "id" in request.data:
            Reset(request.data["id"])
            test = Test.objects.filter(id=request.data["id"])[0]
            test.Progress = 0
            test.Status = 0
            test.save()
            tests = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)


class GetProgressView(APIView):
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
                return JsonResponse(round(prog),safe= False)
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class Pause(APIView):
    def post(self, request):
        if "id" in request.data:
            if Test.objects.filter(id=request.data["id"]).exists():
                temp = Test.objects.filter(id=request.data["id"])[0]
                temp.Status = 2
                temp.save()
                return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

