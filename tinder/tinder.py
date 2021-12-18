import logging
from typing import Tuple, List

from tinder.entities.match import Match
from tinder.exceptions import Unauthorized, LoginException
from tinder.http import Http
from tinder.entities.user import UserProfile, LikePreview, Recommendation, SelfUser, LikedUser


class TinderClient:

    def __init__(self, auth_token: str, log_level: int = logging.INFO, ratelimit: int = 10):
        self._http = Http(auth_token, timeout_factor=ratelimit)
        self._self_user = None
        self._matches: dict = {}
        logging.getLogger().name = 'tinder-py'
        logging.getLogger().setLevel(log_level)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        try:
            self._self_user = self.get_self_user()
        except Unauthorized:
            pass
        if self._self_user is None:
            raise LoginException()

    def get_recommendations(self) -> Tuple[Recommendation]:
        response = self._http.make_request(method='GET', route='/recs/core').json()
        return tuple(Recommendation(r, self._http) for r in response['results'])

    def get_like_previews(self) -> Tuple[LikePreview]:
        response = \
            self._http.make_request(method='GET', route='/v2/fast-match/teasers').json()
        return tuple(LikePreview(user['user'], self._http) for user in response['data']['results'])

    def load_all_matches(self, page_token: str = None) -> Tuple[Match]:
        route = f'/v2/matches?count=60'
        if page_token:
            route = f'{route}&page_token={page_token}'

        data = self._http.make_request(method='GET', route=route).json()['data']
        matches: List[Match] = list(Match(m, self._http) for m in data['matches'])
        if 'next_page_token' in data:
            matches.extend(self.load_all_matches(data['next_page_token']))

        self._matches.clear()
        for match in matches:
            self._matches.update(key=match.id, value=match)
        return tuple(matches)

    def get_match(self, match_id: str) -> Match:
        if match_id in self._matches:
            return self._matches[match_id]
        else:
            response = self._http.make_request(method='GET', route=f'/v2/matches/{match_id}').json()
            match = Match(response['data'], self._http)
            self._matches[match.id] = match
            return match

    def get_user_profile(self, user_id: str) -> UserProfile:
        response = self._http.make_request(method='GET', route=f'/user/{user_id}').json()
        return UserProfile(response['results'], self._http)

    def get_self_user(self) -> SelfUser:
        if self._self_user is None:
            response = self._http.make_request(method='GET', route='/profile').json()
            return SelfUser(response, self._http)
        else:
            return self._self_user

    def get_liked_users(self) -> Tuple[LikedUser]:
        response = self._http.make_request(method='GET', route='/v2/my-likes').json()
        result = []
        for user in response['data']['results']:
            transformed = {}
            transformed.update(user.items())
            transformed.pop('type')
            transformed.pop('user')
            transformed.update(user['user'].items())
            result.append(transformed)
        return tuple(LikedUser(user, self._http) for user in result)
