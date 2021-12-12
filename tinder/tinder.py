import logging
from typing import Tuple, List

from tinder.entities.match import Match
from tinder.http import Http
from tinder.entities.user import UserProfile, LikePreview, Recommendation, SelfUser, LikedUser


class TinderClient:

    def __init__(self, auth_token: str):
        self._http = Http(auth_token)
        logging.getLogger().name = "tinder-py"
        logging.getLogger().setLevel(logging.DEBUG)

    def get_recommendations(self) -> Tuple[Recommendation]:
        response = self._http.make_request(method='GET', route='/recs/core').json()
        return tuple(Recommendation(r) for r in response['results'])

    def get_like_previews(self) -> Tuple[LikePreview]:
        response = \
            self._http.make_request(method='GET', route='/v2/fast-match/teasers').json()
        return tuple(LikePreview(user['user']) for user in response['data']['results'])

    def load_all_matches(self, page_token: str = None, count: int = 60) -> Tuple[Match]:
        route = f'/v2/matches?count={count}&messages=60'
        if page_token:
            route = f'{route}&page_token={page_token}'

        data = self._http.make_request(method='GET', route=route).json()['data']
        matches: List[Match] = list(Match(m) for m in data['matches'])
        if 'next_page_token' in data:
            matches.extend(self.load_all_matches(data['next_page_token'], count))

        return tuple(matches)

    def get_match(self, match_id: str) -> Match:
        response = self._http \
            .make_request(method='GET', route=f'/v2/matches/{match_id}?messages=60') \
            .json()
        return Match(response['data'])

    def get_user_profile(self, user_id: str) -> UserProfile:
        response = self._http.make_request(method='GET', route=f'/user/{user_id}').json()
        return UserProfile(response['data'])

    def get_self_user(self) -> SelfUser:
        response = self._http.make_request(method='GET', route='/profile').json()
        return SelfUser(response['data'])

    def get_liked_users(self) -> Tuple[LikedUser]:
        response = self._http.make_request(method='GET', route='/v2/my-likes').json()
        return tuple(LikedUser(user['user']) for user in response['data']['results'])
