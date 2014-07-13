from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    '''
    Basic permission to allow only owner to edit or delete an object.
    '''
    def has_permission(self, request, view, obj=None):
        # Edit and delete permission is allowed only to its owner.
        return obj is None or obj.user == request.user
        
    