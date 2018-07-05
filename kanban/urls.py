from django.urls import path, re_path
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = []

urlpatterns = [
    *urlpatterns,
    path('', views.index),
    path("_update_kind/", views.update_kind),
    re_path(r'^(?P<path>[\w_-]+)$', views.board),
    re_path(r'^(?P<path>[\w_-]+)+/done/$', views.done),
    re_path(r'^(?P<path>[\w_-]+)+/issue/$', views.create_issue),
    re_path(r'^(?P<path>[\w_-]+)+/backlog/$', views.backlog),
    re_path(r'^(?P<path>[\w_-]+)+/issue/(?P<issue_id>\d+)$', views.issue_detail),
    re_path(r'^(?P<path>[\w_-]+)+/issue/(?P<issue_id>\d+)$', views.issue_edit),
]

