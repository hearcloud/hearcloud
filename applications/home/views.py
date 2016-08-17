from django.views.generic import TemplateView
from django.shortcuts import redirect


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            return redirect('box:index')

        return super(IndexView, self).get(request)
