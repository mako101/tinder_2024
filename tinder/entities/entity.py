class Entity:
    __slots__ = ['entity_id']

    def __init__(self, entity: dict):
        if '_id' in entity:
            self.entity_id: str = entity['_id']
        elif 'id' in entity:
            self.entity_id: str = entity['id']
        else:
            raise TypeError('Not an entity!')
