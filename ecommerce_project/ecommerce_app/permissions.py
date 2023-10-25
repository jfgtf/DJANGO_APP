from ecommerce_app.models import UserProfile
from rest_framework import permissions

roles = UserProfile.RoleChoice


class IsUserSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.user_details.role == roles.SELLER


class CanEditProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        user = request.user
        return user.user_details.role == roles.SELLER


class CanPlaceOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == "POST":
            return user.user_details.role == roles.CLIENT

        return user.user_details.role == roles.SELLER
