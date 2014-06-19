from django.conf.urls import patterns, url

from imagesift.views import ImageView, ajax_more


urlpatterns = patterns('',
    url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
    url(r'^more/(?P<gall>\d+)/$', ajax_more, name='ajax_more'),
    )

