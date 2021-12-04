from typing import Tuple

from tinder.entities.entity import Entity


class FacialScope:
    __slots__ = ['width_pct', 'x_offset_pct', 'height_pct', 'y_offset_pct']

    def __init__(self, scope: dict):
        self.width_pct: float = scope['width_pct']
        self.x_offset_pct: float = scope['width_pct']
        self.height_pct: float = scope['height_pct']
        self.y_offset_pct: float = scope['y_offset_pct']


class Face:
    __slots__ = ['algo', 'bounding_box_percentage']

    def __init__(self, face: dict):
        self.algo: FacialScope = FacialScope(face['algo'])
        self.bounding_box_percentage: float = face['bounding_box_percentage']


class CropInfo:
    __slots__ = ['processed_by_bullseye', 'user_customized', 'user', 'algo', 'faces']

    def __init__(self, crop_info: dict):
        self.processed_by_bullseye: bool = crop_info['processed_by_bullseye']
        self.user_customized: bool = crop_info['user_customized']

        self.user = None
        if 'user' in crop_info:
            self.user: FacialScope = FacialScope(crop_info['user'])

        self.algo = None
        if 'algo' in crop_info:
            self.algo: FacialScope = FacialScope(crop_info['algo'])

        if 'faces' in crop_info:
            self.faces: Tuple[Face] = tuple(Face(algo) for algo in crop_info['faces'])

    def has_faces(self) -> bool:
        return len(self.faces) > 0


class SizedImage:
    __slots__ = ['height', 'width', 'url', 'quality']

    def __init__(self, sized_image: dict):
        self.height: int = sized_image['height']
        self.width: int = sized_image['width']
        self.url: str = sized_image['url']

        self.quality = None
        if 'quality' in sized_image:
            self.quality: str = sized_image['quality']

    def is_descriptor_image(self) -> bool:
        return self.quality is not None


class Hash:
    __slots__ = ['version', 'value']

    def __init__(self, hash_algo: dict):
        self.version: str = hash_algo['version']
        self.value: str = hash_algo['value']


class GenericPhoto(Entity):
    __slots__ = ['crop_info', 'url', 'processedFiles', 'file_name', 'extension']

    def __init__(self, photo: dict):
        super().__init__(photo)
        self.crop_info: CropInfo = CropInfo(photo['crop_info'])
        self.url: str = photo['url']
        self.processedFiles: Tuple[SizedImage] = \
            tuple(SizedImage(i) for i in photo['processedFiles'])
        self.file_name: str = photo['fileName']
        self.extension: str = photo['extension']


class ProfilePhoto(GenericPhoto):
    __slots__ = [
        'assets',
        'type',
        'created_at',
        'updated_at',
        'fb_id',
        'webp_qf',
        'rank',
        'score',
        'win_count',
        'phash',
        'dhash'
    ]

    def __init__(self, photo: dict):
        super().__init__(photo)
        self.assets: dict = photo['assets']
        self.type: str = photo['type']
        self.created_at: str = photo['created_at']
        self.updated_at: str = photo['updated_at']
        self.fb_id: str = photo['fb_id']
        self.webp_qf: int = photo['webp_qf'][0]
        self.rank: int = photo['rank']
        self.score: float = photo['score']
        self.win_count: int = photo['win_count']
        self.phash: Hash = Hash(photo['phash'])
        self.dhash: Hash = Hash(photo['dhash'])


class UserPhoto(GenericPhoto):
    __slots__ = ['media_type']

    def __init__(self, photo: dict):
        super().__init__(photo)
        self.media_type: str = photo['media_type']


class MatchPhoto(GenericPhoto):
    __slots__ = ['assets', 'type', 'webp_qf', 'rank', 'score', 'win_count']

    def __init__(self, photo: dict):
        super().__init__(photo)
        self.assets: dict = photo['assets']
        self.type: str = photo['type']
        self.webp_qf: int = photo['webp_qf'][0]
        self.rank: int = photo['rank']
        self.score: float = photo['score']
        self.win_count: int = photo['win_count']
