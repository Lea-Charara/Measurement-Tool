from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test
from django.http import *
from DatabaseTest.models import DatabaseTest
from Database.models import Database
from Type.models import Type
import json
import pyorient
import time

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




class BeginTestView(APIView):
    def post(self, request):
        
        if "id" in request.data:
            
            test = Test.objects.filter(id=request.data["id"])[0]
            test.Nb_of_done = 0
            if(not(test.AbleToRun)):
                test.AbleToRun = True
            test.save()
            tests = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
            for dbtest in tests:
                db = Database.objects.filter(id=dbtest.DB_id_id)[0]
                dbtype = Type.objects.filter(typename=db.dbtype).first()
                dbtest.Nb_of_done = 0
                if((str(dbtype)) == "Cassandra"):
                    return
                
                if((str(dbtype)) == "OrientDB"):
                    if(test.AbleToRun):
                        client = pyorient.OrientDB(str(db.host), int(db.port)) 
                        #session_id = client.connect(str(db.username), str(db.password))
                        client.db_open(str(db.name), str(db.username), str(db.password))
                        start = time.time()
                        for i in range(test.repetition):
                            test = Test.objects.filter(id=request.data["id"])[0]
                            print(test.AbleToRun)
                            if(test.AbleToRun):
                                timeout = int(test.timeout)*1000
                                temp = client.query(dbtest.query +" TIMEOUT "+str(timeout))
                                dbtest.Nb_of_done +=1
                                dbtest.save()
                            else :
                                print(test.Nb_of_done)
                                print("stop")
                                break
                        end = time.time()
                        print(end - start)
                        dbtest.Test_Duration = end - start
                        dbtest.save()
                        if(test.AbleToRun):
                            test.Nb_of_done +=1
                            test.save()
                        return Response(status = status.HTTP_200_OK)
                elif((str(dbtype)) == "Neo4j"):
                 driver = GraphDatabase.driver(uri="bolt://"+str(db.host) +":"+int(db.port), auth=(str(db.username), str(db.password))
                            start = time.time()
                             for i in range(test.repetition):
                                 test = Test.objects.filter(id=request.data["id"])[0]
                                    print(test.AbleToRun)
                                    if(test.AbleToRun):
                                        timeout = int(test.timeout)*1000
                                        temp = driver.query(dbtest.query +" dbms.transaction.timeout= "+str(timeout))
                                        dbtest.Nb_of_done +=1
                                        dbtest.save()
                                    else :
                                        print(test.Nb_of_done)
                                        print("stop")
                                        break
                                end = time.time()
                                print(end - start)
                                dbtest.Test_Duration = end - start
                                dbtest.save()
                                if(test.AbleToRun):
                                    test.Nb_of_done +=1
                                    test.save()
                return
                elif((str(dbtype)) == "Postgres"):
                    return
        return Response(status = status.HTTP_400_BAD_REQUEST)

class ContinueTestView(APIView):
    def post(self, request):
        
        if "id" in request.data:
            test = Test.objects.filter(id=request.data["id"])[0]
            test.AbleToRun = True
            test.save()
            tests = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
            for dbtest in tests:
                db = Database.objects.filter(id=dbtest.DB_id_id)[0]
                dbtype = Type.objects.filter(typename=db.dbtype).first()
                
                if((str(dbtype)) == "Cassandra"):
                    return
                
                if((str(dbtype)) == "OrientDB"):
                    if(test.AbleToRun):
                        client = pyorient.OrientDB(str(db.host), int(db.port))
                        client.db_open(str(db.name), str(db.username), str(db.password))
                        start = time.time()
                        i = db.Nb_of_done
                        for i in range(test.AbleToRun):
                            test = Test.objects.filter(id=request.data["id"])[0]
                            if(test.AbleToRun):
                                timeout = int(test.timeout)*1000
                                temp = client.query(dbtest.query)
                                dbtest.Nb_of_done +=1
                                dbtest.save()
                            else:
                                break
                        end = time.time()
                        dbtest.Test_Duration += end - start
                        dbtest.save()
                        if(test.AbleToRun):
                            test.Nb_of_done +=1
                            test.save()
                        return Response(status = status.HTTP_200_OK)
                
                elif((str(dbtype)) == "Neo4j"):
                    return
                
                elif((str(dbtype)) == "Postgres"):
                    return
        
        return Response(status = status.HTTP_400_BAD_REQUEST)


class StopTest(APIView):
    def post(self, request):
        if "id" in request.data:
            test = Test.objects.filter(id=request.data["id"])[0]
            test.Nb_of_done = 0
            test.AbleToRun = False
            test.save()
            tests = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
            for dbtest in tests:
                dbtest.Nb_of_done = 0
                dbtest.Test_Duration = 0
                dbtest.save()
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)


class GetNbOfDoneView(APIView):
    def post(self, request):
        if "id" in request.data:
            if Test.objects.filter(id=request.data["id"]).exists():
                nboftest = DatabaseTest.objects.filter(Test_id_id=request.data["id"])
                pdone = (int(Test.objects.filter(id=request.data["id"])[0].Nb_of_done)/len(nboftest))*100
                return JsonResponse(pdone,safe= False)
            return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class AbleToRun(APIView):
    def post(self, request):
        if "id" in request.data:
            if Test.objects.filter(id=request.data["id"]).exists():
                temp = Test.objects.filter(id=request.data["id"])[0]
                temp.AbleToRun = not(temp.AbleToRun)
                temp.save()
                print(temp.AbleToRun)
                return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)