# Generated by Django 4.0.2 on 2022-02-13 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
