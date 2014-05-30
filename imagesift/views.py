from django.views.generic import DetailView

from .models import GalleryPlugin


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

        # compute the prev and next, returning None for one/both, as appropriate
        try:
            prev = next = None

            # plugin is essential for all that follows in the try:
            gall_pk = int(self.request.GET['gall'])
            plugin = GalleryPlugin.objects.get(pk=gall_pk)
            image = kwargs['object']
            prev, next = plugin.get_immediate_neighbours(image)

            # and stash all in the context
            context.update(prev=prev, next=next, gall_plugin=plugin)
        except:
            pass
        return context
