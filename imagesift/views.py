import logging
import urllib

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.shortcuts import render_to_response
from models.gallery import GalleryPlugin
from imagestore.models import Image


logger = logging.getLogger(__name__)


class ImageView(DetailView):
    context_object_name = 'image'
    template_name = 'image_detail.html'
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)

        # we can only return to the page, not the specific gallery -- we have no way to find it
        # so we keep passing it along to the next image page, if prev/next are used
        back = self.request.GET.get('back')
        context.update(back=back)

        # need default geometry, in case detail invoked without a gall argument
        geometry = '500x400'

        try:
            prev = next = None

            # plugin is essential for all that follows in the try:
            gall_pk = int(self.request.GET['gall'])
            plugin = GalleryPlugin.objects.get(pk=gall_pk)

            # compute the prev and next, returning None for one/both, as appropriate
            image = kwargs['object']
            prev, next = plugin.get_immediate_neighbours(image)

            # get geometry
            geometry = plugin.image_geometry

            # and stash all in the context
            context.update(prev=prev, next=next, gall_plugin=plugin)
        except:
            pass

        # set the default, or the setting from the instance
        context.update(geometry=geometry)

        return context

def url_querystring(**kwargs):
    return urllib.urlencode(kwargs)

def get_batch_context(request, instance, context={}):

    try:
        start = int(request.GET.get('start', u'0'))
    except:
        start = 0

    try:
        reverse = request.GET.get('reverse', u'1')
        reverse = reverse and int(reverse)>0 and reverse not in [u'false', u'False']
    except:
        reverse = True

    back = request.GET.get('back', '')

    bundle = instance.get_filtered_queryset_bundle(request, reverse)
    images = bundle['images']

    def_limit = settings.IMAGESIFT_DEFAULT_LIMIT_AJAX_MORE
    limit = (instance.thumbnail_limit if instance.thumbnail_limit else def_limit)
    end = start + limit
    final_batch = end >= len(images)
    if final_batch:
        end = len(images)
    ret = images[start:end]

    prev_start = start  # so that we can build image detail links back to this current block
    # confusing if we were to continue incrementing after final batch, so advance conditionally
    if not final_batch:
        start = end
    remaining = len(images) - end
    old_limit = limit
    limit = min(remaining, limit)

    logger.debug('len images:%s' % request.get_full_path())
    logger.debug('len images:%s' % len(images))
    logger.debug('def limit:%s' % def_limit)
    logger.debug('old_limit:%s' % old_limit)
    logger.debug('limit:%s' % limit)
    logger.debug('prev_start:%s' % prev_start)
    logger.debug('end:%s' % end)
    logger.debug('final_batch:%s' % final_batch)
    logger.debug('len ret:%s' % len(ret))
    logger.debug('start:%s' % start)
    logger.debug('remaining:%s' % remaining)
    logger.debug('reverse:%s' % reverse)

    query = url_querystring(gall=instance.pk, start=start, back=back, reverse=reverse,
        date=bundle.get('date',''), model=bundle.get('model',''), photog=bundle.get('photog',''))

    context.update(dict(instance=instance,
                   back=back,
                   final_batch=final_batch,
                   images=ret,
                   original_imageset=bundle['original_imageset'],
                   limit=limit,
                   remaining=remaining,
                   prev_start=prev_start,
                   reverse=reverse,
                   start=start,
                   query=query # let's move over to this, ASAP
    ))





    del bundle['images']  # don't want to overwrite the images subset already in context

    context.update(bundle)

    return context

def ajax_more(request, gall):
    """
    returns the next batch of images. Template includes a button for the following batch.
    """
    instance = get_object_or_404(GalleryPlugin, pk=gall)

    context = get_batch_context(request, instance)

    return render_to_response('imagesift_more.html', context)

