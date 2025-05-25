from rest_framework.permissions import BasePermission

from accounts.models import CustomUser


class IsAdminPermission(BasePermission):
    """
    Custom permission to check if the user is an admin.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.ADMIN


class IsPublisherPermission(BasePermission):
    """
    Custom permission to check if the user is a publisher.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.PUBLISHER

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
