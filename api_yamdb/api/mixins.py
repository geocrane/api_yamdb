from rest_framework import mixins
from rest_framework import viewsets


class CreateDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                          mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass
