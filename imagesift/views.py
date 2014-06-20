from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.shortcuts import render_to_response

from models.gallery import GalleryPlugin
from imagestore.models import Image


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


def ajax_more(request, gall):
    """
    returns the next batch of images. Template includes a button for the following batch.
    """
    instance = get_object_or_404(GalleryPlugin, pk=gall)

    try:
        start = int(request.GET.get('start', u'0'))
    except:
        start = 0

    try:
        reverse = request.GET.get('reverse', u'')
        reverse = reverse and int(reverse)>1 and reverse not in [u'false', u'False']
    except:
        reverse = False

    back = request.GET.get('back', '')

    bundle = instance.get_filtered_queryset_bundle(request)
    images = bundle['images']

    def_limit = settings.IMAGESIFT_DEFAULT_LIMIT_AJAX_MORE
    limit = (instance.thumbnail_limit if instance.thumbnail_limit else def_limit)
    end = start + limit
    final_batch = end >= len(images)
    ret = images[start:end]

    prev_start = start  # so that we can build image detail links back to this current block
    # confusing if we were to continue incrementing after final batch, so advance conditionally
    if not final_batch:
        start += end
    remaining = len(images) - start
    limit = min(remaining, limit)

    context = dict(instance=instance,
                   back=back,
                   final_batch=final_batch,
                   images=ret,
                   limit=limit,
                   remaining=remaining,
                   prev_start=prev_start,
                   reverse=reverse,
                   start=start)

    del bundle['images']  # don't want to overwrite the images subset already in context

    context.update(bundle)

    print context

    return render_to_response('imagesift_more.html', context)

