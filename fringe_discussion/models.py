from django.db import models

from fringe_x import models as fringex_models
# Create your models here.

class DiscussionPrimeCategory(models.Model):
    name=models.CharField(max_length=60)

    def __unicode__(self):
        return self.name


class DiscussionSubCategory(models.Model):
    discussion_prime_category=models.ForeignKey(DiscussionPrimeCategory)
    name=models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

class Discussion(models.Model):
    title=models.CharField(max_length=60)
    description=models.CharField(max_length=300)
    publish_date=models.DateTimeField()
    user=models.ForeignKey(fringex_models.User)
    category=models.ForeignKey(DiscussionPrimeCategory)
    subcategory=models.ForeignKey(DiscussionSubCategory)
    location_specific=models.CharField(max_length=3)
    like_count=models.IntegerField()
    unlike_count=models.IntegerField()
    answers_count=models.IntegerField()
    state=models.ForeignKey(fringex_models.State,null=True)
    city=models.ForeignKey(fringex_models.City,null=True)
    locality=models.ForeignKey(fringex_models.Locality,null=True)

    def __unicode__(self):
        return self.title

class DiscussionLikeDislikeTrack(models.Model):
    like_dislike_status=models.CharField(max_length=7)
    discussion=models.ForeignKey(Discussion)
    user=models.ForeignKey(fringex_models.User)



class FollowingTrack(models.Model):
    follower=models.ForeignKey(fringex_models.User, related_name="the_follower")
    followed=models.ForeignKey(fringex_models.User, related_name="the_followed")

class DiscussionReply(models.Model):
    text=models.CharField(max_length=1000)
    reply_date=models.DateTimeField()
    discussion=models.ForeignKey(Discussion)
    like_count=models.IntegerField()
    unlike_count=models.IntegerField()
    user=models.ForeignKey(fringex_models.User)

class DiscussionReplyLikeDislikeTrack(models.Model):
    like_dislike_status=models.CharField(max_length=7)
    reply=models.ForeignKey(DiscussionReply)
    user=models.ForeignKey(fringex_models.User)