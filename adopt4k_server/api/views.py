from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers import UserSerializer, GroupSerializer
from api.serializers import OZFeatureSerializer, AdoptionSerializer
from api.serializers import AdoptionSimpleSerializer, AdoptionWithUserSerializer
from api.models import OZFeature, Adoption
from permissions import IsOwner, AllReadCreateOnlyOwnerUpdateDelete
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

class FullViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, 
        mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    This ViewSet supports create, update, delete, list.
    '''    
    pass


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,]
     
    def get_queryset(self):
        '''
        If a user is admin, whole list is shown. If a user is not admin,
        the user's own info will be shown only. 
        '''
        if self.request.user.is_staff:
            qset = User.objects.all()
        else:
            qset = [User.objects.get(username=self.request.user.username)]     
        return qset



class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    
    
class OZFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows OZFeatures to be viewed or edited.
    """
    queryset = OZFeature.objects.all()
    serializer_class = OZFeatureSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = []    
    
    
    
class AdoptionViewSet(FullViewSet):
    """
    API endpoint that allows Adoption to be viewed or edited.
    """  
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer  
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, AllReadCreateOnlyOwnerUpdateDelete]
    
    def pre_save(self, obj):
        obj.user = request.user
    
    def get_queryset(self):
        '''
        If a user is admin, whole list is shown. If a user is not admin,
        the user's own info will be shown only. 
        '''
        # If a user is checking the availability of an omega zaone having wid
        wid = self.request.QUERY_PARAMS.get('wid', None)
        opt = self.request.QUERY_PARAMS.get('adopted',None)
        if wid:
            self.serializer_class = AdoptionSimpleSerializer
            return Adoption.objects.filter(worldid=wid)
        
        if opt and (opt == 'true' or opt == 'false') :
            self.serializer_class = AdoptionSimpleSerializer
            if opt == 'true':
                adopted = True
            else:
                adopted = False
            return Adoption.objects.filter(is_adopted=adopted)
            
        # User's privilege based Adoption list
        if self.request.user.is_staff:
            qset = Adoption.objects.all()
            self.serializer_class = AdoptionWithUserSerializer
        else:
            qset = Adoption.objects.filter(user=self.request.user)     
        return qset 
    

"""
class AdoptionStatusViewSet(viewsets.GenericViewSet):
    '''
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    '''
    queryset = Adoption.objects.all()
    lookup_field = 'worldid'
    serializer_class = AdoptionSerializer 
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [AllReadCreateOnlyOwnerUpdateDelete]
    permission_classes = []
    
    def create(self, request):
        wid = request.POST.get('worldid', None)
        if wid is None:
            return response({'status':'Failed to create.'})
        ozs = Adoption.objects.filter(worldid=wid)
        if len(ozs) > 0 :
            status = {'status':'Failed to create. The worldid already exists,'}
            return response(status)
        adoption = Adoption()
        adoption.worldid = wid
        adoption.is_adopted = request.POST.get('is_adopted', False)
        adoption.user = request.user
        adoption.targetyear = request.POST.get('is_adopted', 0)
        adoption.save()
        return response({'status':'Successfully created.'})

    def retrieve(self, request, worldid=None):
        queryset = Adoption.objects.all()
        adoption = get_object_or_404(queryset, worldid=worldid)
        serializer = AdoptionSimpleSerializer(adoption)
        return Response(serializer.data)

    def update(self, request, worldid=None):
        if worldid is None:
            return response({'status':'Failed to update.'})
        ozs = Adoption.objects.filter(worldid=worldid)
        if len(ozs) == 1 and (request.user.id == ozs[0].user_id):
            oz = ozs[0]
            oz.worldid = worldid
            oz.is_adopted = request.POST.get('is_adopted',False)
            oz.targetyear = request.POST.get('targetyear', 0)
            oz.save()
            return response({'status':'Successfully updated.'}) 
        return response({'status':'Failed to update.'})
            
    def partial_update(self, request, worldid=None):
        if worldid is None:
            return response({'status':'Failed to partial-update.'})
        ozs = Adoption.objects.filter(worldid=worldid)
        if len(ozs) == 1 and (request.user.id == ozs[0].user_id):
            oz = ozs[0]
            oz.worldid = worldid
            oz.is_adopted = request.POST.get('is_adopted',oz.is_adopted)
            oz.targetyear = request.POST.get('targetyear',oz.targeryear)
            oz.save()
            return response({'status':'Successfully updated.'})  
        return response({'status':'Failed to partial-update.'}) 

    def destroy(self, request, worldid=None):
        if worldid is None:
            return response({'status':'Failed to delete.'})
        ozs = Adoption.objects.filter(worldid=worldid)
        if len(ozs) == 1 and (request.user.id == ozs[0].user_id):
            ozs[0].delete()
            return response({'status':'Successfully deleted.'})  
        return response({'status':'Failed to delete.'}) 
"""            
    
    
    
    
    
    