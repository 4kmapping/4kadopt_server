from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers import UserSerializer, GroupSerializer
from api.serializers import OZFeatureSerializer, AdoptionSerializer
from api.models import OZFeature, Adoption
from permissions import IsOwner



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
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        '''
        If a user is admin, whole list is shown. If a user is not admin,
        the user's own info will be shown only. 
        '''
        if self.request.user.is_staff:
            qset = Adoption.objects.all()
        else:
            qset = Adoption.objects.filter(user=self.request.user)     
        return qset 
    
           
    
    
    
    
    
    