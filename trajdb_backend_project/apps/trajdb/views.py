# models:
from .models import (MetaCollection,
                     Collection,
                     Trajectory,
                     Setup,
                     )
from django.contrib.auth.models import User

# serializers
from .serializers import (CollectionSerializer,
                          MetaCollectionSerializer,
                          TrajectorySerializer,
                          SetupSerializer,
                          UserSerializer
                          )

from rest_framework import generics, status
from rest_framework import viewsets

from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response


# helper class:
class ModelViewSet_withOwner(viewsets.ModelViewSet):
    # store the creator in the model
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Users


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


##########################################################################
# Trajectories and setups

class TrajectoryViewSet(viewsets.ModelViewSet):
    from rest_framework.parsers import MultiPartParser, FormParser
    queryset = Trajectory.objects.all()
    serializer_class = TrajectorySerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsOwnerOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TrajectoryDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trajectory.objects.all()
    serializer_class = TrajectorySerializer


class SetupViewSet(viewsets.ModelViewSet):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer


class SetupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer

##########################################################################
# Collections


class CollectionViewSet(ModelViewSet_withOwner):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class MetaCollectionViewSet(viewsets.ModelViewSet):
    queryset = MetaCollection.objects.all()
    serializer_class = MetaCollectionSerializer


class MetaCollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaCollection.objects.all()
    serializer_class = MetaCollectionSerializer

###############################################################################
