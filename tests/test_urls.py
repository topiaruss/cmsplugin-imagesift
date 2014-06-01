from django.contrib import admin
from django.conf.urls import url, patterns, include

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gallery/', include('imagesift.urls', namespace='imagesift')),
    url(r'', include('cms.urls')),
)