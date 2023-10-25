# Generated by Django 4.2.6 on 2023-10-20 16:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documents', models.FileField(upload_to='uploads/documents/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('txt', 'pdf', 'doc', 'docx'))])),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/images/%Y/%m/%d/')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='uploads/videos/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vlogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
                ('documents', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.documents')),
                ('images', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.images')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('videos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.videos')),
            ],
            options={
                'ordering': ['-posted_date'],
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vlogs')),
            ],
            options={
                'ordering': ['-posted_date'],
            },
        ),
    ]
