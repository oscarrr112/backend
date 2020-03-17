from hashlib import new

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import datetime
import time

from .models import *

URL = 'http://127.0.0.1:8000/media/'


def newid():
    id = int(time.time())
    return id


@require_http_methods(["GET", "POST"])
def getcloth(request):
    response = {}
    try:
        json_result = json.loads(request.GET.get('data'))
        try:
            User.objects.get(
                phonenum=json_result['PhoneNum'])
            try:
                getlist = Cloth.objects.filter(
                    phonenum=json_result['PhoneNum'],
                    classifycode=json_result['ClassifyCode']).values('id', 'clothurl')
                if getlist.count() == 0:
                    response['code'] = 2
                else:
                    response['code'] = 0
                    json_data = {}
                    cloth = []
                    for index in range(getlist.count()):
                        tempjson = {}
                        tempjson['ClothNum'] = str(getlist[index]['id'])
                        tempjson['ClothUrl'] = URL + getlist[index]['clothurl']
                        cloth.append(tempjson)
                    json_data['ClothList'] = cloth
                    response['data'] = json_data
            except Exception as e:
                print('code:3 ', e)
                response['code'] = 3
        except Exception as e:
            print('code: 1', e)
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)


def newcloth(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        print(request.FILES['ClothPic'])
        print(json_result)
        try:
            user = User.objects.get(phonenum=json_result['PhoneNum'])
            try:
                cloth = Cloth(id=newid(), phonenum=json_result['PhoneNum'], classifycode=json_result['ClassifyCode'],
                              clothurl=request.FILES['ClothPic'])
                cloth.save()
                print(cloth.clothurl)
                response['code'] = 0
            except Exception as e:
                response['code'] = 2
                print(e)
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)


def delcloth(request):
    response = {}
    try:
        json_result = json.loads(request.POST.get('data'))
        try:
            cloth = Cloth.objects.get(
                id=json_result['ClothNum'])
            try:
                Cloth.objects.filter(
                    id=json_result['ClothNum']).delete()
                response['code'] = 0
            except Exception as e:
                response['code'] = 2
        except Exception:
            response['code'] = 1
    except Exception as e:
        print('error: ', e)
    return JsonResponse(response)
