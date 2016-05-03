import os

from django.views.generic import TemplateView
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.views.generic import View
from django.core.files import File
from django.utils.timezone import now as tznow

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mutagen.mp3 import MP3

from base64 import decodestring
from datetime import timedelta

from .models import Song
from .forms import SongForm, UpdateSongForm
from .serializers import SongSerializer
from .functions import mp3_tags_to_song_model, tags_from_song_model_to_mp3

from users.models import User

class IndexView(TemplateView):
    """ 
    View to show a list of all the user stored songs
    """
    template_name = 'box/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(
            all_songs = Song.objects.filter(user=self.request.user),
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

        song = form.save(commit=False) # Creates an object from the form but doesn't save it into db yet
            
        # Cleaned (normalized) data
        audio_file = form.cleaned_data["audio_file"]
        audio_file_path = audio_file.temporary_file_path()
        audio_file_name = audio_file.name
        audio_extension = os.path.splitext(audio_file_name)[1]
        print audio_extension

        # MP3 ID3 stuff
        if audio_extension==".mp3":
            song = mp3_tags_to_song_model(audio_file_name, audio_file_path, song)

            # Get the song length
            mutagen_mp3 = MP3(audio_file_path)
            song.duration = timedelta(seconds=int(mutagen_mp3.info.length))
    
        # If there is no 'Title' attribute, use the filename as title
        if not song.song_title:
            song.song_title = os.path.splitext(audio_file_name)[0]

        # Save into db
        song.save()

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
            
        # MP3 ID3 stuff
        tags_from_song_model_to_mp3(song)

        # Save into db
        song.save()

        return super(SongUpdateView, self).form_valid(form)


class SongDelete(AjaxDeleteView):
    model = Song
    pk_url_kwarg = 'song_id'
    success_url = reverse_lazy('box:index') # Redirect to index after successfully delete a song
