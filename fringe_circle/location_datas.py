from bs4 import BeautifulSoup as bs
import requests as rq
from fringe_x import models
from django.utils import timezone
import random
import datetime

def get_all_states():
    urlmain="http://www.commonfloor.com/cities"
    main_soup=bs(rq.get(urlmain).text)
    state_list=[]
    state_divs=main_soup.find_all('div',style="padding-bottom:2px")
    for state in state_divs:
        state_list.append(state.get_text().replace('\n',''))

    return state_list

def get_city_data(city_name="Noida"):
    urlmain="http://www.commonfloor.com/localities/index/city/"
    main_soup=bs(rq.get(urlmain+city_name).text)
    city_initials_spans=main_soup.find_all("span",style="padding-right:5px")
    city_names=[]
    for span in city_initials_spans:
        anchor =span.find("a")
        if anchor is not None:
            ansoup=bs(rq.get("http://www.commonfloor.com"+anchor.get("href")).text)
            city_divs=ansoup.find_all("div",style="padding:10px")
            for city in city_divs:
                city_names.append(city.get_text().strip())
                print "[*] %s Locaity for %s city fetched" %(city.get_text().strip(),city_name)

    return city_names

def create_localities(locality_list, city_obj):
    if len(locality_list) is not 0:
        for locality_name in locality_list:
            locobj=models.Locality()
            locobj.city=city_obj
            locobj.name_of_locality=locality_name
            locobj.save()
            print "[*] %s locality for %s city is created." %(locality_name,city_obj)



def populate_city(state_name,city_name):
    state_obj=models.State.objects.get(name_of_state=state_name)
    city_obj=models.City()
    city_obj.name_of_city=city_name
    city_obj.state=state_obj
    city_obj.save()
    create_localities(get_city_data(city_name),city_obj)


def populate_sub_masters(subfilter_name,subcategory_obj,master_list):
    subfilter_obj=models.ProductSubFilter.objects.get(name=subfilter_name,subcategory=subcategory_obj)
    for master in master_list:
        if len(master) is not 0:
            master_obj=models.ProductSubFilterMaster()
            master_obj.value=master
            master_obj.product_sub_filter=subfilter_obj
            master_obj.save()
            print "[*] %s master value for %s filter is created" %(master,subfilter_obj)

def populate_prime_masters(primefilter_name,primcat_obj,master_list):
    primefilter_obj=models.ProductPrimeFilter.objects.get(name=primefilter_name,product_prime_category=primcat_obj)
    for master in master_list:
        master=str(master)
        if len(master) is not 0:
            master_obj=models.ProductPrimeFilterMaster()
            master_obj.value=master
            master_obj.product_prime_filter=primefilter_obj
            master_obj.save()
            print "[*] %s master value for %s filter is created" %(master,primefilter_obj)


def populate_random_ads():
    primecats=models.ProductPrimeCategory.objects.all()

    for primecat in primecats:
        subcats=models.ProductSubCategory.objects.filter(product_prime_category=primecat)

        for subcat in subcats:
            print "[*]Creating ad... "

            ad=models.ProductAd()
            ad.title="%s random_ad :%s_%s" %(str(random.randrange(1,10000)),primecat.name,subcat.name)
            ad.category=primecat
            ad.description=" pretends songeant vaudrait. Gendarmes par soufflent sentiment les possedera son fourneaux superieur. Souhaitait ifs maintenant evidemment ras toi lumineuses moi. Dansent seconde fatigue toi age grandie ici aisance. Credit cran"
            ad.price=random.randrange(1200,100000)
            ad.ad_post_duration=timezone.localtime(timezone.now())
            ad.posted_by='Individual'
            ad.product_images='no'
            ad.seller=models.User.objects.all()[0]
            ad.state=models.State.objects.get(name_of_state='Delhi')
            ad.city=models.City.objects.get(name_of_city='Delhi')
            ad.locality=models.Locality.objects.filter(city=ad.city)[random.randrange(len(models.Locality.objects.filter(city=ad.city)))]
            ad.subcategory=subcat
            ad.save()
            print "[*] %s : Ad Created" % (ad.title)

            prime_filters=models.ProductPrimeFilter.objects.filter(product_prime_category=primecat)
            sub_filters=models.ProductSubFilter.objects.filter(subcategory=subcat)
            print "[*] Creating Filter Datas for ad %s" %(ad.title)

            for subfilter in sub_filters:
                sub_filter_data=models.ProductSubFilterData()
                sub_filter_data.ad=ad
                sub_filter_data.product_sub_filter=subfilter
                submasters=models.ProductSubFilterMaster.objects.filter(product_sub_filter=subfilter)
                if len(submasters) is not 0:
                    sub_filter_data.value=submasters[random.randrange(len(submasters))].value
                sub_filter_data.save()
                print "[*] SubFilter Data %s:%s created" %(subfilter.name,sub_filter_data.value)
                print "[*] Creating Master Filter Datas for ad %s" %(ad.title)

            for primefilter in prime_filters:
                prime_filter_data=models.ProductPrimeFilterData()
                prime_filter_data.ad=ad
                prime_filter_data.product_prime_filter=primefilter
                primemasters=models.ProductPrimeFilterMaster.objects.filter(product_prime_filter=primefilter)
                if len(primemasters) is not 0:
                    prime_filter_data.value=primemasters[random.randrange(len(primemasters))].value
                prime_filter_data.save()
                print "[*] Master Filter Data %s:%s created " %(primefilter,prime_filter_data.value)

    print "[*] All Ad Filters created successfully"

