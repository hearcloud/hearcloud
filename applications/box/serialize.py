# encoding: utf-8
import mimetypes
import re
from django.core.urlresolvers import reverse


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize_file(instance, file_attr='file', thumbnail_attr='artwork'):
    obj = getattr(instance, file_attr)
    thumbnail = getattr(instance, thumbnail_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        'type': mimetypes.guess_type(obj.path)[0],
        'thumbnailUrl': thumbnail.url,
        'size': obj.size,
        'deleteUrl': reverse('box:song-delete', kwargs={'username': instance.user.username, 'slug': instance.slug}),
        'deleteType': 'DELETE',
    }

