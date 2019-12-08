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

# Create your views here.
class AddTestView(APIView):

    def post(self, request):
        
            if "name" in request.data and "description" in request.data and "repetition" in request.data and "timeout" in request.data:
                if not(Test.objects.filter(name=request.data["name"]).exists()):
                    test = Test()
                    test.name = request.data["name"]
                    test.description = request.data["description"]
                    test.repetition = request.data["repetition"]
                    test.timeout = request.data["timeout"]
                    test.save()
                    return Response(status = status.HTTP_200_OK)
                return HttpResponseForbidden()
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
        return Response(status = status.HTTP_400_BAD_REQUEST)



def Reset(id):
        dbtests = DatabaseTest.objects.filter(Test_id_id=id)
        for dbtest in dbtests:
            dbtest.Test_Duration = 0
            dbtest.Progress = 0
            dbtest.save()
class BeginTestView(APIView):
    

    def post(self, request):
        if "id" in request.data:
            test = Test.objects.filter(id=request.data["id"])[0]
            if(test.Progress == 100):
                Reset(id = request.data["id"])
                test.Progress = 0
                
            test.Status = 1
            test.save()
            tests = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
            for i in range(len(tests)):
                dbtest = tests[i]
                db = Database.objects.filter(id=dbtest.DB_id_id)[0]
                dbtype = Type.objects.filter(typename=db.dbtype).first()
              
                if((str(dbtype)) == "Cassandra"):
                    return
                
                if((str(dbtype)) == "OrientDB"):
                    if(test.Status == 1):
                        client = pyorient.OrientDB(str(db.host), int(db.port)) 
                        client.db_open(str(db.name), str(db.username), str(db.password))
                        start = time.time()
                        for i in range(dbtest.Progress,test.repetition):
                            test = Test.objects.filter(id=request.data["id"])[0]
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
                        if(test.Progress == 100):
                            test.Status = 0
                            test.save()
                            return Response(status = status.HTTP_200_OK)                       
                elif((str(dbtype)) == "Neo4j"):
                    if(test.Status == 1):
                        driver = GraphDatabase.driver(uri="bolt://"+str(db.host) +":"+int(db.port), auth=(str(db.username), str(db.password)))
                        start = time.time()
                        for i in range(test.repetition):
                            test = Test.objects.filter(id=request.data["id"])[0]
                            print(test.Status)
                            if(test.Status == 1):
                                timeout = int(test.timeout)*1000
                                temp = driver.query(dbtest.query +" dbms.transaction.timeout= "+str(timeout))
                                dbtest.Progress +=1
                                dbtest.save()
                            else :
                                print("stop")
                                break
                        end = time.time()
                        print(end - start)
                        dbtest.Test_Duration = end - start
                        dbtest.save()
                        driver.close()
                elif((str(dbtype)) == "Postgres"):
                    if(test.Status == 1):
                        connections = psycopg2.connect(database=str(db.name),user=str(db.username),password=str(db.password),host=str(db.host),port=int(db.port))
                        start = time.time()
                        for i in range(test.repetition):
                            test = Test.objects.filter(id=request.data["id"])[0]
                            print(test.Status)
                            if(test.Status == 1):
                                cursor = connections.cursor()
                                temp = cursor.execute(dbtest.query)
                                cursor.close()
                                dbtest.Progress +=1
                                dbtest.save()
                            else :
                                print("stop")
                                break
                        end = time.time()
                        print(end - start)
                        dbtest.Test_Duration = end - start
                        dbtest.save()
                        connections.close()
                return Response(status = status.HTTP_200_OK)
            
        return Response(status = status.HTTP_400_BAD_REQUEST)
    




class StopTest(APIView):
    def post(self, request):
        if "id" in request.data:
            test = Test.objects.filter(id=request.data["id"])[0]
            test.Progress = 0
            test.Status = 0
            test.save()
            tests = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
            for dbtest in tests:
                dbtest.Progress = 0
                dbtest.Test_Duration = 0
                dbtest.save()
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)


class GetProgressView(APIView):
    def post(self, request):
        if "id" in request.data:
            if Test.objects.filter(id=request.data["id"]).exists():
                qrs = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
                test = Test.objects.filter(id=request.data["id"])[0]
                rep = int(test.repetition)
                qrsdone = qrs.annotate(done=Sum('Progress'))[0].done
                prog = ((qrsdone)/(rep*len(qrs)))*100
                test.Progress = prog
                test.save()
                #pdone = (int(test.Progress)/(rep*len(qrs)))*100
                return JsonResponse(round(prog),safe= False)
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class Status(APIView):
    def post(self, request):
        if "id" in request.data:
            if Test.objects.filter(id=request.data["id"]).exists():
                temp = Test.objects.filter(id=request.data["id"])[0]
                temp.Status = 2
                temp.save()
                return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

# class DbInUse(APIView):
#     def post(self,request):
#         if "id" in request.data:
#             if Database.objects.filter(id=request.data["id"]).exists():
#                 dbtests = list(DatabaseTest.objects.filter(db_id=request.data["id"]).values())
#                 for dbtest in dbtests:
#                     test = Test.objects.filter(id=request.data["id"])[0]
#                     if(test.Status == 1):
#                         return True
#                 return False

class RestartTestView(APIView):
    def post(self, request):
        if "id" in request.data:
            print("yes")
            start = BeginTestView()
            start.post(request)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)