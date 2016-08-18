from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(
                reverse('box:index', kwargs={'username': request.user.slug})
            )

        return super(IndexView, self).get(request)
