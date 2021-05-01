from django.db import models

# Create your models here.
class Artist(models.Model):
    id=models.CharField(default=None, max_length=100, primary_key=True)
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    albums=models.CharField(default=None, max_length=500)
    tracks=models.CharField(default=None, max_length=500)
    self_url=models.CharField(default=None, max_length=500)

class Album(models.Model):
    id=models.CharField(default=None, max_length=100, primary_key=True)
    name=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    artist_id=models.ForeignKey(Artist, on_delete=models.CASCADE)
    artist=models.CharField(default=None, max_length=500)
    tracks=models.CharField(default=None, max_length=500)
    self_url=models.CharField(default=None, max_length=500)


class Track(models.Model):
    id=models.CharField(default=None, max_length=100, primary_key=True)
    name=models.CharField(max_length=100)
    duration=models.FloatField()
    times_played=models.IntegerField(default=0)
    artist_id=models.ForeignKey(Artist, on_delete=models.CASCADE)
    album_id=models.ForeignKey(Album, on_delete=models.CASCADE)
    artist=models.CharField(default=None, max_length=500)
    album=models.CharField(default=None, max_length=500)
    self_url=models.CharField(default=None, max_length=500)

    
