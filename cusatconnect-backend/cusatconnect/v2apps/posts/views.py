from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer, CommentSerializer, LikeGetSerializer, LikeSerializer
from .models import Post, Activity


class PostImageView(APIView):

    permission_classes = ()
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = PostSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(CreateAPIView):

    permission_classes = ()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentView(CreateAPIView):

    permission_classes = ()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeAddView(CreateAPIView):

    permission_classes = ()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        object_id = serializer.validated_data['object_id']
        content_type = serializer.validated_data['content_type']
        new_like, created = Activity.objects.get_or_create(
                                user=user, object_id=object_id, content_type=content_type,
                            )
        new_like.activity_type = serializer.validated_data['activity_type']
        new_like.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeGetView(RetrieveAPIView):

    permission_classes = ()
    serializer_class = LikeGetSerializer

    def get_object(self):
        queryset = Post.objects.get(pk=self.kwargs.get('pk'))
        return queryset
