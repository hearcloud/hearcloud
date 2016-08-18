from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrSuperuserOrDenyAccess(BasePermission):
    def has_object_permission(self, request, view, obj, **kwargs):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True  # It's superuser, so he can access
        else:
            # Check if it's the owner of the object
            return obj.user == request.user and request.user.id == obj.objects.get(request=kwargs["slug"]).user.id
