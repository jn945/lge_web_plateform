import asyncio
import logging
from multiprocessing import Process
from time import sleep

import psutil
from modules.data_struct.WsDataStruct import (
    CommandEnum,
    DataTypeEnum,
    ResultDataStruct,
    ResultEnum,
    ResultOpt,
    ResultOptSet,
    StatusDataStruct,
    StatusEnum,
    WsDataStruct,
)

logger = logging.getLogger(__name__)

process_dict: dict[str, Process] = {}


async def send_status_data(ws, device_ip: str, test_id: str, status: StatusEnum):
    status_data = StatusDataStruct(status.value)
    ws_data = WsDataStruct(
        DataTypeEnum.STATUS.value, device_ip, test_id, status_data.dict
    )
    await ws.send(ws_data.json)


async def send_result_data(
    ws,
    args: WsDataStruct,
    test_no: int,
    result: ResultEnum,
    result_judge_image: ResultOptSet,
    result_judge_cmd: ResultOptSet,
    source_img_path: str,
):
    result_data = ResultDataStruct(
        test_no, result.value, result_judge_image, result_judge_cmd, source_img_path
    )
    ws_data = WsDataStruct(
        DataTypeEnum.RESULT.value, args.device_ip, args.test_id, result_data.dict
    )
    await ws.send(ws_data.json)


async def task_test(ws, args: WsDataStruct):
    global process_list

    await send_status_data(ws, args.device_ip, args.test_id, StatusEnum.START)

    i = 0

    while i < 100:
        source_img_path = f"path/img_{i}.png"
        result_judge_image = ResultOptSet(
            ResultOpt("opt1", "0.1", ResultEnum.OK.value),
            ResultOpt("opt2", "0.1", ResultEnum.OK.value),
            ResultOpt("opt3", "0.1", ResultEnum.OK.value),
        )
        result_judge_cmd = ResultOptSet(
            ResultOpt("opt1", "0.1", ResultEnum.OK.value),
            ResultOpt("opt2", "0.1", ResultEnum.OK.value),
            ResultOpt("opt3", "0.1", ResultEnum.OK.value),
        )
        await send_result_data(
            ws,
            args,
            i,
            ResultEnum.OK,
            result_judge_image,
            result_judge_cmd,
            source_img_path,
        )
        i += 1
        sleep(0.5)

    await send_status_data(ws, args.device_ip, args.test_id, StatusEnum.FINISH)
    process_dict.pop(args.test_id)


def tast_test_run(ws, args: WsDataStruct):
    asyncio.run(task_test(ws, args))


def test_start(ws, args: WsDataStruct):
    global process_list
    if args.test_id not in process_dict:
        p1 = Process(target=tast_test_run, args=(ws, args), daemon=True)
        process_dict[args.test_id] = p1
        p1.start()
    else:
        logger.error(f"START: {args.test_id} is already started")


async def test_stop(ws, args: WsDataStruct):
    global process_dict

    if args.test_id in process_dict:
        process_dict[args.test_id].terminate()
        process_dict.pop(args.test_id)
        await send_status_data(ws, args.device_ip, args.test_id, StatusEnum.STOP)
    else:
        logger.error("STOP: process does not exist")


async def test_pause(ws, args: WsDataStruct):
    global process_dict

    if args.test_id in process_dict:
        p = psutil.Process(process_dict[args.test_id].pid)
        if p.status() == "stopped":
            logger.info("PAUSE: process already paused")
        else:
            p.suspend()
            await send_status_data(ws, args.device_ip, args.test_id, StatusEnum.PAUSE)
    else:
        logger.error("PAUSE: process does not exist")


async def test_resume(ws, args: WsDataStruct):
    global process_dict

    if args.test_id in process_dict:
        p = psutil.Process(process_dict[args.test_id].pid)
        if p.status() != "stopped":
            logger.info("RESUME: process not paused")
        else:
            p.resume()
            await send_status_data(ws, args.device_ip, args.test_id, StatusEnum.RESUME)
    else:
        logger.error("RESUME: process does not exist")


async def excute_cmd(ws, ws_data: WsDataStruct):
    if ws_data.data["cmd"] == CommandEnum.START.value:
        test_start(ws, ws_data)
    elif ws_data.data["cmd"] == CommandEnum.STOP.value:
        await test_stop(ws, ws_data)
    elif ws_data.data["cmd"] == CommandEnum.PAUSE.value:
        await test_pause(ws, ws_data)
    elif ws_data.data["cmd"] == CommandEnum.RESUME.value:
        await test_resume(ws, ws_data)
