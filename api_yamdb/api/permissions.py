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
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'create':
            allowed = (
                request.user.is_authenticated,
                request.user.is_admin,
                request.user.is_moderator,
            )
            return any(allowed)
        if request.user.is_authenticated:
            allowed = (
                obj.author == request.user,
                request.user.is_admin,
                request.user.is_moderator,
            )
            return any(allowed)
        return False

    # def has_permission(self, request, view):
    #     if view.action in ['list', 'retrieve']:
    #         return True
    #     elif view.action in ['create', 'update', 'partial_update', 'destroy']:
    #         if not request.user.is_authenticated:
    #             return False
    #         else:
    #             return True
    #     else:
    #         return False

    # def has_object_permission(self, request, view, obj):
    #     if view.action in ['list', 'retrieve']:
    #         return True
    #     elif view.action == 'create':
    #         allowed = (
    #             request.user.is_authenticated,
    #             request.user.is_admin,
    #             request.user.is_moderator,
    #         )
    #         return any(allowed)
    #     elif view.action in ['update', 'partial_update', 'destroy']:
    #         allowed = (
    #             obj.author == request.user,
    #             request.user.is_admin,
    #             request.user.is_moderator,
    #         )
    #         return any(allowed)
    #     else:
    #         return False
