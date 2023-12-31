# Generated by Django 4.2.6 on 2023-10-21 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_vlogs_cover_vlogs_tags_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'vlog')},
        ),
        migrations.AlterField(
            model_name='vlogs',
            name='tags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.tags'),
        ),
    ]
