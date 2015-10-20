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
    upload_file = serializers.FileField()

    # FilePathField(path, match=None, recursive=False, allow_files=True,
    # allow_folders=False, required=None, **kwargs

    class Meta:
        model = Trajectory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    collections = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),
                                                      view_name='snippet-detail', many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'collections')
