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

from rest_framework import generics
from rest_framework import viewsets

from .permissions import IsOwnerOrReadOnly

## Users
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


##########################################################################
# Trajectories and setups


class TrajectoryViewSet(viewsets.ModelViewSet):
    queryset = Trajectory.objects.all()
    serializer_class = TrajectorySerializer


from rest_framework.parsers import MultiPartParser, FormParser
class TrajectoryDetails(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, FormParser,)
    queryset = Trajectory.objects.all()
    serializer_class = TrajectorySerializer

    def post(self, request, format=None):
        my_file = request.FILES['file_field_name']
        filename = '/tmp/myfile'
        with open(filename, 'wb+') as temp_file:
            for chunk in my_file.chunks():
                temp_file.write(chunk)

        #my_saved_file = open(filename) #there you go


class SetupViewSet(viewsets.ModelViewSet):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer


class SetupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer

##########################################################################
# Collections


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def perform_create(self, serializer):
        print "hiiiiiiiiiiiiiiiiiiiiii"
        serializer.save(owner=self.request.user)


class MetaCollectionViewSet(viewsets.ModelViewSet):
    queryset = MetaCollection.objects.all()
    serializer_class = MetaCollectionSerializer


class MetaCollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaCollection.objects.all()
    serializer_class = MetaCollectionSerializer

###############################################################################
