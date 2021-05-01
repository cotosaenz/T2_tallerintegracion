from rest_framework import serializers
from .models import Artist, Album, Track

class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Artist    
        fields=('id','name','age','albums','tracks','self_url')

class AlbumListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Album    
        fields=('id','artist_id','name','genre','artist','tracks','self_url')

class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Track    
        fields=('id','artist_id','album_id','name','duration','times_played','artist','album','self_url')