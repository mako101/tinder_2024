from typing import Tuple, Union

from tinder.entities.entity import Entity
from tinder.entities.message import Message
from tinder.entities.photo import MatchPhoto
from tinder.entities.socials import FacebookInfo
from tinder.entities.user import MatchedUser
from tinder.http import Http


class Match(Entity):
    """
    Represents a Tinder match.
    """
    __slots__ = [
        'closed',
        'facebook',
        'created_date',
        'dead',
        'last_activity_date',
        'message_history',
        'pending',
        'is_super_like',
        'is_boost_match',
        'is_super_boost_match',
        'is_experiences_match',
        'is_fast_match',
        'is_opener',
        'following',
        'following_moments',
        'matched_user',
        'liked_content',
        'seen',
        'last_seen_message_id'
    ]

    def __init__(self, match: dict, http: Http):
        """
        Creates a new match object

        :param match: the dictionary to construct the match from
        """
        super().__init__(match, http)
        self.closed: bool = match['closed']
        self.facebook: FacebookInfo = FacebookInfo(match)
        self.created_date: str = match['created_date']
        self.dead: bool = match['dead']
        self.last_activity_date: str = match['last_activity_date']
        self.message_history: MessageHistory = MessageHistory()
        self.pending: bool = match['pending']
        self.is_super_like: bool = match['is_super_like']
        self.is_boost_match: bool = match['is_boost_match']
        self.is_super_boost_match: bool = match['is_super_boost_match']
        self.is_experiences_match: bool = match['is_experiences_match']
        self.is_fast_match: bool = match['is_fast_match']
        self.is_opener: bool = match['is_opener']
        """`true` if the self user liked first"""
        self.following: bool = match['following']
        self.following_moments: bool = match['following_moments']
        self.matched_user: MatchedUser = MatchedUser(match['person'])
        if 'liked_content' in match:
            liked_content = match['liked_content']
            # if is_opener is true the self user liked first. Thus, the other user "closed" aka
            # completed the match. If is_opener is false the other use was the match "opener"
            if self.is_opener:
                self.liked_content: MatchPhoto = (liked_content['by_closer']['photo'])
            else:
                self.liked_content: MatchPhoto = (liked_content['by_opener']['photo'])
        self.seen: bool = False
        self.last_seen_message_id: str = ''
        if 'seen' in match:
            self.seen: bool = match['seen']['match_seen']
            if 'last_seen_message_id' in match['seen']:
                self.last_seen_message_id: str = match['seen']['last_seen_message_id']

    def send_message(self, message: Union[str, Message]) -> Message:

        pass

    def delete_match(self):
        pass


class MessageHistory:
    """
    Access point to the message history of a Match.

    By default, this class will cache the first 60 messages. `load_all_messages` to request
    all messages sent from the Tinder API.

    Message order is always in recent to past order.
    For example, a message at index 0 is more recent than a message at index 1.
    """

    def __init__(self, http: Http):
        self.http: Http = http
        pass

    def get_message_by_id(self) -> Message:
        """
        Gets a message by its id. Will request the message from the API if the message is not
        present in the cache.

        :return: a message by its id
        """
        pass

    def get_messages(self) -> Tuple[Message]:
        """
        Gets all messages inside the cache.

        :return: all messages inside the cache
        """
        pass

    def get_messages_before(self, message_id: str) -> Tuple[Message]:
        """
        Gets all messages sent before the provided message id.

        This will only consider cached messages.

        :return: all messages sent before the provided message id
        """
        pass

    def get_messages_after(self, message_id: str) -> Tuple[Message]:
        """
        Gets all messages sent after the provided message id.

        This will only consider cached messages.

        :return: all messages sent after the provided message id
        """
        pass

    def load_all_messages(self, count: int = 60, page_token: str = None) -> Tuple[Message]:
        """
        Requests all messages from the Tinder API.

        :param count: the messages to load per request
        :param page_token: token of the next page
        :return: all messages of a match
        """
        pass

    def size(self):
        """
        Gets the size of the cache.

        :return: the size of the cache
        """
        pass
