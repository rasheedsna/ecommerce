from rest_framework import permissions


class AuthorisedEditOnly(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        print(obj)
        if request.method not in self.edit_methods:
            return True

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        if obj.author == request.user:
            return True

        return False
