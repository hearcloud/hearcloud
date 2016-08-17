import json

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.timezone import now as tznow
from django.views import generic
from django.views.generic import ListView, TemplateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from fm.views import AjaxUpdateView, AjaxDeleteView

from .forms import UpdateSongForm
from .models import Song, Playlist
from .response import JSONResponse, response_mimetype
from .serialize import serialize_file


class IndexView(TemplateView):
    """
    View to show a list of all the user stored songs
    """
    template_name = 'box/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(
            all_songs=Song.objects.filter(user=self.request.user).order_by('title'),
            **kwargs
        )
        return context

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('home:index')

        return super(IndexView, self).get(request)

class PlaylistListView(ListView):
    """
    View to show a list of all the playlists an user has created
    """
    template_name = 'box/playlists.html'
    model = Playlist

    def get_context_data(self, **kwargs):
        context = super(PlaylistListView, self).get_context_data(
            all_playlists=Playlist.objects.filter(user=self.request.user).order_by('name'),
            **kwargs
        )
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('home:index')

        return super(PlaylistListView, self).get(request, *args, **kwargs)

class PlaylistCreateView(CreateView):
    model = Playlist
    fields = ('name',)
    template_name = "box/playlist_create.html"

class SongCreateView(CreateView):
    model = Song
    fields = ('file',)
    template_name = "box/song_upload.html"

    def form_valid(self, form):
        # self.object = form.save()
        # files = [serialize(self.object)]
        self.object = Song.objects.create(user=self.request.user, file=form.cleaned_data['file'])
        self.object.original_filename = self.request.FILES['file'].name
        self.object.save(create=True)
        files = [serialize_file(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class SongListView(ListView):
    model = Song

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize_file(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class SongDetailView(generic.DetailView):
    template_name = "box/detail.html"
    model = Song

    def get_context_data(self, **kwargs):
        context = super(SongDetailView, self).get_context_data(
            today=tznow(),
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

        song = form.save(commit=False)  # Creates an object from the form but doesn't save it into db yet

        # Save into db
        song.save(update=True)

        return super(SongUpdateView, self).form_valid(form)


class SongDelete(AjaxDeleteView):
    model = Song
    # pk_url_kwarg = 'song_id'
    success_url = reverse_lazy('box:index')  # Redirect to index after successfully delete a song

    def delete(self, request, *args, **kwargs):
        return super(SongDelete, self).delete(request)


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


# ############################### ERROR ##################################### #
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
