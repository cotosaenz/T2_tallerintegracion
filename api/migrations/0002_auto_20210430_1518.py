# Generated by Django 3.2 on 2021-04-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='album_id',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='artist_id',
        ),
        migrations.RemoveField(
            model_name='track',
            name='track_id',
        ),
        migrations.AddField(
            model_name='track',
            name='id',
            field=models.CharField(default=None, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='album',
            name='id',
            field=models.CharField(default=None, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='album',
            name='self_url',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='album',
            name='tracks',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='artist',
            name='albums',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='artist',
            name='id',
            field=models.CharField(default=None, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='artist',
            name='self_url',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='artist',
            name='tracks',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='track',
            name='self_url',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
