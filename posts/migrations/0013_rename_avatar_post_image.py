# Generated by Django 4.0.2 on 2022-02-28 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_remove_post_image_post_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='avatar',
            new_name='image',
        ),
    ]
