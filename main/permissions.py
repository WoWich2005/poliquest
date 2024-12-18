from rest_framework import permissions


class IsUserHasPointPermissionsOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return view.kwargs.get('point_id') in [point.id for point in request.user.points.all()]
