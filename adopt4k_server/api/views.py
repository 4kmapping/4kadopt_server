from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer
from api.serializers import OZFeatureSerializer, AdoptionSerializer
from api.models import OZFeature, Adoption


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    
class OZFeatureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows OZFeatures to be viewed or edited.
    """
    queryset = OZFeature.objects.all()
    serializer_class = OZFeatureSerializer
    
    
class AdoptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Adoption to be viewed or edited.
    """  
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer      
    
    
    
    
    
    