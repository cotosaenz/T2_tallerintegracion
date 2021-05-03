from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Artist, Album, Track
from .serializers import ArtistListSerializer, AlbumListSerializer, TrackListSerializer
from base64 import b64encode

# Create your views here.
class ArtistListView(APIView):
    def get(self, request):
        lista = Artist.objects.all()
        serializer=ArtistListSerializer(lista, many=True)
        final = []
        for element in serializer.data:
            dic = element
            url = element['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            final.append(dic)
        return Response(final)

    def post(self, request, format=None):
        datos = list(request.data.keys())
        if len(datos) != 2:
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif datos[0]!='name' or datos[1]!='age':
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif type(request.data['name']) != str or type(request.data['age'])!= int:
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        string_name = request.data['name']
        key = b64encode(string_name.encode()).decode('utf-8')
        if len(key)>22:
            key = key[:22]
        data={
            'id':key,
            'name':string_name,
            'age':request.data['age'],
            'albums':'https://t2-tallerintegracion-sm.herokuapp.com/artists/'+key+'/albums',
            'tracks':'https://t2-tallerintegracion-sm.herokuapp.com/artists/'+key+'/tracks',
            'self_url':'https://t2-tallerintegracion-sm.herokuapp.com/artists/'+key,
        }
        serializer = ArtistListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            dic = serializer.data
            url = serializer.data['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            return Response(dic, status=status.HTTP_201_CREATED)
        elif status.HTTP_409_CONFLICT:
            artist = Artist.objects.get(id=key)
            serializer=ArtistListSerializer(artist, many=False)
            dic = serializer.data
            url = serializer.data['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            return Response(dic, status=status.HTTP_409_CONFLICT)
        
class ArtistDetailView(APIView):
    def get(self, request, id):
        try:
            artist = Artist.objects.get(id=id)
            serializer=ArtistListSerializer(artist, many=False)
            dic = serializer.data
            url = serializer.data['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            return Response(dic)
        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            artist = Artist.objects.get(id=id)
            albums = Album.objects.filter(artist_id=id)
            tracks = Track.objects.filter(artist_id=id)
            for track in tracks:
                track.delete()
            for album in albums:
                album.delete()
            artist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)

class ArtistAlbumsView(APIView):
    def get(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
            albums = Album.objects.filter(artist_id=artist_id)
            serializer=AlbumListSerializer(albums, many=True)
            final = []
            for element in serializer.data:
                dic = element
                url = element['self_url']
                dic['self'] = url
                dic.pop('self_url', None)
                final.append(dic)
            return Response(final)

        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)

    def post(self, request, artist_id):
        datos = list(request.data.keys())
        if len(datos) != 2:
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif datos[0]!='name' or datos[1]!='genre':
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif type(request.data['name']) != str or type(request.data['genre'])!= str:
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            artist = Artist.objects.get(id=artist_id)
            string_name = request.data['name']+artist_id
            key = b64encode(string_name.encode()).decode('utf-8')
            if len(key)>22:
                key = key[:22]
            data={
                'id':key,
                'name':string_name,
                'genre':request.data['genre'],
                'artist_id':artist_id,
                'artist':'https://t2-tallerintegracion-sm.herokuapp.com/artists/'+artist_id,
                'tracks':'https://t2-tallerintegracion-sm.herokuapp.com/albums/'+key+'/tracks',
                'self_url':'https://t2-tallerintegracion-sm.herokuapp.com/albums/'+key,
            }
            serializer = AlbumListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                dic = serializer.data
                url = serializer.data['self_url']
                dic['self'] = url
                dic.pop('self_url', None)
                return Response(dic, status=status.HTTP_201_CREATED)
            elif status.HTTP_409_CONFLICT:
                album = Album.objects.get(id=key)
                serializer=AlbumListSerializer(album, many=False)
                dic = serializer.data
                url = serializer.data['self_url']
                dic['self'] = url
                dic.pop('self_url', None)
                return Response(dic, status=status.HTTP_409_CONFLICT)
            
        except:
            return Response({'error':'artist_id not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, artist_id, format=None):
        try:
            artist = Artist.objects.get(id=artist_id)
            tracks = Track.objects.filter(artist_id=artist_id)
            for track in tracks:
                act = track.times_played+1
                data={"id":track.id, "artist_id":track.artist_id.id, "album_id":track.album_id.id,
                "name":track.name, "duration":track.duration, "times_played":act,
                "artist":track.artist, "album":track.album, "self_url":track.self_url}
                serializer = TrackListSerializer(track, data=data)
                if serializer.is_valid():
                    serializer.save()
            return Response(status.HTTP_200_OK)
        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)

class ArtistTracksView(APIView):
    def get(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
            tracks = Track.objects.filter(artist_id=artist_id)
            serializer=TrackListSerializer(tracks, many=True)
            final = []
            for element in serializer.data:
                dic = element
                url = element['self_url']
                dic['self'] = url
                dic.pop('self_url', None)
                dic.pop('artist_id', None)
                final.append(dic)
            return Response(final)

        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)
    
class AlbumListView(APIView):

    def get(self, request):
        lista = Album.objects.all()
        serializer=AlbumListSerializer(lista, many=True)
        final = []
        for element in serializer.data:
            dic = element
            url = element['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            final.append(dic)
        return Response(final)

class AlbumTracksView(APIView):
    def get(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)
            tracks = Track.objects.filter(album_id=album_id)
            serializer=TrackListSerializer(tracks, many=True)
            final = []
            for element in serializer.data:
                dic = element
                url = element['self_url']
                dic['self'] = url
                dic.pop('self_url', None)
                dic.pop('artist_id', None)
                final.append(dic)
            return Response(final)

        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)

    def post(self, request, album_id):
        datos = list(request.data.keys())
        if len(datos) != 2:
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif datos[0]!='name' or datos[1]!='duration':
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif type(request.data['name']) != str or type(request.data['duration'])!= float:
            return Response({'error':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            album = Album.objects.get(id=album_id)
            artist_id = album.artist_id.id
            string_name = request.data['name']+album_id
            key = b64encode(string_name.encode()).decode('utf-8')
            if len(key)>22:
                key = key[:22]
            data={
                'id':key,
                'name':string_name,
                'duration':request.data['duration'],
                'times_played':0,
                'artist_id':artist_id,
                'album_id':album_id,
                'artist':'https://t2-tallerintegracion-sm.herokuapp.com/artists/'+artist_id,
                'album':'https://t2-tallerintegracion-sm.herokuapp.com/albums/'+album_id,
                'self_url':'https://t2-tallerintegracion-sm.herokuapp.com/tracks/'+key,
            }
            serializer = TrackListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                dic = serializer.data
                url = serializer.data['self_url']
                dic['self'] = url
                dic.pop('self_url', None)
                dic.pop('artist_id', None)
                return Response(dic, status=status.HTTP_201_CREATED)
            elif status.HTTP_409_CONFLICT:
                track = Track.objects.get(id=key)
                serializer=TrackListSerializer(track, many=False)
                dic = serializer.data
                url = serializer.data['self_url']
                dic['self'] = url
                dic.pop('self_url', None)
                dic.pop('artist_id', None)
                return Response(dic, status=status.HTTP_409_CONFLICT)
            
        except:
            return Response({'error':'albumt_id not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)
            tracks = Track.objects.filter(album_id=album_id)
            for track in tracks:
                act = track.times_played+1
                data={"id":track.id, "artist_id":track.artist_id.id, "album_id":track.album_id.id,
                "name":track.name, "duration":track.duration, "times_played":act,
                "artist":track.artist, "album":track.album, "self_url":track.self_url}
                serializer = TrackListSerializer(track, data=data)
                if serializer.is_valid():
                    serializer.save()
            return Response(status.HTTP_200_OK)
        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)

class AlbumDetailView(APIView):
    def get(self, request, id):
        try:
            album = Album.objects.get(id=id)
            serializer=AlbumListSerializer(album, many=False)
            dic = serializer.data
            url = serializer.data['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            return Response(dic)
        except:
            return Response({'error':'album_id not found'}, status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        try:
            album= Album.objects.get(id=id)
            tracks = Track.objects.filter(album_id=id)
            for track in tracks:
                track.delete()
            album.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error':'album_id not found'}, status.HTTP_404_NOT_FOUND)

class TrackListView(APIView):

    def get(self, request):
        lista = Track.objects.all()
        serializer=TrackListSerializer(lista, many=True)
        final = []
        for element in serializer.data:
            dic = element
            url = element['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            dic.pop('artist_id', None)
            final.append(dic)
        return Response(final)

class TrackDetailView(APIView):
    def get(self, request, id):
        try:
            track = Track.objects.get(id=id)
            serializer=TrackListSerializer(track, many=False)
            dic = serializer.data
            url = serializer.data['self_url']
            dic['self'] = url
            dic.pop('self_url', None)
            dic.pop('artist_id', None)
            return Response(dic)
        except:
            return Response({'error':'track_id not found'}, status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            track = Track.objects.get(id=id)
            act = track.times_played+1
            data={
                'id':track.id,
                'artist_id':track.artist_id.id,
                'album_id':track.album_id.id,
                'name':track.name,
                'duration':track.duration,
                'times_played':act,
                'artist':track.artist,
                'album':track.album,
                'self_url':track.self_url,
            }
            serializer = TrackListSerializer(track, data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(status.HTTP_200_OK)
        except:
            return Response({'error':'artist_id not found'}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            track= Track.objects.get(id=id)
            track.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error':'track_id not found'}, status.HTTP_404_NOT_FOUND)
