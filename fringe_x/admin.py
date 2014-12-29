from django.contrib import admin
from fringe_x import models

# Register your models here.

class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_filter = ['product_prime_category']

class SubCategoryFilterAdmin(admin.ModelAdmin):
    list_filter = ['subcategory']

class PrimeCategoryFilterAdmin(admin.ModelAdmin):
    list_filter=['product_prime_category']

class SubCategoryFilterMasterAdmin(admin.ModelAdmin):
    list_filter = ['product_sub_filter']

class PrimeCategoryFilterMasterAdmin(admin.ModelAdmin):
    list_filter = ['product_prime_filter']

class CityFilterAdmin(admin.ModelAdmin):
    list_filter = ["state"]

class LocalityFilterAdmin(admin.ModelAdmin):
    list_filter = ["city"]

admin.site.register(models.ProductPrimeCategory)
admin.site.register(models.ProductSubCategory,ProductSubCategoryAdmin)
admin.site.register(models.ProductPrimeFilter,PrimeCategoryFilterAdmin)
admin.site.register(models.ProductSubFilter,SubCategoryFilterAdmin)
admin.site.register(models.ProductPrimeFilterData)
admin.site.register(models.ProductSubFilterData)
admin.site.register(models.ProductPrimeFilterMaster,PrimeCategoryFilterMasterAdmin)
admin.site.register(models.ProductSubFilterMaster,SubCategoryFilterMasterAdmin)
admin.site.register(models.State)
admin.site.register(models.City,CityFilterAdmin)
admin.site.register(models.Locality,LocalityFilterAdmin)
admin.site.register(models.ProductAd)
admin.site.register(models.User)
admin.site.register(models.TempRegistrations)

