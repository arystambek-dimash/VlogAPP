from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models
from drf_spectacular.views import extend_schema


@extend_schema(
    summary="Get a list of vlogs",
    description="Retrieve a list of vlogs with optional filtering by title and tags.",
    tags=["Vlogs"],
    parameters=[
        {
            "name": "title",
            "in": "query",
            "required": False,
            "description": "Filter by title",
            "schema": {"type": "string"},
        },
        {
            "name": "tags",
            "in": "query",
            "required": False,
            "description": "Filter by tags",
            "schema": {"type": "string"},
        },
    ],
    responses={200: serializers.VlogsListSerializer(many=True)},
)
class VlogsGetView(generics.ListAPIView):
    queryset = models.Vlogs.objects.all()
    serializer_class = serializers.VlogsListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']


@extend_schema_view(
    create=extend_schema(summary="Create a vlog", description="Create a new vlog."),
    retrieve=extend_schema(summary="Get a vlog", description="Retrieve a specific vlog."),
    update=extend_schema(summary="Update a vlog", description="Update an existing vlog."),
    destroy=extend_schema(summary="Delete a vlog", description="Delete an existing vlog.")
)
@extend_schema(
    summary="Create a vlog",
    description="Retrieve a specific vlog.",
    tags=["Vlogs"],
    responses={200: serializers.VlogsSerializer()}
)
class VlogsPostView(generics.CreateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = serializers.VlogsSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Get a vlog",
    description="Retrieve a specific vlog.",
    tags=["Vlogs"],
    responses={200: serializers.VlogsSerializer()}
)
class VlogsView(generics.RetrieveAPIView):
    queryset = models.Vlogs.objects.all()
    serializer_class = serializers.VlogsSerializer


@extend_schema(
    summary="Update a vlog",
    description="Update an existing vlog.",
    tags=["Vlogs"],
    responses={200: serializers.VlogsSerializer()}
)
class VlogsUpdateView(generics.UpdateAPIView):
    parser_classes = (FormParser, MultiPartParser)
    queryset = models.Vlogs.objects.all()
    serializer_class = serializers.VlogsSerializer
    permission_classes = [IsAdminUser]

    allowed_methods = ['PATCH']


@extend_schema(
    summary="Delete a vlog",
    description="Delete an existing vlog.",
    tags=["Vlogs"],
    responses={204: None}
)
class VlogsDeleteView(generics.DestroyAPIView):
    queryset = models.Vlogs.objects.all()
    serializer_class = serializers.VlogsSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    summary="The vlog image Update Delete",
    description="Retrieve a specific vlog.",
    tags=["Vlogs Medias"],
    responses={200: serializers.VlogsSerializer()}
)
class VlogImageUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Images.objects.all()
    serializer_class = serializers.ImagesSerializer
    permission_classes = [IsAdminUser]

    allowed_methods = ['PATCH', 'DELETE']

    def get_queryset(self):
        vlog_pk = self.kwargs.get('vlog_pk')
        return models.Images.objects.filter(vlog=vlog_pk)


@extend_schema(
    summary="The vlog video Update Delete",
    description="Retrieve a specific vlog.",
    tags=["Vlogs Medias"],
    responses={200: serializers.VlogsSerializer()}
)
class VlogVideoUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Videos.objects.all()
    serializer_class = serializers.VideosSerializer
    permission_classes = [IsAdminUser]
    allowed_methods = ['PATCH', 'DELETE']

    def get_queryset(self):
        vlog_pk = self.kwargs.get('vlog_pk')
        return models.Videos.objects.filter(vlog=vlog_pk)


@extend_schema(
    summary="The vlog document Update Delete",
    description="Retrieve a specific vlog.",
    tags=["Vlogs Medias"],
    responses={200: serializers.VlogsSerializer()}
)
class VlogDocumentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Documents.objects.all()
    serializer_class = serializers.VideosSerializer
    permission_classes = [IsAdminUser]
    allowed_methods = ['PATCH', 'DELETE']

    def get_queryset(self):
        vlog_pk = self.kwargs.get('vlog_pk')
        return models.Documents.objects.filter(vlog=vlog_pk)


@extend_schema(
    summary="Create a comment",
    description="Create a new comment on a vlog.",
    tags=["Comments"],
    request=serializers.CommentsSerializer(),
    responses={200: serializers.CommentsSerializer()}
)
class CommentsPostView(generics.CreateAPIView):
    queryset = models.Comments.objects.all()
    serializer_class = serializers.CommentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        vlog = get_object_or_404(models.Vlogs, pk=self.kwargs.get("pk"))
        serializer.save(user=self.request.user, vlog=vlog)


@extend_schema(
    summary="Update a comment",
    description="Update an existing comment on a vlog.",
    tags=["Comments"],
    request=serializers.CommentsSerializer(),
    responses={200: serializers.CommentsSerializer()}
)
class CommentsUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.CommentsSerializer
    allowed_methods = ['PATCH']

    def get_queryset(self):
        vlog_id = self.kwargs['vlog_id']
        queryset = models.Comments.objects.filter(user=self.request.user, vlog__id=vlog_id)

        return queryset


@extend_schema(
    summary="Delete a comment",
    description="Delete an existing comment on a vlog.",
    tags=["Comments"],
    responses={204: None}
)
class CommentsDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.CommentsSerializer

    def get_queryset(self):
        vlog_id = self.kwargs['vlog_id']
        queryset = models.Comments.objects.filter(user=self.request.user, vlog__id=vlog_id)

        return queryset


@extend_schema(
    summary="Like a vlog",
    description="Like a vlog if not already liked, or do nothing if already liked.",
    tags=["Vlog Likes"],
    request=serializers.LikeSerializer(),
    responses={200: serializers.LikeSerializer()}
)
class LikeVlogView(generics.CreateAPIView):
    serializer_class = serializers.LikeSerializer

    def create(self, request, *args, **kwargs):
        vlog_id = self.kwargs.get('vlog_id')
        vlog = get_object_or_404(models.Vlogs, pk=vlog_id)
        existing_like = models.Like.objects.filter(user=self.request.user, vlog=vlog).first()

        if existing_like is not None:
            return Response({'detail': 'You have already liked this vlog.'}, status=status.HTTP_400_BAD_REQUEST)

        like = models.Like.objects.create(user=self.request.user, vlog=vlog)
        vlog.likes = models.Like.objects.filter(vlog=vlog).count()
        vlog.save()
        serializer = self.get_serializer(like)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(
    summary="Drop a like",
    description="Remove a like from a vlog if it exists.",
    tags=["Vlog Likes"],
    responses={204: None}
)
class DropLikeView(generics.UpdateAPIView):
    serializer_class = serializers.LikeSerializer
    allowed_methods = ['PUT']

    def update(self, request, *args, **kwargs):
        vlog_id = kwargs.get('vlog_id')
        vlog = get_object_or_404(models.Vlogs, pk=vlog_id)
        likes = models.Like.objects.filter(user=request.user, vlog=vlog)
        if likes.exists():
            likes.delete()
            vlog.likes = models.Like.objects.filter(vlog=vlog).count()
            vlog.save()

            return Response({'message': 'Like dropped successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You have not liked this vlog'}, status=status.HTTP_400_BAD_REQUEST)
