'''
Created on 19.10.2015

@author: marscher
'''

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (MetaCollection, Collection, Trajectory, Setup, Topology)


class TopologySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topology

    n_atoms = serializers.ReadOnlyField()
    n_residues = serializers.ReadOnlyField()
    n_chains = serializers.ReadOnlyField()

    unitcell_vectors = serializers.ReadOnlyField()
    unitcell_angles = serializers.ReadOnlyField()
    unitcell_volume = serializers.ReadOnlyField()


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
#         fields = ('name',
#                   'description',
#                   'n_atoms',
#                   'cumulative_length',
#                   'setup',
#                   'owner'
#                   )


class TrajectorySerializer(serializers.HyperlinkedModelSerializer):
    # handled by backend
    owner = serializers.ReadOnlyField(source='owner.username')
    uri = serializers.ReadOnlyField()
    length = serializers.ReadOnlyField()

    class Meta:
        model = Trajectory
        fields = ('data',
                  'length',
                  'parent_traj',
                  'collection',
                  'uri',
                  'hash_sha512',
                  'created',
                  'owner',
                  )


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username')
