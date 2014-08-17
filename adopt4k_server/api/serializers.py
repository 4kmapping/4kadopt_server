from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import OZFeature, Adoption

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','url', 'username', 'first_name','last_name', 'is_staff', 
            'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
        
class OZFeatureSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta:
        model = OZFeature

        # full list
        # fields = ('url','worldid','zonename', 'world_type','cntyid','cntyname',

        # condensed list for performance
        fields = ('worldid','polygons', 'cntyid')
        
class AdoptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Adoption
        #fields = ('url','worldid','targetyear','user','update','is_adopted')
        fields = ('url','worldid','targetyear','update','is_adopted', 
            'oz_zone_name', 'oz_country_name', 'user_display_name' )        

class AdoptionWithUserSerializer(serializers.HyperlinkedModelSerializer):
    # FOR ADMIN USER
    class Meta:
        model = Adoption
        fields = ('url','worldid','targetyear','user','update','is_adopted',
            'oz_zone_name', 'oz_country_name', 'user_display_name')
        
             
class AdoptionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ('worldid','targetyear','is_adopted', 'user')              