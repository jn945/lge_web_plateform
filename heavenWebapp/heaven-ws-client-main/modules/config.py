import configparser
import json

from modules.common.utils.singletone import Singletone


def is_number(value: str):
    try:
        judge = str(float(value))
        return False if (judge == "nan" or judge == "inf" or judge == "-inf") else True
    except ValueError:
        return False


def str_to_number(value: str):
    if is_number(value):
        try:
            return int(value)
        except ValueError:
            return float(value)
    return value


class Config(Singletone):
    """Config class

    Attributes:
        self.__config (dict): config.ini 파일을 불러와 dict 형식으로 저장
    """

    @property
    def config(self) -> dict:
        """The config property."""
        return self.__config

    def __init__(self, config_file_path: str) -> None:
        self.__configparser = configparser.ConfigParser()
        self.__configparser.read(config_file_path)
        self.__config = dict()
        self._str_to_list()

    def _str_to_list(self) -> None:
        """형태에 맞는 문자열 type 변환

        Returns:
            list: list (str) -> list (list)
            int: int (str) -> int (int)
        """
        for section in self.__configparser.sections():
            if not (section in self.__config.keys()):
                self.__config[section] = {}
            for key in self.__configparser[section].keys():
                if not (key in self.__config[section].keys()):
                    self.__config[section][key] = {}

                # 문자열이 리스트 형태일 경우, 리스트로 변환
                # 숫자 데이터인 경우, 숫자로 변환
                if (self.__configparser[section][key][0] == "[") and (
                    self.__configparser[section][key][-1] == "]"
                ):
                    list_value = json.loads(self.__configparser[section][key])
                    for item in list_value:
                        item = str_to_number(item)
                    self.__config[section][key] = list_value
                else:
                    self.__config[section][key] = str_to_number(
                        self.__configparser[section][key]
                    )
