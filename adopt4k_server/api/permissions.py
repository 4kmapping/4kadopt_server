from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    '''
    Basic permission to allow only owner to edit or delete an object.
    '''
    def has_permission(self, request, view, obj=None):
        # Edit and delete permission is allowed only to its owner.
        return obj is None or obj.user == request.user
        
       
class AllReadCreateOnlyOwnerUpdateDelete(permissions.BasePermission):
    '''
    Allows All to read and create, but only owner to update and delete.
    '''
    def has_object_permission(self, request, view, obj=None):
        # Edit and delete permission is allowed only to its owner.
        method = request.method
        if method == 'GET' or method == 'POST':
            #return False
            #return obj.user == request.user
            return True
        elif method == 'PUT' or method == 'PATCH' or method == 'DELETE':
            if request.user.is_staff: # system user has full power
                return True    
            return obj is None or obj.user == request.user
    
    