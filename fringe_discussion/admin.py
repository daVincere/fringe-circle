from django.contrib import admin
from fringe_discussion import models

# Register your models here.
admin.site.register(models.DiscussionPrimeCategory)
admin.site.register(models.DiscussionSubCategory)
admin.site.register(models.Discussion)
admin.site.register(models.DiscussionLikeDislikeTrack)
admin.site.register(models.DiscussionReply)