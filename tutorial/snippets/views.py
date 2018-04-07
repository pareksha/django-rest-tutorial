from rest_framework import viewsets
from django.contrib.auth.models import User
from snippets.serializer import UserSerializer, SnippetSerializer
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework import renderers
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
