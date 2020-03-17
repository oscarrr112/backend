from hashlib import new

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import *

URL = 'http://127.0.0.1:8000/media/'


# Create your views here.
@require_http_methods(["GET", "POST"])
def register(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        try:
            try:
                if User.objects.get(phonenum=json_result['PhoneNum']):
                    response['code'] = 2
                    return JsonResponse(response)
            except Exception:
                response['code'] = 0

                user = User.objects.create(
                    phonenum=json_result['PhoneNum'],
                    username=json_result['UserName'],
                    password=json_result['Password'],
                    sex=json_result['Sex'],
                    requestion=json_result['Requestion'],
                    answer=json_result['Answer'],
                    userpic=request.FILES['Avater'])

            temp = json_result['Style']
            for index in range(len(temp)):
                style = Style.objects.create(
                    phonenum=user.phonenum,
                    stylename=temp[index],
                )
        except Exception as e:
            response['code'] = 1
            print('error: ', type(e))
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
def login(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        try:
            user = User.objects.get(
                phonenum=json_result['PhoneNum'])
            if user.password == json_result['Password']:
                response['code'] = 0
            else:
                response['code'] = 2
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)


def findpassword1(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        try:
            user = User.objects.get(
                phonenum=json_result['PhoneNum'])
            response['code'] = 0
            json_data = {}
            json_data['Requestion'] = user.requestion
            response['data'] = json_data
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ' , e)
    return JsonResponse(response)


def findpassword2(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        try:
            user = User.objects.get(
                phonenum=json_result['PhoneNum'])
            if user.answer == json_result['Answer']:
                response['code'] = 0
                json_data = {}
                json_data['Password'] = user.password
                response['data'] = json_data
            else:
                response['code'] = 2
        except Exception as e:
            print(e)
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)


def getinfo(request):
    response = {}
    try:
        json_result = json.loads(request.GET.get('data'))
        try:
            print(json_result['PhoneNum'])
            user = User.objects.get(
                phonenum=json_result['PhoneNum'])
            response['code'] = 0
            json_data = {}
            json_data['UserName'] = user.username
            json_data['Avater'] = URL + str(user.userpic)
            json_data['Password'] = user.password
            json_data['Sex'] = user.sex
            json_data['Requestion'] = user.requestion
            json_data['Answer'] = user.answer
            style_search = Style.objects.filter(phonenum=user.phonenum).values('stylename')
            num = style_search.count()
            style_response = []
            for index in range(num):
                style_response.append(style_search[index]['stylename'])
            json_data['Style'] = style_response
            response['data'] = json_data
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ' , e)
    return JsonResponse(response)


def editinfo(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        try:
            user = User.objects.get(
                phonenum=json_result['PhoneNum'])
            try:
                user.phonenum = json_result['PhoneNum']
                user.username = json_result['UserName']
                user.password = json_result['Password']
                user.sex = json_result['Sex']
                user.requestion = json_result['Requestion']
                user.answer = json_result['Answer']
                user.userpic = request.FILES['Avater']
                user.save()
                Style.objects.filter(
                    phonenum=user.phonenum).delete()
                temp = json_result['Style']
                for index in range(len(temp)):
                    style = Style.objects.create(
                        phonenum=user.phonenum,
                        stylename=temp[index]
                    )
                response['code'] = 0
            except Exception as e:
                print(e)
                response['code'] = 2
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)


def addmodel(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        try:
            user = User.objects.get(
                phonenum=json_result['PhoneNum'])
            try:
                user.usermodel = json_result['Model']
                user.save()
                response['code'] = 0
            except Exception as e:
                print(e)
                response['code'] = 2
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)


def getmodel(request):
    response = {}
    try:
        json_result = json.loads(request.GET.get('data'))
        try:
            print(json_result['PhoneNum'])
            user = User.objects.get(
                phonenum=json_result['PhoneNum'])
            response['code'] = 0
            json_data = {}
            json_data['Model'] = user.usermodel
            response['data'] = json_data
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)
