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
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseBadRequest


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
        obj.user = self.request.user
    
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
    

def ozstatus(request):
    if request.method == 'GET':
        status = 'none'
        if request.GET.get('wid', None):
            wid = request.GET['wid']
            
            # Check if wid is valid
            ozs_check = OZFeature.objects.filter(worldid=wid)
            if len(ozs_check) > 0:
                status = 'wrongId'
                return HttpResponse(status)   
            
            if request.GET.get('uid',None):
                uid = request.GET['uid']                
                ozs = Adoption.objects.filter(worldid=wid,user=uid)
                if len(ozs) > 0: # The current user already adopted oz.
                    status = 'owned'
                    return HttpResponse(status)
            
            ozs = Adoption.objects.filter(worldid=wid)    
            if len(ozs) > 0:
                status = 'taken'
        return HttpResponse(status)
    else:
        mssg = 'The HTTP method is not supported'
        return HttpResponseBadRequest(mssg)

    