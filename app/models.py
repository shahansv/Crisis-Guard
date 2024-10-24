from django.db import models

# Create your models here.

class login_table(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

class camp_table(models.Model):
    campName = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    pin = models.BigIntegerField()
    email = models.CharField(max_length=200)
    contactno = models.BigIntegerField()

class camp_coordinator_table(models.Model):
    LOGIN = models.ForeignKey(login_table,on_delete=models.CASCADE)
    CAMP = models.ForeignKey(camp_table,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    dob=models.CharField(max_length=100)
    contactNo = models.BigIntegerField()
    email = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    pin = models.BigIntegerField()
    photo = models.FileField()

class Guidelines_table(models.Model):
    CAMP_COORDINATOR = models.ForeignKey(camp_coordinator_table, on_delete=models.CASCADE)
    guideline = models.FileField()
    date = models.DateField()
    time = models.TimeField()

class public_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    dob = models.DateField()
    district=models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    pin = models.BigIntegerField()
    post = models.CharField(max_length=200)
    contactNo = models.BigIntegerField()
    email = models.CharField(max_length=200)
    photo = models.FileField()

class complaint_table(models.Model):
    PUBLIC = models.ForeignKey(public_table, on_delete=models.CASCADE)
    complaint  = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    reply = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

class notification_table(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()

class emergency_team_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    department= models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    pin = models.BigIntegerField()
    ContactNo = models.BigIntegerField()
    email = models.CharField(max_length=200)

class needs_table(models.Model):
    COORDINATOR = models.ForeignKey(camp_coordinator_table, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    quantity = models.IntegerField()
    date = models.DateField()

class goods_table(models.Model):
    PUBLIC = models.ForeignKey(public_table, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    quantity = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()

class emergency_request_table(models.Model):
    EMERGENCY_TEAM = models.ForeignKey(emergency_team_table, on_delete=models.CASCADE)
    request = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()

class stock_table(models.Model):
    category =  models.CharField(max_length=200)
    product =  models.CharField(max_length=200)
    quantity =  models.IntegerField()
    date = models.DateField()

class member_table(models.Model):
    COORDINATOR=models.ForeignKey(camp_coordinator_table,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    dob = models.DateField()
    district = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    pin = models.BigIntegerField()
    contactNo = models.BigIntegerField()
    email = models.CharField(max_length=200)
    photo = models.FileField()

class volunteer_table(models.Model):
    COORDINATOR = models.ForeignKey(camp_coordinator_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    dob = models.DateField()
    district = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    pin = models.BigIntegerField()
    ContactNo = models.BigIntegerField()
    email = models.CharField(max_length=200)
    photo = models.FileField()

class asset_table(models.Model):
    MEMBER = models.ForeignKey(member_table, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    asset = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date = models.DateField()
    status = models.CharField(max_length=200)

class medical_request_table(models.Model):
    CAMP = models.ForeignKey(camp_table, on_delete=models.CASCADE)
    request = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()

class services_table(models.Model):
    VOLUNTEER = models.ForeignKey(volunteer_table, on_delete=models.CASCADE)
    services  = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()