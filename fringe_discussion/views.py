import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Template
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render
from fringe_x import models as fringex_models
from fringe_discussion import models



# Create your views here.
def board_index(request,discussion_cat=None,page_index=None):
    context_dict={}
    if(user_signed_in(request)):
        current_user=fringex_models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    else:
        return HttpResponseRedirect("/fringe_circle/login/")

    if ('state_session' in request.session and
        'city_session' in request.session):
        if (request.session['state_session']
            and request.session['city_session']):
            context_dict['location_state_context']=request.session['state_session']
            context_dict['location_city_context']=request.session['city_session']
            context_dict['all_states_context']=fringex_models.State.objects.all()

    if (discussion_cat is not None):
        if(discussion_cat.lower()=='all'):
            context_dict['discussions_context']=models.Discussion.objects.all()
            context_dict['current_cat_context']='All'
        else:
            context_dict['discussions_context']=models.Discussion.objects.filter(category=\
                models.DiscussionPrimeCategory.objects.get(name=discussion_cat))
            context_dict['current_cat_context']=discussion_cat

    context_dict['prime_cat_context']=models.DiscussionPrimeCategory.objects.all()
    context_dict['sub_cat_context']=models.DiscussionSubCategory.objects.all()


    template_obj=loader.get_template("fringe_discussion/fringe-board.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))



def individual_discussion(request,discussion_id=None):
    context_dict={}
    if(user_signed_in(request)):
        current_user=fringex_models.User.objects.get(id=request.session["user_id"])
        context_dict["current_user_context"]=current_user
    else:
        return HttpResponseRedirect("/fringe_circle/login/")

    if ('state_session' in request.session and 'city_session' in request.session):
        if request.session['state_session'] and request.session['city_session']:
            context_dict['location_state_context']=request.session['state_session']
            context_dict['location_city_context']=request.session['city_session']
            context_dict['all_states_context']=fringex_models.State.objects.all()

    if (discussion_id is not None):
        context_dict['discussion_obj_context']=models.Discussion.objects.get(id=discussion_id)
        context_dict['replies_context']=models.DiscussionReply.objects.filter(discussion=context_dict['discussion_obj_context'])

    template_obj=loader.get_template("fringe_discussion/individual-discussion.html")
    context_obj=RequestContext(request,context_dict)
    return HttpResponse(template_obj.render(context_obj))


#view to get sub category names through ajax
def get_subcategories_ajax(request,primecat_name=None):
    json_encoder_obj=json.JSONEncoder()
    primecat_obj=models.DiscussionPrimeCategory.objects.get(name=primecat_name)
    subcat_name_list=[]
    if primecat_name is not None:
        for subcat in models.DiscussionSubCategory.objects.filter(discussion_prime_category=primecat_obj):
            subcat_name_list.append(subcat.name)

    return HttpResponse(json_encoder_obj.encode(subcat_name_list))

def create_discussion(request):
    if request.method=='POST':
        discussion_object=models.Discussion()
        discussion_object.title=request.POST['discussion_title_postdisc']
        discussion_object.category=models.DiscussionPrimeCategory.objects.get(name=request.POST['post_disc_prime_cat_name'])
        discussion_object.subcategory=models.DiscussionSubCategory.objects.get(name=request.POST['post_disc_sub_cat_name'],discussion_prime_category=discussion_object.category)
        discussion_object.location_specific=request.POST['location_specific_radio']
        if request.POST['location_specific_radio']=='Yes':
            discussion_object.state=fringex_models.State.objects.get(name_of_state=request.POST['state_select_postdisc'])
            discussion_object.city=fringex_models.City.objects.get(name_of_city=request.POST['city_select_postdisc'],state=discussion_object.state)
            discussion_object.locality=fringex_models.Locality.objects.get(name_of_locality=request.POST['state_select_postdisc'],city=discussion_object.city)

        discussion_object.description=request.POST['description_postdisc']
        discussion_object.like_count=0
        discussion_object.unlike_count=0
        discussion_object.answers_count=0
        discussion_object.publish_date=timezone.localtime(timezone.now())
        discussion_object.user=fringex_models.User.objects.all()[0]
        discussion_object.save()

    return HttpResponseRedirect('/fringe_circle/fringe_board/all/')

def create_like_dislike_reply(request,like_dislike_status,reply_id=None):
    json_encoder_obj=json.JSONEncoder()
    unselected_stat=""
    stat_dict={}
    if(like_dislike_status=="like"):
        unselected_stat="unlike"
    else:
        unselected_stat="like"
    if(user_signed_in(request)):
        current_user=fringex_models.User.objects.get(id=request.session["user_id"])
        current_reply=models.DiscussionReply.objects.get(id=reply_id)
        all_like_count=current_reply.like_count
        all_unlike_count=current_reply.unlike_count

        current_stat_results=models.DiscussionReplyLikeDislikeTrack.objects.filter(user=current_user,reply=current_reply)
        if(len(current_stat_results)==0):
            stat_obj=models.DiscussionReplyLikeDislikeTrack()
            stat_obj.user=current_user
            stat_obj.discussion=current_reply
            stat_obj.like_dislike_status=like_dislike_status
            stat_obj.save()
            if(like_dislike_status=="like"):
                current_reply.like_count=int(all_like_count)+1
                current_reply.save()
            else:
                current_reply.unlike_count=int(all_unlike_count)+1
                current_reply.save()

            stat_dict[unselected_stat]="flat"
            stat_dict[like_dislike_status]="inc"
            return HttpResponse(json_encoder_obj.encode(stat_dict))

        elif(len(current_stat_results)==1):
            if (current_stat_results[0].like_dislike_status==like_dislike_status):
                stat_dict[unselected_stat]="flat"
                stat_dict[like_dislike_status]="flat"
                return HttpResponse(json_encoder_obj.encode(stat_dict))
            current_stat_results[0].delete()
            stat_obj=models.DiscussionReplyLikeDislikeTrack()
            stat_obj.user=current_user
            stat_obj.discussion=current_reply
            stat_obj.like_dislike_status=like_dislike_status
            stat_obj.save()
            if(like_dislike_status=="like"):
                current_reply.like_count=int(all_like_count)+1
                if (all_unlike_count!=0):
                    current_reply.unlike_count=int(all_unlike_count)-1
                current_reply.save()
            else:
                current_reply.unlike_count=int(all_unlike_count)+1
                if(all_like_count!=0):
                    current_reply.like_count=int(all_like_count)-1
                current_reply.save()

            stat_dict[unselected_stat]="dec"
            stat_dict[like_dislike_status]="inc"
            return HttpResponse(json_encoder_obj.encode(stat_dict))
    else:
        return HttpResponse(json_encoder_obj.encode(stat_dict))

def createLikeDislike(request,like_dislike_status=None,discussion_id=None):
    json_encoder_obj=json.JSONEncoder()
    unselected_stat=""
    stat_dict={}
    if(like_dislike_status=="like"):
        unselected_stat="unlike"
    else:
        unselected_stat="like"
    if(user_signed_in(request)):
        current_user=fringex_models.User.objects.get(id=request.session["user_id"])
        current_discussion=models.Discussion.objects.get(id=discussion_id)
        all_like_count=current_discussion.like_count
        all_unlike_count=current_discussion.unlike_count

        current_stat_results=models.DiscussionLikeDislikeTrack.objects.filter(user=current_user,discussion=current_discussion)
        if(len(current_stat_results)==0):
            stat_obj=models.DiscussionLikeDislikeTrack()
            stat_obj.user=current_user
            stat_obj.discussion=current_discussion
            stat_obj.like_dislike_status=like_dislike_status
            stat_obj.save()
            if(like_dislike_status=="like"):
                current_discussion.like_count=int(all_like_count)+1
                current_discussion.save()
            else:
                current_discussion.unlike_count=int(all_unlike_count)+1
                current_discussion.save()

            stat_dict[unselected_stat]="flat"
            stat_dict[like_dislike_status]="inc"
            return HttpResponse(json_encoder_obj.encode(stat_dict))

        elif(len(current_stat_results)==1):
            if (current_stat_results[0].like_dislike_status==like_dislike_status):
                stat_dict[unselected_stat]="flat"
                stat_dict[like_dislike_status]="flat"
                return HttpResponse(json_encoder_obj.encode(stat_dict))
            current_stat_results[0].delete()
            stat_obj=models.DiscussionLikeDislikeTrack()
            stat_obj.user=current_user
            stat_obj.discussion=current_discussion
            stat_obj.like_dislike_status=like_dislike_status
            stat_obj.save()
            if(like_dislike_status=="like"):
                current_discussion.like_count=int(all_like_count)+1
                if (all_unlike_count!=0):
                    current_discussion.unlike_count=int(all_unlike_count)-1
                current_discussion.save()
            else:
                current_discussion.unlike_count=int(all_unlike_count)+1
                if(all_like_count!=0):
                    current_discussion.like_count=int(all_like_count)-1
                current_discussion.save()

            stat_dict[unselected_stat]="dec"
            stat_dict[like_dislike_status]="inc"
            return HttpResponse(json_encoder_obj.encode(stat_dict))
    else:
        return HttpResponse(json_encoder_obj.encode(stat_dict))


def follow_user(request,target_user_id=None):
    follow_status_dict={}
    json_encoder_obj=json.JSONEncoder()
    if(user_signed_in(request)):
        current_user=fringex_models.User.objects.get(id=request.session["user_id"])
        follow_status_results=models.FollowingTrack.objects.filter(follower=current_user,followed=target_user_id)
        if(len(follow_status_results)==0):
            follow_obj=models.FollowingTrack()
            follow_obj.follower=current_user
            follow_obj.followed=fringex_models.User.objects.get(id=target_user_id)
            follow_obj.save()
            follow_status_dict["follow_status"]="follow_start"
            return HttpResponse(json_encoder_obj.encode(follow_status_dict))
        else:
            follow_status_results[0].delete()
            follow_status_dict["follow_status"]="follow_stop"
            return HttpResponse(json_encoder_obj.encode(follow_status_dict))
    else:
        return HttpResponse(json_encoder_obj.encode(follow_status_dict))

def create_discussion_reply_through_form(request,discussion_id=None):
    if(user_signed_in(request)):
        current_user=fringex_models.User.objects.get(id=request.session["user_id"])
        if(request.method=="POST"):
            reply_obj=models.DiscussionReply()
            reply_obj.text=request.POST["reply_text"]
            reply_obj.discussion=models.Discussion.objects.get(id=discussion_id)
            reply_obj.like_count=0
            reply_obj.unlike_count=0
            reply_obj.user=current_user
            reply_obj.reply_date=timezone.localtime(timezone.now())
            reply_obj.save()
            discussion_obj=models.Discussion.objects.get(id=discussion_id)
            discussion_obj.answers_count+=1
            discussion_obj.save()
            #status_dict["reply_status"]="%s" %(reply_obj.id)
            return HttpResponseRedirect("/fringe_circle/fringe_individual_discussion/"+discussion_id)

def create_discussion_reply(request,discussion_id=None):
    json_encoder_obj=json.JSONEncoder()
    status_dict={}
    if(user_signed_in(request)):
        current_user=fringex_models.User.objects.get(id=request.session["user_id"])
        if(request.method=="POST"):
            reply_obj=models.DiscussionReply()
            reply_obj.text=request.POST["reply_text"]
            reply_obj.discussion=models.Discussion.objects.get(id=discussion_id)
            reply_obj.like_count=0
            reply_obj.unlike_count=0
            reply_obj.reply_date=timezone.localtime(timezone.now())
            reply_obj.user=current_user
            reply_obj.save()
            discussion_obj=models.Discussion.objects.get(id=discussion_id)
            discussion_obj.answers_count+=1
            discussion_obj.save()
            status_dict["reply_id"]="%s" %(reply_obj.id)
            status_dict["text"]=reply_obj.text
            status_dict["likes"]=reply_obj.like_count
            status_dict["unlikes"]=reply_obj.unlike_count
            status_dict["reply_user"]=reply_obj.user.name
            status_dict["reply_date"]=str(reply_obj.reply_date)
            status_dict["discussion_user"]=reply_obj.discussion.user.name
            return HttpResponse(json_encoder_obj.encode(status_dict))
        else:
            status_dict["reply_status"]="reply_failed"
            return HttpResponse(json_encoder_obj.encode(status_dict))

    else:
        status_dict["reply_status"]="reply_failed"
        return HttpResponse(json_encoder_obj.encode(status_dict))



def get_filter_discussions(request,ads_params=None):
    pass

def user_signed_in(request):
    if("user_id" in request.session and request.session["user_id"]):
        return True
    else:
        return False