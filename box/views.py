import os
from itertools import chain

from django.views.generic import TemplateView
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.views.generic import View
from django.core.files import File
from django.utils.timezone import now as tznow
from django.http import HttpResponseForbidden, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from base64 import decodestring

from .models import Song
from .forms import SongForm, UpdateSongForm
from .serializers import SongSerializer

from users.models import User

class IndexView(TemplateView):
    """
    View to show a list of all the user stored songs
    """
    template_name = 'box/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(
            all_songs = Song.objects.filter(user=self.request.user).order_by('title'),
            today = tznow(),
            **kwargs
        )
        return context

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('home:index')

        return super(IndexView, self).get(request)

class SongAjaxCreateView(AjaxCreateView):
    """
    View to allow users store new songs into the db.
    """
    form_class = SongForm
    template_name = "box/song_form.html"


    def form_valid(self, form):
        """
        Overriding the form_valid method to do the ID3 tags stuff before store
        the song
        """
        form.instance.user = self.request.user

        song = form.save(commit=False)

        song.file = form.cleaned_data['file']

        song.save(create=True)

        return super(SongAjaxCreateView, self).form_valid(form)


class SongDetailView(generic.DetailView):
    template_name = "box/detail.html"
    model = Song

    def get_context_data(self, **kwargs):
        context = super(SongDetailView, self).get_context_data(
            today = tznow(),
            **kwargs
        )
        return context

    def get(self, request, **kwargs):
        # Check if the user is trying to get a song which doesn't own
        if not request.user.id == Song.objects.get(slug=kwargs['slug']).user.id:
            return handler401(request)

        return super(SongDetailView, self).get(request)

class SongUpdateView(AjaxUpdateView):
    form_class = UpdateSongForm
    model = Song
    pk_url_kwarg = 'song_id'

    def form_valid(self, form):
        """
        Overriding the form_valid method to do the ID3 tags stuff over the
        stored file song
        """
        form.instance.user = self.request.user

        song = form.save(commit=False) # Creates an object from the form but doesn't save it into db yet

        # Save into db
        song.save(update=True)

        return super(SongUpdateView, self).form_valid(form)


class SongDelete(AjaxDeleteView):
    model = Song
    #pk_url_kwarg = 'song_id'
    success_url = reverse_lazy('box:index') # Redirect to index after successfully delete a song

def song_download(request, username, slug):
    song = Song.objects.get(slug=slug)

    if not request.user.id == song.user.id:
        return handler401(request)

    fsock = open(song.file.path, 'rb')
    response = HttpResponse(fsock, content_type="audio/mpeg")
    response['Content-Disposition'] = "attachment; filename=%s - %s.%s" % \
                                     (song.artist, song.title, song.file_type)
    return response

def song_search(request):
    """
    View to show a list of the songs that match an user search
    """
    template_name = 'box/index.html'

    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    songs = Song.objects.filter(user=request.user).filter(title__contains=search_text).order_by('title')

    return render_to_response(template_name, {'all_songs': songs})
        

##################### ERROR ##########################
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler401(request):
    response = render_to_response('401.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 401
    return response
