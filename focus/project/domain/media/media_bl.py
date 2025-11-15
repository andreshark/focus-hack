from project.domain.media.media_dal import MediaDal
from project.utils.data_state import DataState

class MediaBl:
    @staticmethod
    def get_all_musics(user_id: int) -> DataState:
        return MediaDal.get_all_musics(user_id)

    @staticmethod
    def buy(user_id: int, music_id: int) -> DataState:
        return MediaDal.buy(user_id,music_id)