from django.db import models

class ReferenceData(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        ('male', MALE),
        ('female', FEMALE)
    ]
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=255,choices=GENDER_CHOICES)

class SourceData(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        ('male', MALE),
        ('female', FEMALE)
    ]
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=255,choices=GENDER_CHOICES)


