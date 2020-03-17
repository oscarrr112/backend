from django.db import models


class Cloth(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)  # Field name made lowercase.
    phonenum = models.CharField(db_column='PhoneNum', max_length=150)  # Field name made lowercase.
    classifycode = models.CharField(db_column='ClassifyCode', max_length=150)  # Field name made lowercase.
    clothurl = models.ImageField(db_column='ClothUrl', upload_to='cloth/')

    class Meta:
        managed = True
        db_table = 'cloth'


class Style(models.Model):
    phonenum = models.CharField(db_column='PhoneNum', max_length=150)  # Field name made lowercase.
    stylename = models.CharField(db_column='StyleName', max_length=150)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'style'


class User(models.Model):
    phonenum = models.CharField(db_column='PhoneNum', primary_key=True, max_length=150)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=150)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=150)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=150)  # Field name made lowercase.
    requestion = models.CharField(db_column='Requestion', max_length=150)  # Field name made lowercase.
    answer = models.CharField(db_column='Answer', max_length=150)  # Field name made lowercase.
    userpic = models.ImageField(db_column='UserPic', upload_to='user/',
                                default='user/default.jpg')  # Field name made lowercase.
    usermodel = models.CharField(db_column='UserModel', max_length=150, null=True,
                                 blank=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'user'
