'''
Created on 19.10.2015

@author: marscher
'''

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (MetaCollection, Collection, Trajectory, Setup)


class SetupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Setup


class MetaCollectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MetaCollection


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # the backend keeps track of this field
    cumulative_length = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = ('name',
                  'description',
                  'n_atoms',
                  'cumulative_length',
                  'setup',
                  'owner'
                  )


class TrajectorySerializer(serializers.HyperlinkedModelSerializer):
    # handled by backend
    owner = serializers.ReadOnlyField(source='owner.username')
    uri = serializers.ReadOnlyField()
    length = serializers.ReadOnlyField()
    #data = serializers.FileField()
#     data = serializers.SerializerMethodField('get_uri')
#     def get_uri(self, obj):
#         return str(obj.uri)

    class Meta:
        model = Trajectory
        fields = ('name',
                  'data',
                  'length',
                  'parent_traj',
                  'collection',
                  'uri',
                  'hash_sha512',
                  'created',
                  'owner',
                  )


#     def create(self,*a,**kw):
#         instance = super(TrajectorySerializer, self).create(*a, **kw)
#         instance.length=0
#         instance.save()
#         return instance
        """
        try:
            import mdtraj
            with mdtraj.open(instance.data)
"""

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username')
