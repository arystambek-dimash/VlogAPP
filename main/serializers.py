from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import Images, Videos, Documents, Comments, Vlogs, Like


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
        read_only_fields = ["vlog"]

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'

    read_only_fields = ["vlog"]

    def update(self, instance, validated_data):
        instance.video = validated_data.get('video', instance.video)
        instance.save()
        return instance


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'
        read_only_fields = ["vlog"]

    def update(self, instance, validated_data):
        instance.document = validated_data.get('document', instance.document)
        instance.save()
        return instance


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'comment', 'user', 'vlog', 'posted_date', 'updated_date']
        read_only_fields = ['vlog', 'user', 'posted_date', 'updated_date']

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class VlogsSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    videos = VideosSerializer(many=True, read_only=True)
    documents = DocumentsSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )
    uploaded_videos = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True, required=False, validators=(
            [FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]
        )
    )
    uploaded_documents = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True, required=False, validators=(
            [FileExtensionValidator(allowed_extensions=('txt', 'pdf', 'doc', 'docx'), )]
        )
    )
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Vlogs
        fields = ['id', 'title', 'cover', 'content', 'description', 'posted_date', 'updated_date', 'likes',
                  'images', 'uploaded_images',
                  'videos', 'uploaded_videos',
                  'documents', 'uploaded_documents',
                  'comments',
                  'user']
        read_only_fields = ['likes', 'user', 'comments']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        uploaded_videos = validated_data.pop('uploaded_videos', [])
        uploaded_documents = validated_data.pop('uploaded_documents', [])
        vlog = Vlogs.objects.create(**validated_data)

        for image_data in uploaded_images:
            Images.objects.create(vlog=vlog, image=image_data)

        for video_data in uploaded_videos:
            Videos.objects.create(vlog=vlog, video=video_data)

        for document_data in uploaded_documents:
            Documents.objects.create(vlog=vlog, document=document_data)

        return vlog

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.cover = validated_data.get("cover", instance.cover)
        instance.content = validated_data.get("content", instance.content)
        instance.description = validated_data.get("description", instance.description)
        instance.updated_date = validated_data.get("updated_date", instance.updated_date)

        instance.save()
        return instance


class VlogsListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='tag', read_only=True)
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Vlogs
        fields = ["id", "title", "cover", "content", "description", "likes", "tags", "posted_date", "updated_date",
                  "user"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ["user", "vlog"]
