from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    """
    Permission check that allows users to update
    or delete only their own articles.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
