# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Type
from django.http import JsonResponse

class GetTypeName(APIView):
    def get(self, request):
        if len(Type.objects.all()) > 0:
            typelist = list(Type.objects.all().values())
            return JsonResponse(typelist,safe = False)
        return Response(status = status.HTTP_400_BAD_REQUEST)