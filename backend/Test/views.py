from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test
from django.http import *


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
        
            if len(Test.objects.all()) > 0:
                tests = Test.objects.all().values()
                tests_list = list(tests)
                return JsonResponse(tests_list, safe=False)
            return Response(status = status.HTTP_400_BAD_REQUEST)