from rest_framework import permissions

from . import models


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_superuser and
            request.user.is_authenticated
        )


class IsAdminPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsSubscribedPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        user = models.User.objects.filter(id=request.user.id).first()
        course = view.kwargs.get('id')
        subscription = models.Subscription.objects.filter(
            user=user, course=course
        ).exists()
        return request.user.is_authenticated and subscription
