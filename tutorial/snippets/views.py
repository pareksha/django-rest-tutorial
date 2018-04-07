from snippets.models import Snippet
from snippets.serializer import SnippetSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from snippets.serializer import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from snippets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.renderers import StaticHTMLRenderer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
    })

@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly))
def snippet_list(request, format=None):
    if request.method == 'GET':
        serializer = SnippetSerializer(Snippet.objects.all(), many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly))
def snippet_detail(request, pk, format=None):
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def user_list(request, format=None):
    if request.method == 'GET':
        serializer = UserSerializer(User.objects.all(), many=True, context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
def user_detail(request, pk, format=None):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
@renderer_classes((StaticHTMLRenderer,))
def get_snippet_highlight(request, pk, format=None):
    snippet = get_object_or_404(Snippet, pk=pk)
    return Response(snippet.highlighted)
