from django.db import models
from time import time
from django.utils import timezone
import datetime

# Create your models here.
class State(models.Model):
    name_of_state=models.CharField(max_length=40)

    def __unicode__(self):
        return self.name_of_state

class City(models.Model):
    name_of_city=models.CharField(max_length=40)
    state=models.ForeignKey(State)

    def __unicode__(self):
        return self.name_of_city

class Locality(models.Model):
    name_of_locality=models.CharField(max_length=40)
    city=models.ForeignKey(City)

    def __unicode__(self):
        return self.name_of_locality

def get_image_file_name(instance,file_name):
    return "%s_%s" %(str(time()).replace(".","_"),file_name)

class ProductPrimeCategory(models.Model):
    name=models.CharField(max_length=100)
    icon_image_url=models.ImageField(upload_to=get_image_file_name)

    def __unicode__(self):
        return self.name

def get_icon_file_name(instance, file_name):
    return "product_prime_category_icons/%s_%s" %(str(time()).replace(".","_"),file_name)

class ProductSubCategory(models.Model):
    product_prime_category=models.ForeignKey(ProductPrimeCategory)
    name=models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class User(models.Model):
    name=models.CharField(max_length=100)
    corporate_email_id=models.EmailField()
    alternate_email_id=models.EmailField()
    contact_no=models.CharField(max_length=20)
    state=models.ForeignKey(State)
    city=models.ForeignKey(City)
    locality=models.ForeignKey(Locality)

    def __unicode__(self):
        return self.name+" : "+self.alternate_email_id

class UserSecurityCreds(models.Model):
    user=models.ForeignKey(User)
    salt=models.CharField(max_length=32)
    pass_hash=models.CharField(max_length=128)

class ProductAd(models.Model):
    category=models.ForeignKey(ProductPrimeCategory)
    subcategory=models.ForeignKey(ProductSubCategory)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    no_of_views=models.IntegerField()
    seller=models.ForeignKey(User)
    state=models.ForeignKey(State)
    city=models.ForeignKey(City)
    locality=models.ForeignKey(Locality)
    product_images=models.CharField(max_length=4)
    ad_post_duration=models.DateTimeField()
    posted_by=models.CharField(max_length=10)
    price=models.FloatField(null=True,blank=True)

    def __unicode__(self):
        return self.title

    def published_day_ago(self):
        if (((datetime.datetime.now()-self.ad_post_duration).seconds)/60)<=1440:
            return self

    def published_week_ago(self):
        if (((datetime.datetime.now()-self.ad_post_duration).seconds)/60)/24 <=7:
            return self

    def published_month_ago(self):
        if (((datetime.datetime.now()-self.ad_post_duration).seconds)/60)/24 <=30:
            return self


class ProductSubFilter(models.Model):
    subcategory=models.ForeignKey(ProductSubCategory)
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=40)

    def __unicode__(self):
        return self.subcategory.name+":"+self.name

class ProductPrimeFilter(models.Model):
    product_prime_category=models.ForeignKey(ProductPrimeCategory)
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=40)

    def __unicode__(self):
        return self.product_prime_category.name+":"+self.name


class ProductSubFilterData(models.Model):
    product_sub_filter=models.ForeignKey(ProductSubFilter)
    ad=models.ForeignKey(ProductAd)
    value=models.CharField(max_length=50)

    def __unicode__(self):
        return self.product_sub_filter.name+" : "+self.value+" : "

class ProductPrimeFilterData(models.Model):
    product_prime_filter=models.ForeignKey(ProductPrimeFilter)
    ad=models.ForeignKey(ProductAd)
    value=models.CharField(max_length=50)

    def __unicode__(self):
        return self.product_prime_filter.name+" : "+self.value+" : "

class ProductSubFilterMaster(models.Model):
    product_sub_filter=models.ForeignKey(ProductSubFilter)
    value=models.CharField(max_length=50)

    def __unicode__(self):
        return self.product_sub_filter.name+" : "+self.value

class ProductPrimeFilterMaster(models.Model):
    product_prime_filter=models.ForeignKey(ProductPrimeFilter)
    value=models.CharField(max_length=50)

    def __unicode__(self):
        return self.product_prime_filter.name+" : "+self.value

# class AdImages(models.Model):
#     ad=models.ForeignKey(ProductAd)
#     image_url=models.ImageField(upload_to='')


class DomainMaster(models.Model):
    corporate_name=models.CharField(max_length=200,blank=True,null=True)
    corporate_email_domain=models.CharField(max_length=300)
    corporate_website=models.URLField(null=True,blank=True)

class TempRegistrations(models.Model):
    alternate_email=models.EmailField()
    corporate_email=models.EmailField()
    temp_token=models.CharField(max_length=32)

class Article(models.Model):
    name=models.CharField(max_length=50)
    image_url=models.CharField(max_length=100)