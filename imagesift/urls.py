from django.conf.urls import patterns, url, include
from imagesift.views import ImageView

urlpatterns = patterns('',
    url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
    )

