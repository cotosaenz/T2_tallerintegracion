# Generated by Django 3.2 on 2021-04-30 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210430_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='artist_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.artist'),
        ),
        migrations.AddField(
            model_name='track',
            name='album_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.album'),
        ),
        migrations.AddField(
            model_name='track',
            name='artist_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.artist'),
        ),
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='track',
            name='album',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='track',
            name='artist',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
