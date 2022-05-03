from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class ReviewComment(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            if not request.user.is_authenticated:
                return False
            else:
                return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action == 'create':
            possible_options = (
                request.user.is_authenticated,
                request.user.is_admin,
                request.user.is_moderator,
            )
            return any(possible_options)
        elif view.action in ['update', 'partial_update', 'destroy']:
            possible_options = (
                obj.author == request.user,
                request.user.is_admin,
                request.user.is_moderator,
            )
            return any(possible_options)
        else:
            return False
