# Generated by Django 4.2.7 on 2024-01-28 21:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_alter_post_unique_together_post_unique_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reactions',
            field=models.ManyToManyField(related_name='user_reactions', to=settings.AUTH_USER_MODEL),
        ),
    ]