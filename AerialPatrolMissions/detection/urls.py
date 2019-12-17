# -*- coding: utf-8 -*-
from django.urls import path, include
import detection.views
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('profile_demo/', detection.views.profile_demo),
    path('upload_demo/<int:upload_page_id>', detection.views.upload_demo),
    path('get_all_missions/', detection.views.get_all_missions),
    path('create_mission/', detection.views.create_mission),
    path('get_mission_info/', detection.views.get_mission_info),
    path('upload/', detection.views.upload),
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]