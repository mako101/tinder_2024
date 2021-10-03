from tinder.entities import entity, user
from tinder.http import Http


class Recommendation(entity.Entity):
    __slots__ = [

    ]

    def __init__(self, http: Http, recommendation: dict):
        user_dict = recommendation["user"]
        super().__init__(http, user_dict["_id"])

    def retrieve_user(self) -> user.User:
        route = "/user/" + self.entity_id
        response = self._http.get(route).json()
        return user.User(self._http, response)
