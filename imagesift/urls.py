try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import patterns, url
from views import (NullView,)


urlpatterns = patterns('imagesift.views',
                       url(r'^$', NullView.as_view(), name='null'),
                       url(r'^gallery/', include('imagestore.urls', namespace='imagestore')),


                       )

