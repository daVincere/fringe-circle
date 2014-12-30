import os
import hashlib
import uuid
import smtplib
from smtplib import SMTPException
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext, loader, Template
from fringe_x import models
from fringe_x import forms
import json
from datetime import datetime
from django.utils import timezone
from fringe_circle import settings

# Create your views here.
def fringecircle_index(request):
    context_dict={}
    if(user_signed_in(request)):
        current_user=models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    template_obj=loader.get_template("fringe_x/fringe_circle_index.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))


def fringex_index(request):
    context_dict={}
    # #select location logic starts here
    # if request.method=="POST":
    #     if 'change_state' in request.POST:
    #         del request.session['name_of_state_session']
    #
    #         if 'name_of_city_session' in request.session:
    #             del request.session['name_of_city_session']
    #
    #     if 'change_city' in request.POST:
    #
    #         if 'name_of_city_session' in request.session:
    #             del request.session['name_of_city_session']
    #
    #     if 'name_of_state_select' in request.POST:
    #         request.session["name_of_state_session"]=request.POST["name_of_state_select"]
    #
    #     if 'name_of_cities_select' in request.POST:
    #         request.session["name_of_city_session"]=request.POST["name_of_cities_select"]
    #
    # if 'name_of_state_session' in request.session:
    #     context_dict['name_of_state_context']=request.session["name_of_state_session"]
    #     stateobj=models.State.objects.get(name_of_state=request.session['name_of_state_session'])
    #
    #     if 'name_of_city_session' in request.session:
    #         context_dict["name_of_city_context"]=request.session["name_of_city_session"]
    #     else:
    #         context_dict['list_of_cities_context']=models.City.objects.filter(state=stateobj)
    #
    # else:
    #     context_dict['list_of_states_context']=models.State.objects.all()
    if(user_signed_in(request)):
        current_user=models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    else:
        return HttpResponseRedirect("/fringe_circle/login/")

    if 'state_session' in request.session and 'city_session' in request.session:
        if request.session['state_session'] and request.session['city_session']:
            context_dict['location_state_context']=request.session['state_session']
            context_dict['location_city_context']=request.session['city_session']
            context_dict['all_states_context']=models.State.objects.all()
    #select location logic ends here

    context_dict['product_prime_category_context']=models.ProductPrimeCategory.objects.all()
    context_dict['product_subcategory_context']=models.ProductSubCategory.objects.all()
    subcat_dict={}
    # for prime_cat in models.ProductPrimeCategory.objects.all():
    #     counter=0
    #     temp=[]
    #     for subcat in models.ProductSubCategory.objects.all():
    #         if subcat.product_prime_category == prime_cat:
    #             temp.append(subcat.name)
    #             counter+=1
    #         if counter ==4:
    #             subcat_dict[prime_cat]=temp
    #             break

    for prime_cat in models.ProductPrimeCategory.objects.all():
        subcats=models.ProductSubCategory.objects.filter(product_prime_category=prime_cat)
        temp=[]
        if len(subcats) <=4:
            for subcat in subcats:
                temp.append(subcat.name)
        else:
            for i in range(4):
                temp.append(subcats[i].name)
        subcat_dict[prime_cat]=temp


    context_dict['subcat_dict']=subcat_dict

    template_obj=loader.get_template("fringe_x/index.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))


#view to handle the data entry and file upload
def all_articles(request,subcategory=None):
    context_dict={}
    articles=models.Article.objects.all()
    context_dict['articles_context']=articles
    context_dict['subcat_context']=subcategory
    if subcategory is not None:
        subcat_object=models.ProductSubCategory.objects.get(name=subcategory)
        context_dict['filters_context']=models.ProductSubFilter.objects.filter(subcategory=subcat_object)
    template_obj=loader.get_template("fringe_x/all_articles.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))

def product_list(request,subcategory_name=None):
    context_dict={}
    if(user_signed_in(request)):
        current_user=models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    else:
        return HttpResponseRedirect("/fringe_circle/login/")

    ads_list=[]
    if 'state_session' in request.session and 'city_session' in request.session:
        if request.session['state_session'] and request.session['city_session']:
            context_dict['location_state_context']=request.session['state_session']
            context_dict['location_city_context']=request.session['city_session']
            state_obj=models.State.objects.get(name_of_state=request.session['state_session'])
            city_obj=models.City.objects.get(state=state_obj, name_of_city=request.session['city_session'])
            context_dict['all_localities_context']=models.Locality.objects.filter(city=city_obj)

    if subcategory_name is not None:
        subcategory_masters_dict={}
        prime_category_masters_dict={}
        context_dict['subcategory_name_context']=subcategory_name
        subcategory_obj=models.ProductSubCategory.objects.get(name=subcategory_name)
        context_dict['subcategories_list_context']=models.ProductSubCategory.objects.filter(product_prime_category=subcategory_obj.product_prime_category)
        context_dict['subcategory_obj_context']=subcategory_obj
        # context_dict['subcategory_ads_context']=models.ProductAd.objects.filter(subcategory=subcategory_obj)

        context_dict['subcategory_filters_context']=models.ProductSubFilter.objects.filter(subcategory=subcategory_obj)
        context_dict['prime_category_filters_context']=models.ProductPrimeFilter.objects.filter(product_prime_category=subcategory_obj.product_prime_category)
        for product_sub_filter_loop in models.ProductSubFilter.objects.filter(subcategory=subcategory_obj):
            subcategory_masters_dict[product_sub_filter_loop]=models.ProductSubFilterMaster.objects.filter(product_sub_filter=product_sub_filter_loop)

        for product_prime_filter_loop in models.ProductPrimeFilter.objects.filter(product_prime_category=subcategory_obj.product_prime_category):
            prime_category_masters_dict[product_prime_filter_loop]=models.ProductPrimeFilterMaster.objects.filter(product_prime_filter=product_prime_filter_loop)

        context_dict['subcategory_masters_dict_context']=subcategory_masters_dict
        context_dict['prime_category_masters_dict_context']=prime_category_masters_dict

    if request.method == 'POST':
        for subfilter in context_dict['subcategory_filters_context']:
            for filter_value in request.POST.getlist(subfilter.name):
                filter_datas=models.ProductSubFilterData.objects.filter(value=filter_value.strip)
                for data in filter_datas:
                    if data.ad not in ads_list:
                        ads_list.append(data.ad)

    context_dict['ads_list']=ads_list

    context_dict['subcategory_ads_context']=models.ProductAd.objects.filter(subcategory=subcategory_obj)

    template_obj=loader.get_template("fringe_x/product_list.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))

def product_grid(request,subcategory_name=None):
    context_dict={}
    if(user_signed_in(request)):
        current_user=models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    else:
        return HttpResponseRedirect("/fringe_circle/login/")
    ads_list=[]
    if 'state_session' in request.session and 'city_session' in request.session:
        if request.session['state_session'] and request.session['city_session']:
            context_dict['location_state_context']=request.session['state_session']
            context_dict['location_city_context']=request.session['city_session']
            state_obj=models.State.objects.get(name_of_state=request.session['state_session'])
            city_obj=models.City.objects.get(state=state_obj, name_of_city=request.session['city_session'])
            context_dict['all_localities_context']=models.Locality.objects.filter(city=city_obj)

    if subcategory_name is not None:
        subcategory_masters_dict={}
        prime_category_masters_dict={}
        context_dict['subcategory_name_context']=subcategory_name
        subcategory_obj=models.ProductSubCategory.objects.get(name=subcategory_name)
        context_dict['subcategories_list_context']=models.ProductSubCategory.objects.filter(product_prime_category=subcategory_obj.product_prime_category)
        context_dict['subcategory_obj_context']=subcategory_obj
        # context_dict['subcategory_ads_context']=models.ProductAd.objects.filter(subcategory=subcategory_obj)

        context_dict['subcategory_filters_context']=models.ProductSubFilter.objects.filter(subcategory=subcategory_obj)
        context_dict['prime_category_filters_context']=models.ProductPrimeFilter.objects.filter(product_prime_category=subcategory_obj.product_prime_category)
        for product_sub_filter_loop in models.ProductSubFilter.objects.filter(subcategory=subcategory_obj):
            subcategory_masters_dict[product_sub_filter_loop]=models.ProductSubFilterMaster.objects.filter(product_sub_filter=product_sub_filter_loop)

        for product_prime_filter_loop in models.ProductPrimeFilter.objects.filter(product_prime_category=subcategory_obj.product_prime_category):
            prime_category_masters_dict[product_prime_filter_loop]=models.ProductPrimeFilterMaster.objects.filter(product_prime_filter=product_prime_filter_loop)

        context_dict['subcategory_masters_dict_context']=subcategory_masters_dict
        context_dict['prime_category_masters_dict_context']=prime_category_masters_dict

    if request.method == 'POST':
        for subfilter in context_dict['subcategory_filters_context']:
            for filter_value in request.POST.getlist(subfilter.name):
                filter_datas=models.ProductSubFilterData.objects.filter(value=filter_value.strip)
                for data in filter_datas:
                    if data.ad not in ads_list:
                        ads_list.append(data.ad)

    context_dict['ads_list']=ads_list

    context_dict['subcategory_ads_context']=models.ProductAd.objects.filter(subcategory=subcategory_obj)


    template_obj=loader.get_template("fringe_x/product_grid.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))

def post_ad(request,subcategory_name=None):
    context_dict={}
    if(user_signed_in(request)):
        current_user=models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    else:
        return HttpResponseRedirect("/fringe_circle/login/")

    if 'state_session' in request.session and 'city_session' in request.session:
        if request.session['state_session'] and request.session['city_session']:
            context_dict['location_state_context']=request.session['state_session']
            context_dict['location_city_context']=request.session['city_session']

    context_dict['product_prime_category_context']=models.ProductPrimeCategory.objects.all()
    context_dict['product_subcategory_context']=models.ProductSubCategory.objects.all()

    if request.method =="POST":
        subcat_obj=subcat_obj=models.ProductSubCategory.objects.get(name=request.session['subcat_name'])
        ad_object=models.ProductAd()
        ad_object.title=request.POST['title_ad']
        ad_object.description=request.POST['description_ad']
        ad_object.subcategory=subcat_obj
        ad_object.category=subcat_obj.product_prime_category
        ad_object.state=models.State.objects.get(name_of_state=request.POST['state_select'])
        ad_object.city=models.City.objects.get(name_of_city=request.POST['city_select'])
        ad_object.locality=models.Locality.objects.get(name_of_locality=request.POST['locality_select'])
        ad_object.posted_by='Individual'
        ad_object.product_images='no'
        ad_object.price=request.POST['price']
        ad_object.seller=models.User.objects.all()[0]
        datetime_current=timezone.localtime(timezone.now())
        ad_object.ad_post_duration=datetime_current
        ad_object.save()
        context_dict['ad_object_context']=models.ProductAd.objects.get(ad_post_duration=datetime_current)
        for subfilter1 in models.ProductSubFilter.objects.filter(subcategory=models.ProductSubCategory.objects.get(name=request.session['subcat_name'])):
            if request.POST[subfilter1.name]:
                sub_filter_data_obj=models.ProductSubFilterData()
                sub_filter_data_obj.ad=models.ProductAd.objects.get(ad_post_duration=datetime_current)
                sub_filter_data_obj.product_sub_filter=subfilter1
                sub_filter_data_obj.value=request.POST[subfilter1.name]
                sub_filter_data_obj.save()

        search_subcat=models.ProductSubCategory.objects.get(name=request.session['subcat_name'])
        context_dict['abr']=search_subcat.product_prime_category.name
        for primefilter1 in models.ProductPrimeFilter.objects.filter(product_prime_category=search_subcat.product_prime_category):
            if request.POST[primefilter1.name]:
                prime_filter_data_obj=models.ProductPrimeFilterData()
                prime_filter_data_obj.ad=models.ProductAd.objects.get(ad_post_duration=datetime_current)
                prime_filter_data_obj.product_prime_filter=primefilter1
                prime_filter_data_obj.value=request.POST[primefilter1.name]
                prime_filter_data_obj.save()

        return HttpResponseRedirect("/fringe_circle/product_list/"+ad_object.subcategory.name)


    if subcategory_name is not None:
        request.session['subcat_name']=subcategory_name
        subcategory_masters_dict={}
        prime_category_masters_dict={}
        context_dict['subcategory_name_context']=subcategory_name
        subcategory_obj=models.ProductSubCategory.objects.get(name=subcategory_name)
        context_dict['current_subcategory_obj_context']=subcategory_obj
        context_dict['subcategory_filters_context']=models.ProductSubFilter.objects.filter(subcategory=subcategory_obj)
        context_dict['prime_category_filters_context']=models.ProductPrimeFilter.objects.filter(product_prime_category=subcategory_obj.product_prime_category)
        for product_sub_filter_loop in models.ProductSubFilter.objects.filter(subcategory=subcategory_obj):
            subcategory_masters_dict[product_sub_filter_loop]=models.ProductSubFilterMaster.objects.filter(product_sub_filter=product_sub_filter_loop)

        for product_prime_filter_loop in models.ProductPrimeFilter.objects.filter(product_prime_category=subcategory_obj.product_prime_category):
            prime_category_masters_dict[product_prime_filter_loop]=models.ProductPrimeFilterMaster.objects.filter(product_prime_filter=product_prime_filter_loop)

        context_dict['subcategory_masters_dict_context']=subcategory_masters_dict
        context_dict['prime_category_masters_dict_context']=prime_category_masters_dict
    context_dict['states_context']=models.State.objects.all()

    template_obj=loader.get_template("fringe_x/post-ads.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))


def individual_ad(request,ad_id=None):
    context_dict={}
    if(user_signed_in(request)):
        current_user=models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    else:
        return HttpResponseRedirect("/fringe_circle/login/")

    if 'state_session' in request.session and 'city_session' in request.session:
        if request.session['state_session'] and request.session['city_session']:
            context_dict['location_state_context']=request.session['state_session']
            context_dict['location_city_context']=request.session['city_session']

    if ad_id is not None:
        product_ad_obj=models.ProductAd.objects.get(id=ad_id)
        context_dict['product_ad_obj_context']=product_ad_obj
        context_dict['subfilter_data_context']=models.ProductSubFilterData.objects.filter(ad=ad_id)
        context_dict['primefilter_data_context']=models.ProductPrimeFilterData.objects.filter(ad=ad_id)
    template_obj=loader.get_template("fringe_x/individual_product_page.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))


#view for ajax request of city and their locality fetching
def fetch_locality(request, city_name=None):
    locality_names=[]
    json_encoder_obj=json.JSONEncoder()
    if city_name is not None:
        city_obj=models.City.objects.get(name_of_city=city_name)
        for locality in models.Locality.objects.filter(city=city_obj):
            locality_names.append(locality.name_of_locality)

    return HttpResponse(json_encoder_obj.encode(locality_names))


#view for ajax request to fetch list of all states
def fetch_all_states(request):
    state_names=[]
    json_encoder_obj=json.JSONEncoder()
    states=models.State.objects.all()
    for state in states:
        state_names.append(state.name_of_state)
    return HttpResponse(json_encoder_obj.encode(state_names))

#view for ajax request of state and their city fetching
def fetch_city(request,state_name=None):
    city_names=[]
    json_encoder_obj=json.JSONEncoder()
    if state_name is not None:
        state_obj=models.State.objects.get(name_of_state=state_name)
        for city in models.City.objects.filter(state=state_obj):
            city_names.append(city.name_of_city)

    return HttpResponse(json_encoder_obj.encode(city_names))


#view for ajax request to fetch the subcategory names
def fetch_subcategory_names(request,prime_cat_name=None):
    subcat_names=[]
    json_encoder_obj=json.JSONEncoder()
    if prime_cat_name is not None:
        prime_cat_obj=models.ProductPrimeCategory.objects.get(name=prime_cat_name)
        for subcat in models.ProductSubCategory.objects.filter(product_prime_category=prime_cat_obj):
            subcat_names.append(subcat.name)

    return HttpResponse(json_encoder_obj.encode(subcat_names))

#view for returning prime category filters through ajax query

def fetch_prime_filters(request,prime_cat_name=None):
    if prime_cat_name is not None:
        json_encoder_obj=json.JSONEncoder()
        prime_filters_name_list=[]
        primecat_obj=models.ProductPrimeCategory.objects.get(name=prime_cat_name)
        for prime_filter in models.ProductPrimeFilter.objects.filter(product_prime_category=primecat_obj):
            prime_filters_name_list.append(prime_filter.name)

    return HttpResponse(json_encoder_obj.encode(prime_filters_name_list))

#view for returning sub category filters through ajax query

def fetch_sub_filters(request,sub_cat_name=None):
    if sub_cat_name is not None:
        json_encoder_obj=json.JSONEncoder()
        sub_filters_name_list=[]
        subcat_obj=models.ProductSubCategory.objects.get(name=sub_cat_name)
        for sub_filter in models.ProductSubFilter.objects.filter(subcategory=subcat_obj):
            sub_filters_name_list.append(sub_filter.name)

    return HttpResponse(json_encoder_obj.encode(sub_filters_name_list))

#view for returning prime category filter masters through ajax query

def fetch_prime_filter_masters(request,prime_filter_name=None):
    if prime_filter_name is not None:
        json_encoder_obj=json.JSONEncoder()
        prime_filter_name_list=prime_filter_name.split('_')
        if len(prime_filter_name_list) is 2:
            primecat_obj=models.ProductPrimeCategory.objects.get(name=prime_filter_name_list[0])
            prime_filter=models.ProductPrimeFilter.objects.get(product_prime_category=primecat_obj,name=prime_filter_name_list[1])
        prime_filter_master_list=[]
        for prime_filter_master in models.ProductPrimeFilterMaster.objects.filter(product_prime_filter=prime_filter):
            prime_filter_master_list.append(prime_filter_master.value)
    return HttpResponse(json_encoder_obj.encode(prime_filter_master_list))


#view for returning sub category filter masters
def fetch_sub_filter_masters(request,sub_filter_name=None):
    if sub_filter_name is not None:
        json_encoder_obj=json.JSONEncoder()
        sub_filter_name_list=sub_filter_name.split('_')
        if len(sub_filter_name_list) is 2:
            sub_filter_master_list=[]
            subcat_obj=models.ProductSubCategory.objects.get(name=sub_filter_name_list[0])
            sub_filter=models.ProductSubFilter.objects.get(subcategory=subcat_obj,name=sub_filter_name_list[1])
            for sub_filter_master in models.ProductSubFilterMaster.objects.filter(product_sub_filter=sub_filter):
                sub_filter_master_list.append(sub_filter_master.value)

    return HttpResponse(json_encoder_obj.encode(sub_filter_master_list))

def fetch_first_sub_filter_masters(request,subcategory_name=None):
    sub_filter_master_list=[]
    if subcategory_name is not None:
        json_encoder_obj=json.JSONEncoder()
        subfilter_obj=models.ProductSubFilter.objects.filter(subcategory=models.ProductSubCategory.objects.get(name=subcategory_name))[0]
        masters=models.ProductSubFilterMaster.objects.filter(product_sub_filter=subfilter_obj)
        for sub_filter_master in masters:
            sub_filter_master_list.append(sub_filter_master.value)

    return HttpResponse(json_encoder_obj.encode(sub_filter_master_list))


#view for location selection
def location_selection(request,location_param=None):
    context_dict={}
    if location_param is not None:
        state_city=location_param.split("_")
        if len(state_city) is 2:
            state_obj=models.State.objects.get(name_of_state=state_city[0])
            city_obj=models.City.objects.get(name_of_city=state_city[1])
            request.session['state_session']=state_obj.name_of_state
            request.session['city_session']=city_obj.name_of_city

            HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



#view for returning ads based on filter

def get_filter_ads(request, ad_parameters=None):
    json_decoder_obj=json.JSONDecoder()
    json_encoder_obj=json.JSONEncoder()
    if request.method=='POST':
        if ad_parameters is not None:
            price_ascending=False
            price_descending=False

            ad_parameters_list=ad_parameters.split('_')
            subcat_name=ad_parameters_list[0]

            #retrieved the subcategory from the url argument
            subcat_obj=models.ProductSubCategory.objects.get(name=subcat_name)

            #parsed the post data for json and stored it in a list
            json_text=request.POST['filter_Data']
            filter_data_list=json.loads(json_text)

            if('sorting_items' in request.POST and request.POST['sorting_items']):
                sort_data_list=json.loads(request.POST['sorting_items'])
                for sort_data in sort_data_list:
                    if (sort_data['filter_name']=='price_sort'):
                        if(sort_data['filter_value']=='priceAsc'):
                            price_ascending=True
                        elif(sort_data['filter_value']=='priceDsc'):
                            price_descending=True


            productsubfilters_list=[]
            productprimefilters_list=[]
            productprimefilterdata_list=[]
            productsubfilterdata_list=[]
            ads_list=[]
            ads_json_serializable_list=[]
            filter_empty=False

            if len(filter_data_list) is 0:
                filter_empty=True

            elif len(filter_data_list) is 2:
                for data in filter_data_list:
                    if data['filter_id']=='pricefilter':
                        filter_empty=True
                        break

            else:
                filter_empty=False


            for filter_data in filter_data_list:
                if filter_data['filter_id'] == 'subfilter':
                    productsubfilters_list.append(models.ProductSubFilter.objects.get(subcategory=subcat_obj,name=filter_data['filter_name']))

            for filter_data in filter_data_list:
                if filter_data['filter_id'] == 'primefilter':
                    productprimefilters_list.append(models.ProductPrimeFilter.objects.get(product_prime_category=subcat_obj.product_prime_category,name=filter_data['filter_name']))

            for productsubfilter in productsubfilters_list:
                for filter_data in filter_data_list:
                    if filter_data['filter_id'] == 'subfilter':
                        productsubfilterdata_list.append(models.ProductSubFilterData.objects.filter(product_sub_filter=productsubfilter,value=filter_data['filter_value']))

            for productprimefilter in productprimefilters_list:
                for filter_data in filter_data_list:
                    if filter_data['filter_id'] == 'primefilter':
                        productsubfilterdata_list.append(models.ProductPrimeFilterData.objects.filter(product_prime_filter=productprimefilter, value=filter_data['filter_value']))

            for productsubfilterdata_innerlist in productsubfilterdata_list:
                for productsubfilterdata in productsubfilterdata_innerlist:
                    ads_list.append(productsubfilterdata.ad)

            for productprimefilterdata_innerlist in productprimefilterdata_list:
                for productprimefilterdata in productprimefilterdata_innerlist:
                    if productprimefilterdata.ad not in ads_list:
                        ads_list.append(productprimefilterdata.ad)

            new_ads_list=[]
            for ad in ads_list:
                if ad not in new_ads_list and ad.subcategory==subcat_obj:
                    new_ads_list.append(ad)

            if len(new_ads_list) is 0 and filter_empty:
                for ad in models.ProductAd.objects.filter(subcategory=subcat_obj):
                    new_ads_list.append(ad)


            price_data=request.POST['price_data'].split('_')
            price_min=float(price_data[0])
            price_max=float(price_data[1])

            if price_ascending:
                new_ads_list.sort(key=lambda x:x.price)
            elif price_descending :
                new_ads_list.sort(key=lambda x:x.price,reverse=True)
            else:
                pass


            for ad in new_ads_list:
                if ad.price>=price_min and ad.price<=price_max:
                    ad_dict={}
                    ad_dict['id']=ad.id
                    ad_dict['title']=ad.title
                    ad_dict['description']=ad.description
                    ad_dict['price']=ad.price
                    ad_dict['duration']=unicode(ad.ad_post_duration)[0:unicode(ad.ad_post_duration).find('.')]
                    ad_dict['city_name']=ad.city.name_of_city
                    ad_dict['locality_name']=ad.locality.name_of_locality
                    ad_dict['subcategory_name']=ad.subcategory.name
                    ads_json_serializable_list.append(ad_dict)

                

            return HttpResponse(json_encoder_obj.encode(ads_json_serializable_list))
    return HttpResponse('<h1>no data</h1>')


def post_form(request):
    context_dict={}
    template_obj=loader.get_template("fringe_x/test.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))

def post_data(request):
    if request.method=='POST':
        if True:
            abcobj=models.Article()
            abcobj.name=request.POST['title']
            handle_uploaded_files(request.FILES['file_control'])
            abcobj.image_url=os.path.join('/','static','fringe_x','product_images',request.FILES['file_control'].name)
            abcobj.save()

    return HttpResponse('<h1>No post data found!<h1>')

def login(request):
    context_dict={}
    if(request.method=="POST"):
        email=request.POST["work_email"]
        users=models.User.objects.filter(corporate_email_id=email)
        if(len(users)==0):
            context_dict["login_error_context"]="login error"
        elif(len(users)==1):
            user_c=users[0]
            sec_creds=models.UserSecurityCreds.objects.get(user=user_c)
            current_hash_obj=hashlib.sha512(request.POST["password"]+sec_creds.salt)
            current_hash=current_hash_obj.hexdigest()
            if(current_hash==sec_creds.pass_hash):
                request.session["user_id"]=user_c.id
                return HttpResponseRedirect("/fringe_circle/")
            context_dict["login_error_context"]="login error"

    template_obj=loader.get_template("fringe_x/login.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))

def logout(request):
    if("user_id" in request.session and request.session["user_id"]):
        del request.session["user_id"]
        return HttpResponseRedirect("/fringe_circle/")
    return HttpResponse("/fringe_circle/")

def signup(request):
    context_dict={}
    if(request.method=="POST"):
        requested_corporate_email=request.POST["workEmail"]
        requested_alternate_email=request.POST["altEmail"]
        already_registered_check=models.User.objects.filter(corporate_email_id=requested_corporate_email)
        already_exists=False

        if(len(already_registered_check) !=0):
            already_exists=True

        results=models.TempRegistrations.objects.filter(corporate_email=requested_corporate_email)

        if(len(results)==0 and not already_exists):
            new_temp_registration=models.TempRegistrations()
            new_temp_registration.temp_token=uuid.uuid4().hex
            new_temp_registration.alternate_email=requested_alternate_email
            new_temp_registration.corporate_email=requested_corporate_email
            new_temp_registration.save()
            msg='follow link: http://92.222.27.234:8000/fringe_circle/register_user/%s' %(new_temp_registration.temp_token)
            sent_flag=sendmail("admin@fringecircle.com",new_temp_registration.corporate_email,msg)
            return HttpResponseRedirect("/fringe_circle/")
        if(len(results)==1 or already_exists):
            context_dict["signup_error_context"]="%s is already registered" %(requested_corporate_email)

    template_obj=loader.get_template("fringe_x/new_signup.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))


def handle_uploaded_files(f):
    with open(os.path.join(settings.BASE_DIR,'fringe_x','static','fringe_x','product_images','title_image.jpg',),'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def register_user_page(request,registration_token=None):
    context_dict={}

    if(registration_token is not None):
        temp_reg_objs=models.TempRegistrations.objects.filter(temp_token=registration_token)

        if(len(temp_reg_objs)==0):
            return HttpResponseNotFound("Invalid token:Page not found")
        context_dict["states_context"]=models.State.objects.all()
        temp_reg=temp_reg_objs[0]
        context_dict["registration_token_context"]=registration_token
        context_dict["work_email_context"]=temp_reg.corporate_email
        context_dict["alt_email_context"]=temp_reg.alternate_email


    template_obj=loader.get_template("fringe_x/register_detail.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))

def register_user(request,registration_token=None):
    if(registration_token is not None):
        if(request.method=="POST"):
            user_obj=models.User()
            sec_cred_obj=models.UserSecurityCreds()
            salt=uuid.uuid4().hex
            password=request.POST["secondPass"]
            user_obj.name=request.POST["fullname"]
            user_obj.corporate_email_id=request.POST["work_email"]
            user_obj.alternate_email_id=request.POST["alt_email"]
            user_obj.contact_no="nill"
            user_obj.state=models.State.objects.get(name_of_state=request.POST["state_select_alert"])
            user_obj.city=models.City.objects.get(name_of_city=request.POST["city_select_alert"],state=user_obj.state)
            user_obj.locality=models.Locality.objects.get(name_of_locality=request.POST["locality_select_alert"],city=user_obj.city)
            user_obj.save()

            sec_cred_obj.user=user_obj
            sec_cred_obj.salt=salt
            hash_obj=hashlib.sha512(password+salt)
            sec_cred_obj.pass_hash=hash_obj.hexdigest()
            sec_cred_obj.save()
            temp_reg_obj=models.TempRegistrations.objects.filter(temp_token=registration_token)[0]
            temp_reg_obj.delete()
            return HttpResponseRedirect("/fringe_circle/")
    return HttpResponse("<h1>Registration Error: Try Later</h1>")


def send_registration_email(request):

    if(request.method=="POST"):
        requested_corporate_email=request.POST["workEmail"]
        requested_alternate_email=request.POST["altEmail"]
        results=models.TempRegistrations.objects.filter(corporate_email=requested_corporate_email)

        if(len(results)==0):
            new_temp_registration=models.TempRegistrations()
            new_temp_registration.temp_token=uuid.uuid4().hex
            new_temp_registration.alternate_email=requested_alternate_email
            new_temp_registration.corporate_email=requested_corporate_email
            new_temp_registration.save()
            msg='follow link: http://92.222.27.234:8000/fringe_circle/register_user/%s' %(new_temp_registration.temp_token)
            sent_flag=sendmail("admin@fringecircle.com",new_temp_registration.corporate_email,msg)
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

def sendmail(sndr,rcvr,msg):
    try:
        smtp_obj=smtplib.SMTP("localhost")
        smtp_obj.sendmail(sndr,rcvr,msg)
        return True

    except SMTPException:
        return False

def user_signed_in(request):
    if("user_id" in request.session and request.session["user_id"]):
        return True
    else:
        return False