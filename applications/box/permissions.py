from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrDenyAccess(BasePermission):
    def has_object_permission(self, request, view, obj, **kwargs):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user and request.user.id == obj.objects.get(request=kwargs["slug"]).user.id
