from datetime import datetime
from enum import Enum
from typing import Tuple

from tinder.entities.entity import Entity
from tinder.entities.socials import InstagramInfo, FacebookInfo, SpotifyTrack, SpotifyTopArtist
from tinder.entities.photo import GenericPhoto, SizedImage, MatchPhoto, ProfilePhoto
from tinder.http import Http


class Badge:
    __slots__ = ['badge_type']

    def __init__(self, badge: dict):
        self.badge_type: str = badge['type']


class ChoiceSelection:
    __slots__ = ['id', 'name']

    def __init__(self, choice_selection: dict):
        self.id: str = choice_selection['id']
        self.name: str = choice_selection['name']


class Descriptor:
    __slots__ = ['id', 'name', 'prompt', 'icon_url', 'icon_urls', 'selection']

    def __init__(self, descriptor: dict):
        self.id: str = descriptor['id']
        self.name: str = descriptor['name']
        self.prompt: str = descriptor['prompt']
        self.icon_url: str = descriptor['icon_url']
        self.icon_urls: Tuple[SizedImage] = tuple(SizedImage(i) for i in descriptor['icon_urls'])
        self.selection: ChoiceSelection = ChoiceSelection(descriptor['choice_selection'])


class Gender(Enum):
    HIDDEN = -1
    MALE = 0
    FEMALE = 1


class Interest:
    __slots__ = ['id', 'name']

    def __init__(self, interest: dict):
        self.id: str = interest['id']
        self.name: str = interest['name']


class Job:
    __slots__ = ['company', 'title']

    def __init__(self, job: dict):
        if 'company' in job:
            self.company: str = job['company']['name']
        if 'title' in job:
            self.title: str = job['title']['name']


class Position:
    __slots__ = ['at', 'latitude', 'longitude']

    def __init__(self, position: dict):
        self.at: int = position['at']
        self.latitude: float = position['lat']
        self.longitude: float = position['lon']


class PositionInfo:
    __slots__ = ['country', 'cc', 'alpha3', 'timezone']

    def __init__(self, position_info):
        self.country: str = position_info['country']['name']
        self.cc: str = position_info['country']['cc']
        self.alpha3: str = position_info['country']['alpha3']
        self.timezone: str = position_info['timezone']


class School:
    __slots__ = ['name', 'metadata_id']

    def __init__(self, school: dict):
        self.name: str = school['name']
        if 'metadata_id' in school:
            self.metadata_id: str = school['metadata_id']


class Teaser:
    __slots__ = ['type', 'value']

    def __init__(self, teaser: dict):
        self.type: str = teaser['type']
        self.value: str = teaser['string']


class GenericUser(Entity):
    __slots__ = ['bio', 'birth_date', 'name', 'gender', 'badges', 'photos']

    def __init__(self, user: dict, http: Http):
        super().__init__(user, http)
        self.bio: str = ''
        if 'bio' in user:
            self.bio: str = user['bio']
        self.birth_date: str = user['birth_date']
        self.name: str = user['name']
        self.gender: Gender = Gender(user['gender'])
        self.badges: Tuple[Badge] = tuple()
        if 'badges' in user:
            self.badges: Tuple[Badge] = tuple(Badge(b) for b in user['badges'])
        self.photos: Tuple[GenericPhoto] = tuple(GenericPhoto(p, http) for p in user['photos'])

    def get_user_profile(self):
        pass

    def report(self):
        pass


class SelfUser(GenericUser):
    __slots__ = [
        'age_filter_min',
        'age_filter_max',
        'create_date',
        'distance_filter',
        'gender_filter',
        'email',
        'instagram',
        'interested_in',
        'job',
        'photo_optimizer_enabled',
        'last_online',
        'position',
        'position_info',
        'school',
        'show_gender_on_profile',
        'can_create_squad'
    ]

    def __init__(self, user: dict):
        super().__init__(user)
        self.photos: Tuple[ProfilePhoto] = tuple(ProfilePhoto(p) for p in user['photos'])
        self.age_filter_min: int = user['age_filter_min']
        self.age_filter_max: int = user['age_filter_max']
        self.create_date: int = user['create_date']
        self.distance_filter: int = user['distance_filter']
        self.gender_filter: Gender = Gender(user['gender_filter'])
        self.email = user['email']
        if 'instagram' in user:
            self.instagram = InstagramInfo(user['instagram'])
        self.interested_in: Tuple[Gender, ...] = tuple(Gender(g) for g in user['interested_in'])
        if 'jobs' in user:
            self.job: Job = Job(user['jobs'])
        self.photo_optimizer_enabled: bool = user['photo_optimizer_enabled']
        self.last_online: str = user['ping_time']
        self.position: Position = Position(user['pos'])
        self.position_info: PositionInfo = PositionInfo(user['pos_info'])
        if 'schools' in user:
            self.school: School = School(user['schools'][0])
        self.show_gender_on_profile: bool = user['show_gender_on_profile']
        self.can_create_squad: bool = user['can_create_squad']


class MatchedUser(GenericUser):
    __slots__ = [
        'birth_date_info',
        'last_online',
        'hide_age',
        'hide_distance',
        'is_travelling',
        'facebook'
    ]

    def __init__(self, user: dict):
        super().__init__(user)
        self.photos: Tuple[MatchPhoto] = tuple(MatchPhoto(p) for p in user['photos'])
        self.last_online: str = user['ping_time']
        self.hide_age: bool = False
        if 'hide_age' in user:
            self.hide_age: bool = user['hide_age']
        self.hide_distance: bool = False
        if 'hide_distance' in user:
            self.hide_distance: bool = user['hide_distance']
        self.is_travelling: bool = False
        if 'is_travelling' in user:
            self.is_travelling: bool = user['is_travelling']
        self.facebook: FacebookInfo = FacebookInfo(user)


class SwipeableUser(GenericUser):
    __slots__ = [
        'job',
        'school',
        'city',
        '_distance',
        's_number',
        'teasers',
        'facebook',
        'interests',
        'descriptors',
        'show_gender_on_profile',
        'top_artists',
        'theme_track'
    ]

    def __init__(self, user: dict, http: Http):
        super().__init__(user, http)
        self.job: Job = Job(user['jobs'])
        if len(user['schools']) > 0:
            self.school: School = School(user['schools'][0])
        if 'city' in user:
            self.city: str = user['city']['name']
        self._distance: int = user['distance_mi']
        self.s_number: int = user['s_number']
        self.teasers: Tuple[Teaser] = tuple(Teaser(t) for t in user['teasers'])
        self.facebook: FacebookInfo = FacebookInfo(user)
        if 'user_interests' in user:
            self.interests: Tuple[Interest] = \
                tuple(Interest(i) for i in user['user_interests']['selected_interests'])
        if 'selected_descriptors' in user:
            self.descriptors: Tuple[Descriptor] = \
                tuple(Descriptor(d) for d in user['selected_descriptors'])
        self.show_gender_on_profile: bool = True
        if 'show_gender_on_profile' in user:
            self.show_gender_on_profile: bool = user['show_gender_on_profile']
        if 'spotify_top_artists' in user:
            self.top_artists: Tuple[SpotifyTopArtist] = \
                tuple(SpotifyTopArtist(a) for a in user['spotify_top_artists'])
        if 'spotify_theme_track' in user:
            self.theme_track: SpotifyTrack = SpotifyTrack(user['spotify_theme_track'])

    def distance_mi(self) -> int:
        return self._distance

    def distance_km(self) -> float:
        return self._distance * 1.609344

    def like(self):
        pass

    def dislike(self):
        pass

    def superlike(self):
        pass


class LikedUser(SwipeableUser):
    __slots__ = ['content_hash', 'has_been_superliked', 'expire_time']

    def __init__(self, user: dict, http: Http):
        super().__init__(user, http)
        self.content_hash: str = user['content_hash']
        self.has_been_superliked: str = user['has_been_superliked']
        self.expire_time: datetime = datetime.fromtimestamp(user['expire_time'] / 1000)


class UserProfile(SwipeableUser):
    __slots__ = [
        'sexual_orientations',
        'last_online',
        'birth_date_info',
        'is_tinder_u',
        'hide_age',
        'hide_distance',
        'is_travelling'
    ]

    def __init__(self, user: dict, http: Http):
        super().__init__(user, http)
        if 'sexual_orientations' in user:
            self.sexual_orientations: Tuple[str] =\
                tuple(str(s['name']) for s in user['sexual_orientations'])
        self.last_online: str = user['ping_time']
        self.birth_date_info: str = user['birth_date_info']
        self.is_tinder_u: bool = user['is_tinder_u']
        self.hide_age: bool = False
        if 'hide_age' in user:
            self.hide_age: bool = user['hide_age']
        self.hide_distance: bool = False
        if 'hide_distance' in user:
            self.hide_distance: bool = user['hide_distance']
        self.is_travelling: bool = False
        if 'is_travelling' in user:
            self.is_travelling: bool = user['is_travelling']


class Recommendation(SwipeableUser):
    __slots__ = ['group_matched', 'content_hash']

    def __init__(self, user: dict, http: Http):
        super().__init__(user, http)
        self.group_matched = user['group_matched']
        self.content_hash = user['content_hash']


class LikePreview(Entity):
    __slots__ = ['photos', 'recently_active']

    def __init__(self, user: dict, http: Http):
        super().__init__(user, http)
        self.recently_active: bool = False
        if 'recently_active' in user:
            self.recently_active: bool = user['recently_active']
