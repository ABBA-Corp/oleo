# Generated by Django 4.1 on 2023-02-20 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_recipe_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='rec_videos', verbose_name='Video'),
        ),
    ]
