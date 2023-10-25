from ecommerce_app.models import UserProfile
from rest_framework import permissions


class IsUserSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.user_details.role == UserProfile.RoleChoice.SELLER


class CanEditProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        user = request.user
        return user.user_details.role == UserProfile.RoleChoice.SELLER
