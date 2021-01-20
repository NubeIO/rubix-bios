import os
from flask import Flask


class AppSetting:
    PORT = 1514
    DATA_DIR_ENV = 'RUBIX_SERVICE_DATA'
    ARTIFACT_DIR_ENV = 'ARTIFACT_DIR'
    GLOBAL_DATA_DIR_ENV = 'GLOBAL_DATA'
    FLASK_KEY: str = 'APP_SETTING'

    default_global_dir: str = 'out'
    default_data_dir: str = 'rubix-bios'
    default_artifact_dir: str = 'apps'

    def __init__(self, **kwargs):
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), self.default_global_dir, 0o777)
        self.__data_dir = self.__compute_dir(kwargs.get('data_dir'),
                                             os.path.join(self.global_dir, self.default_data_dir))
        self.__artifact_dir = self.__compute_dir(kwargs.get('artifact_dir'),
                                                 os.path.join(self.data_dir, self.default_artifact_dir))
        self.__download_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'download'))
        self.__install_dir = self.__compute_dir('', os.path.join(self.__artifact_dir, 'install'))
        self.__prod = kwargs.get('prod') or False
        self.__device_type = kwargs.get('device_type')

    @property
    def global_dir(self):
        return self.__global_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def artifact_dir(self) -> str:
        return self.__artifact_dir

    @property
    def download_dir(self) -> str:
        return self.__download_dir

    @property
    def install_dir(self) -> str:
        return self.__install_dir

    @property
    def prod(self) -> bool:
        return self.__prod

    @property
    def device_type(self) -> str:
        return self.__device_type

    def init_app(self, app: Flask):
        app.config[AppSetting.FLASK_KEY] = self
        return self

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d
