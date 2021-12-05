from datetime import datetime
from enum import Enum

from tinder.entities.entity import Entity
from tinder.entities.socials import SpotifySongAttachment


class Message(Entity):
    __slots__ = [
        'match_id',
        'sent_date',
        'content',
        'author_id',
        'recipient_id',
        'attachment_type',
        'attachment'
    ]

    def __init__(self, message: dict):
        super().__init__(message)
        self.match_id: str = message['match_id']
        self.sent_date: datetime = datetime.fromtimestamp(message['timestamp'])
        self.content: str = message['message']
        # TODO add objects instead of ids
        self.author_id: str = message['from']
        self.recipient_id: str = message['to']
        self.attachment_type: AttachmentType = AttachmentType.NONE

        if 'type' in message:
            self.attachment_type = AttachmentType(message['type'])

        if self.attachment_type == AttachmentType.GIF:
            self.attachment = GIFAttachment(message)
        elif self.attachment_type == AttachmentType.CONTACT_CARD:
            self.attachment = ContactCardAttachment(message)
        elif self.attachment_type == AttachmentType.SONG:
            self.attachment = SongAttachment(message)
        elif self.attachment_type == AttachmentType.STICKER:
            self.attachment = StickerAttachment(message)


class AttachmentType(Enum):
    GIF = 'gif',
    CONTACT_CARD = 'contact_card',
    SONG = 'song'
    STICKER = 'sticker'
    NONE = 'N/A'


class Attachment:
    __slots__ = ['type']

    def __init__(self, attachment_type: AttachmentType):
        self.type: AttachmentType = attachment_type


class GIFAttachment(Attachment):
    __slots__ = ['url']

    def __init__(self, message: dict):
        super().__init__(AttachmentType.GIF)
        self.url: str = message['fixed_height']


class ContactCardAttachment(Attachment):
    __slots__ = ['contact_id', 'contact_type', 'url']

    def __init__(self, message: dict):
        super().__init__(AttachmentType.CONTACT_CARD)
        contact_card = message['contact_card']
        self.contact_id: str = contact_card['contact_id']
        self.contact_type: str = contact_card['contact_type']
        self.url: str = contact_card['deeplink']


class SongAttachment(Attachment):
    __slots__ = ['song']

    def __init__(self, message: dict):
        super().__init__(AttachmentType.SONG)
        self.song: SpotifySongAttachment = SpotifySongAttachment(message['song'])


class StickerAttachment(Attachment):
    __slots__ = ['url']

    def __init__(self, message: dict):
        super().__init__(AttachmentType.STICKER)
        self.url: str = message['fixed_height']
