# Generated by Django 4.2.7 on 2024-01-28 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_post_reactions'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='post',
            name='unique likes',
        ),
    ]