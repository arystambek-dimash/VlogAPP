from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db import models


class Images(models.Model):
    image = models.ImageField(upload_to="uploads/images/%Y/%m/%d/")
    vlog = models.ForeignKey('Vlogs', on_delete=models.CASCADE, related_name='images', null=True)


class Videos(models.Model):
    video = models.FileField(upload_to="uploads/videos/%Y/%m/%d/", validators=(
        [FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]
    ))
    vlog = models.ForeignKey('Vlogs', on_delete=models.CASCADE, related_name='videos', null=True)


class Documents(models.Model):
    document = models.FileField(upload_to="uploads/documents/%Y/%m/%d/", validators=(
        [FileExtensionValidator(allowed_extensions=('txt', 'pdf', 'doc', 'docx'), )]
    ))
    vlog = models.ForeignKey('Vlogs', on_delete=models.CASCADE, related_name='documents', null=True)


class Comments(models.Model):
    comment = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vlog = models.ForeignKey('Vlogs', on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return self.comment[:20]


class Vlogs(models.Model):
    title = models.CharField(max_length=100, null=False)
    cover = models.ImageField(upload_to="uploads/images/%Y/%m/%d/", null=True)
    content = models.CharField(max_length=255, null=True)
    description = models.TextField(null=False)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-posted_date"]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vlog = models.ForeignKey(Vlogs, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vlog')
