from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowPostWithoutAuthentication(BasePermission):
    """
    Permission that allows POST to everyone, but requires authentication for other methods.
    """

    def has_permission(self, request, view):
        # Allows POST to everyone
        if request.method == "POST":
            return True

        # Requires authentication for other methods
        return request.user and request.user.is_authenticated
