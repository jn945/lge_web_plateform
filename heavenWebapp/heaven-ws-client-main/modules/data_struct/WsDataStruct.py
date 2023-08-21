import datetime
import json
import logging
from dataclasses import asdict, dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class AutomationTypeEnum(Enum):
    AC = "AC ON/OFF"
    DC = "DC ON/OFF"


class DataTypeEnum(Enum):
    COMMAND = "command"
    RESULT = "result"
    STATUS = "status"


class StatusEnum(Enum):
    START = "start"
    FINISH = "finish"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"


class CommandEnum(Enum):
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"


class ResultEnum(Enum):
    OK = "ok"
    NG = "ng"


class BaseDataClass:
    @property
    def dict(self):
        return asdict(self)

    @property
    def json(self):
        try:
            return json.dumps(self.dict)
        except Exception:
            logger.error("dict to json failed : \n" + self.dict)


@dataclass
class Opt:
    opt_name: str = None
    opt_value: str = None


@dataclass
class OptSet:
    opt1: Opt = None
    opt2: Opt = None
    opt3: Opt = None


@dataclass
class ResultOpt(Opt):
    opt_result: str = ResultEnum.OK.value


@dataclass
class ResultOptSet:
    opt1: ResultOpt = None
    opt2: ResultOpt = None
    opt3: ResultOpt = None


@dataclass
class CommandData:
    cmd: str = None
    automation_type: str = AutomationTypeEnum.AC.value
    judge_image: bool = True
    judge_cmd: bool = True
    judge_image_opt_set: OptSet = OptSet()
    judge_cmd_opt_set: OptSet = OptSet()


@dataclass
class ResultDataStruct(BaseDataClass):
    test_no: int = 0
    result: str = ResultEnum.OK.value
    judge_image_opt_set: ResultOptSet = ResultOptSet()
    judge_cmd_opt_set: ResultOptSet = ResultOptSet()
    source_img_path: str = None

    @staticmethod
    def from_json(json_str: str):
        try:
            dict_json: dict = json.loads(json_str)
        except Exception:
            logger.error("Message is not matched json format : \n" + json_str)
        try:
            return ResultDataStruct(**dict_json)
        except Exception:
            logger.error("Message is not matched protocol format : \n" + json_str)

    @staticmethod
    def from_dict(json_dict: dict):
        return ResultDataStruct(**json_dict)


@dataclass
class StatusDataStruct(BaseDataClass):
    status: str = None


@dataclass
class WsDataStruct(BaseDataClass):
    data_type: str = None
    device_ip: str = None
    test_id: str = None
    data: dict = None
    dt: str = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
        "%Y/%m/%d %H:%M:%S"
    )

    @staticmethod
    def from_json(json_str: str):
        try:
            dict_json: dict = json.loads(json_str)
        except Exception:
            logger.error("Message is not matched json format : \n" + json_str)
        try:
            return WsDataStruct(**dict_json)
        except Exception:
            logger.error("Message is not matched protocol format : \n" + json_str)

    @staticmethod
    def from_dict(json_dict: dict):
        return WsDataStruct(**json_dict)
