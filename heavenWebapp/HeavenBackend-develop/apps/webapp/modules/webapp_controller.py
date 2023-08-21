def process_recieved_data(text_data: str):
    import json

    from modules.wsctrl.data_struct.WsDataStruct import (
        DataTypeEnum,
        ResultDataStruct,
        StatusDataStruct,
    )

    json_data = json.loads(text_data)
    if json_data["data_type"] == DataTypeEnum.STATUS.value:
        recieved_data = StatusDataStruct.from_json(text_data)
    elif json_data["data_type"] == DataTypeEnum.RESULT.value:
        recieved_data = ResultDataStruct.from_json(text_data)
    return recieved_data
