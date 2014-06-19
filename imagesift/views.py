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
    plugin = get_object_or_404(GalleryPlugin, pk=gall)
    start = request.GET.get('start', 0)
    reverse = request.GET.get('reverse', False)
    back = request.GET.get('back', '')
    # WORK IN PROGRESS
    #TODO: add images
    return render_to_response('imagesift_more.html', dict(start=start, reverse=reverse, back=back))

