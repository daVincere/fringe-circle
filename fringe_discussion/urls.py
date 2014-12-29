__author__ = 'sud'
from django.conf.urls import patterns, url
from fringe_discussion import views

urlpatterns=patterns('',
                     url('^/fringe_board/(?P<discussion_cat>.+)/$',views.board_index),
                     url('^/fringe_individual_discussion/(?P<discussion_id>.+)/$',views.individual_discussion),
                     url('^/post_discussion/$',views.create_discussion),
                     url('^/get_subcat_names/(?P<primecat_name>.+)/$',views.get_subcategories_ajax),
                     url('^/get_filter_discussions/$',views.get_filter_discussions),
                     url('^/get_filter_discussions/(?P<ads_params>.+)/$',views.get_filter_discussions),
                     url('^/like_dislike/(?P<like_dislike_status>.+)/(?P<discussion_id>.+)/$',views.createLikeDislike),
                     url('^/like_dislike_reply/(?P<like_dislike_status>.+)/(?P<reply_id>.+)/$',views.create_like_dislike_reply),
                     url('^/follow_user/(?P<target_user_id>.+)/$',views.follow_user),
                     url('^/create_discussion_reply/(?P<discussion_id>.+)/$',views.create_discussion_reply),
                     url('^/create_discussion_reply_form/(?P<discussion_id>.+)/$',views.create_discussion_reply_through_form),
                     )