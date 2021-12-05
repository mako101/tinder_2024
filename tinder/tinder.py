import logging
from typing import Tuple

from tinder.entities.match import Match
from tinder.entities.message import Message
from tinder.entities.self_user import SelfUser
from tinder.http import Http
from tinder.http import Request
from tinder.entities.user import UserProfile, LikePreview


class TinderClient:
    def __init__(self, auth_token: str):
        self._http = Http(auth_token)
        logging.getLogger().name = "tinder-py"
        logging.getLogger().setLevel(logging.DEBUG)

    def retrieve_like_previews(self) -> Tuple[LikePreview]:
        response = \
            self._http.make_request(Request(method='GET', route='/v2/fast-match/teasers')).json()
        return tuple(LikePreview(user['user']) for user in response['data']['results'])

    def retrieve_recommendations(self):
        route = "v2/recs/core"
        response = self._http.get(route).json()
        recs = set()
        for result in response["data"]["results"]:
            print(result)
            # recs.add(Recommendation(self._http, result))
        return tuple(recs)

    def retrieve_matches(self, count: int = 60, page_token: str = None) -> Tuple[Match, ...]:
        route = "/v2/matches?count={}".format(count)
        if page_token:
            route = route + "&page_token=" + page_token
        response = self._http.make_request(Request(method='GET', route=route)).json()
        matches = set()
        for match in response["data"]["matches"]:
            matches.add(Match(self._http, match))
        return tuple(matches)

    def retrieve_match(self, match_id: str) -> Match:
        route = "/v2/matches/" + match_id
        response = self._http.get(route).json()
        match = response["data"]
        return Match(self._http, match)

    def retrieve_matches_by_name(self, user_name: str) -> Tuple[Match, ...]:
        matches = self.retrieve_matches()
        result = set()
        for match in matches:
            if match.retrieve_user().name == user_name:
                result.add(match)
        return tuple(result)

    def retrieve_user(self, user_id: str) -> UserProfile:
        route = "/user/{}".format(user_id)
        response = self._http.get(route).json()
        return UserProfile(response["results"])

    def retrieve_message(self, message_id) -> Message:
        route = "/message/{}".format(message_id)
        response = self._http.get(route).json()
        return Message(self._http, response)

    def retrieve_self_user(self) -> SelfUser:
        route = "/profile"
        response = self._http.get(route).json()
        return SelfUser(self._http, response)
