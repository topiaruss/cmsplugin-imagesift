from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from imagestore.models import Album, Image
from imagestore.models import image_applabel, image_classname
from imagestore.models import album_applabel, album_classname
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tagging.models import TaggedItem
from tagging.utils import get_tag

from django.db.models import Q



class ImageView(DetailView):
    context_object_name = 'image'
    template_name = 'image_detail.html'
    model = Image

    # def get(self, request, *args, **kwargs):
    #     import pdb; pdb.set_trace()
    #     pass

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #    #
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

    # def get_context_data(self, **kwargs):
    #     context = super(ImageView, self).get_context_data(**kwargs)
    #     image = context['image']
    #
    #     base_qs = self.get_queryset()
    #     count = base_qs.count()
    #     img_pos = base_qs.filter(
    #         Q(order__lt=image.order)|
    #         Q(id__lt=image.id, order=image.order)
    #     ).count()
    #     next = None
    #     previous = None
    #     if count - 1 > img_pos:
    #         try:
    #             next = base_qs.filter(
    #                 Q(order__gt=image.order)|
    #                 Q(id__gt=image.id, order=image.order)
    #             )[0]
    #         except IndexError:
    #             pass
    #     if img_pos > 0:
    #         try:
    #             previous = base_qs.filter(
    #                 Q(order__lt=image.order)|
    #                 Q(id__lt=image.id, order=image.order)
    #             ).order_by('-order', '-id')[0]
    #         except IndexError:
    #             pass
    #     context['next'] = next
    #     context['previous'] = previous
    #     context.update(self.e_context)
    #     return context



