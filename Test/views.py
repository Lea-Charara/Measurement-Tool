from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test
from django.http import *
import json

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