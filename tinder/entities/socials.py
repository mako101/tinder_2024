from typing import Tuple


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
