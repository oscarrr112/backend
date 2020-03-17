from django.test import TestCase

from myapp import models

import json


class RegisterTest(TestCase):

    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥'
        )
        self.url = '/user/register'

    def test_base_register(self):
        data = {
            'PhoneNum': '13907486770',
            'Password': '011016',
            'UserName': 'oscar',
            'Sex': '0',
            'Style': '["休闲"]',
            'Requestion': '叫啥',
            'Answer': '彭奥'
        }
        with open('media/user/default.jpg', 'rb') as pic:
            data = {
                'data': json.dumps(data),
                'Avater': pic
            }
            response = self.client.post(self.url, data=data)
            response = response.json()
            self.assertEqual(response['code'], 0, '用户注册失败')

    def test_duplicate_register(self):
        data = {
            'PhoneNum': '17763638641',
            'Password': '011016',
            'UserName': 'oscar',
            'Sex': '0',
            'Style': '["休闲"]',
            'Requestion': '叫啥',
            'Answer': '彭奥'
        }

        with open('media/user/default.jpg', 'rb') as pic:
            data = {
                'data': json.dumps(data),
                'Avater': pic
            }
            response = self.client.post(self.url, data=data)
            response = response.json()
            self.assertEqual(response['code'], 2, '用户名查重失败')


class LoginTest(TestCase):

    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥'
        )
        self.url = '/user/login'

    def test_base_login(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '17763638641',
                'Password': '011016'
            })
        }
        response = self.client.post(self.url, data=data).json()
        self.assertEqual(response['code'], 0, '登录失败')

    def test_empty_login(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '1',
                'Password': '011016'
            })
        }
        response = self.client.post(self.url, data=data).json()
        self.assertEqual(response['code'], 1, '空用户登录失败')

    def test_wrong_login(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '17763638641',
                'Password': '01101'
            })
        }
        response = self.client.post(self.url, data=data).json()
        self.assertEqual(response['code'], 2, '密码错误登陆失败')


class FindPassword1Test(TestCase):

    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥'
        )
        self.url = '/user/findpassword1'

    def test_base_findpassword1(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '17763638641'
            })
        }
        response = self.client.post(self.url, data=data).json()
        data = response['data']
        self.assertEqual(response['code'], 0, '找回密码1返回码')
        self.assertEqual(data['Requestion'], '叫啥', '找回密码1找回问题')

    def test_empty_findpassword1(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '1'
            })
        }
        response = self.client.post(self.url, data=data).json()
        self.assertEqual(response['code'], 1, '空用户找回密码1返回码')


class FindPassword2Test(TestCase):
    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥'
        )
        self.url = '/user/findpassword2'

    def test_base_findpassword2(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '17763638641',
                'Answer': '彭奥'
            })
        }

        response = self.client.post(self.url, data=data).json()
        data = response['data']
        self.assertEqual(response['code'], 0, '查询密码状态码错误')
        self.assertEqual(data['Password'], '011016', '查询密码返回密码错误')

    def test_empty_findpassword2(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '1',
                'Answer': '彭奥'
            })
        }

        response = self.client.post(self.url, data=data).json()
        self.assertEqual(response['code'], 1, '用户不存在 —— 查询密码状态码错误')

        def test_base_findpassword2(self):
            data = {
                'data': json.dumps({
                    'PhoneNum': '17763638641',
                    'Answer': ''
                })
            }

            response = self.client.post(self.url, data=data).json()
            self.assertEqual(response['code'], 2, '答案错误 —— 查询密码状态码错误')


class GetinfoTest(TestCase):
    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥'
        )
        models.Style.objects.create(phonenum='17763638641', stylename='休闲')
        self.url = '/user/getinfo'

    def test_base_getinfo(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '17763638641'
            })
        }
        response = self.client.get(self.url, data=data).json()
        data = response.get('data')
        data_correct = {
            'UserName': 'oscar',
            'Password': '011016',
            'Sex': '0',
            'Style': ["休闲"],
            'Requestion': '叫啥',
            'Answer': '彭奥',
            'Avater': 'http://127.0.0.1:8000/media/user/default.jpg'
        }
        self.assertEqual(response.get('code'), 0, '获取用户信息返回码错误')
        for key in data.keys():
            self.assertEqual(data[key], data_correct[key], '获取用户信息返回信息错误')

    def test_empty_getinfo(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '1'
            })
        }
        response = self.client.get(self.url, data=data).json()
        self.assertEqual(response.get('code'), 1, '用户不存在 —— 获取用户信息返回码错误')


class EditinfoTest(TestCase):
    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥'
        )
        models.Style.objects.create(phonenum='17763638641', stylename='休闲')
        self.url = '/user/editinfo'

    def test_base_editinfo(self):
        data = {
            'PhoneNum': '17763638641',
            'Password': '011016',
            'UserName': 'oscar',
            'Sex': '0',
            'Style': '["休闲"]',
            'Requestion': '叫啥',
            'Answer': '彭奥'
        }
        with open('media/user/default.jpg', 'rb') as pic:
            data = {
                'data': json.dumps(data),
                'Avater': pic
            }
            response = self.client.post(self.url, data=data)
            response = response.json()
            self.assertEqual(response['code'], 0, '修改用户信息返回码错误')

    def test_empty_editinfo(self):
        data = {
            'PhoneNum': '1',
            'Password': '011016',
            'UserName': 'oscar',
            'Sex': '0',
            'Style': '["休闲"]',
            'Requestion': '叫啥',
            'Answer': '彭奥'
        }
        with open('media/user/default.jpg', 'rb') as pic:
            data = {
                'data': json.dumps(data),
                'Avater': pic
            }
            response = self.client.post(self.url, data=data)
            response = response.json()
            self.assertEqual(response['code'], 1, '用户名不存在 —— 修改用户信息返回码错误')


class AddmodelTest(TestCase):
    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥'
        )
        models.Style.objects.create(phonenum='17763638641', stylename='休闲')
        self.url = '/user/addmodel'

    def test_base_addmodel(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '17763638641',
                'Model': 'http://1'
            })
        }
        response = self.client.post(self.url, data=data).json()
        self.assertEqual(response['code'], 0, '添加模型返回码错误')

    def test_empty_addmodel(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '1',
                'Model': 'http://1'
            })
        }
        response = self.client.post(self.url, data=data).json()
        self.assertEqual(response['code'], 1, '用户不存在 —— 添加模型返回码错误')


class GetmodelTest(TestCase):
    def setUp(self) -> None:
        models.User.objects.create(
            phonenum='17763638641',
            username='oscar',
            password='011016',
            sex='0',
            requestion='叫啥',
            answer='彭奥',
            usermodel='http://1'
        )
        models.Style.objects.create(phonenum='17763638641', stylename='休闲')
        self.url = '/user/getmodel'

    def test_base_getmodel(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '17763638641',
            })
        }

        response = self.client.get(self.url, data=data).json()
        data = response.get('data')
        self.assertEqual(response['code'], 0, '模型获取返回码错误')
        self.assertEqual(data['Model'], 'http://1', '模型获取返回URL错误')

    def test_empty_getmodel(self):
        data = {
            'data': json.dumps({
                'PhoneNum': '1',
            })
        }

        response = self.client.get(self.url, data=data).json()
        self.assertEqual(response['code'], 1, '模型获取返回码错误')

