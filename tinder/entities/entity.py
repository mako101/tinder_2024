from tinder.http import Http


class Entity:
    __slots__ = ['http', 'entity_id']

    def __init__(self, entity: dict, http: Http):
        self.http = http
        if '_id' in entity:
            self.entity_id: str = entity['_id']
        elif 'id' in entity:
            self.entity_id: str = entity['id']
        else:
            raise TypeError('Not an entity!')
