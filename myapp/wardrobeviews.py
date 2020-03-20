from hashlib import new

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import datetime
import time

from .models import *

URL = 'http://47.101.147.32:8080/media/'


def newid():
    id = int(time.time())
    return id


def getcloth(request):
    response = {}
    try:
        json_result = json.loads(request.GET.get('data'))['data']
        try:
            User.objects.get(
                phonenum=json_result['PhoneNum'])
            try:
                clothes = Cloth.objects.filter(
                    phonenum=json_result['PhoneNum'],
                    classifycode=json_result['ClassifyCode']).values('id', 'clothurl')
                if clothes.count() == 0:
                    response['code'] = 2
                else:
                    response['code'] = 0
                    json_data = {'ClothList': list()}
                    print(clothes)
                    for cloth in clothes:
                        tempjson = {}
                        tempjson['ClothNum'] = str(cloth['id'])
                        tempjson['ClothUrl'] = URL + cloth['clothurl']
                        json_data['ClothList'].append(tempjson)
                    response['data'] = json_data
                    print(response['data'])
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
        json_result = json.loads(request.POST.get('data'))['data']
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
        json_result = json.loads(request.body.decode())['data']
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
