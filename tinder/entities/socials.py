from typing import Tuple

from tinder.entities.entity import Entity
from tinder.entities.photo import SizedImage


class InstagramInfo:
    __slots__ = ['last_fetch_time', 'completed_initial_fetch', 'media_count', 'photos']

    def __init__(self, instagram: dict):
        self.last_fetch_time: str = instagram['last_fetch_time']
        self.completed_initial_fetch: bool = instagram['completed_initial_fetch']
        self.media_count: int = instagram['media_count']
        self.photos: Tuple[InstagramPhoto] = tuple(InstagramPhoto(p) for p in instagram['photos'])


class InstagramPhoto:
    __slots__ = ['image', 'thumbnail', 'ts']

    def __init__(self, photo: dict):
        self.image: str = photo['image']
        self.thumbnail: str = photo['thumbnail']
        self.ts: str = photo['ts']
        

class FacebookInfo:
    __slots__ = [
        'common_connections',
        'connection_count',
        'common_interests',
        'common_likes',
        'common_like_count',
        'common_friends',
        'common_friend_count'
    ]

    def __init__(self, facebook: dict):
        self.common_connections = facebook['common_connections']
        self.connection_count = facebook['connection_count']
        self.common_interests = facebook['common_interests']
        self.common_likes = facebook['common_likes']
        self.common_like_count = facebook['common_like_count']
        self.common_friends = facebook['common_friends']
        self.common_friend_count = facebook['common_friend_count']


class SpotifyEntity(Entity):
    __slots__ = ['name']

    def __init__(self, entity: dict):
        super().__init__(entity)
        self.name: str = entity['name']


class SpotifyAlbum(SpotifyEntity):
    __slots__ = ['images']

    def __init__(self, album: dict):
        super().__init__(album)
        self.images: Tuple[SizedImage] = tuple(SizedImage(i) for i in album['images'])


class GenericSpotifyTrack(SpotifyEntity):
    __slots__ = ['album', 'artists']

    def __init__(self, track: dict):
        super().__init__(track)
        self.album: SpotifyAlbum = SpotifyAlbum(track['album'])
        self.artists: Tuple[SpotifyEntity] = tuple(SpotifyEntity(a) for a in track['artists'])


class SpotifyTrack(GenericSpotifyTrack):
    __slots__ = ['url', 'uri']

    def __init__(self, track: dict):
        super().__init__(track)
        self.url: str = track['preview_url']
        self.url: str = track['uri']


class SongAttachment(GenericSpotifyTrack):
    __slots__ = ['url']

    def __init__(self, track: dict):
        super().__init__(track)
        self.url: str = track['url']


class SpotifyTopArtist(SpotifyEntity):

    def __init__(self, artist: dict):
        super().__init__(artist)
        self.selected: bool = artist['selected']
        self.top_track: SpotifyTrack = SpotifyTrack(artist['top_track'])
