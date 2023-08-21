from drf_yasg import openapi
from rest_framework import serializers


class CommonParams:
    merge = [
        openapi.Parameter(
            "mode",
            openapi.IN_QUERY,
            description="merge시, list 형태로 data를 전달해야합니다",
            type=openapi.TYPE_STRING,
        ),
    ]
    list = [
        openapi.Parameter(
            "column_name",
            openapi.IN_QUERY,
            description="column_name 입니다",
            type=openapi.TYPE_STRING,
        ),
    ]
    request_body_list = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id_list": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER),
                description="id_list를 넣어주세요",
            ),
        },
    )
    list_get_params = [
        openapi.Parameter(
            "search_field_name",
            openapi.IN_QUERY,
            description="filtering을 원하시는 field_name을 입력해주세요.\n filtering 한 row들만 반환됩니다. 대소문자 구별하지 않습니다.",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "keyword",
            openapi.IN_QUERY,
            description="filtering을 원하시는 keyword을 입력해주세요.\n filtering 한 row들만 반환됩니다. 대소문자 구별하지 않습니다.",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "fields",
            openapi.IN_QUERY,
            description="filtering을 원하시는 fields를 입력해주세요.\n 입력한 fields만 반환됩니다. 대소문자 구별하지 않습니다.",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "column_name",
            openapi.IN_QUERY,
            description="listing을 원하시는 field를 입력해주세요 \n 입력한 fields에서 중복을 제거하고 반환합니다.",
            type=openapi.TYPE_STRING,
        ),
    ]
    return_params = [
        openapi.Parameter(
            "return",
            openapi.IN_QUERY,
            description="return 할 data를 입력해주세요",
            type=openapi.TYPE_STRING,
        ),
    ]
    retrieve_get = [
        openapi.Parameter(
            "column_name",
            openapi.IN_QUERY,
            description="listing을 원하시는 field를 입력해주세요 \n 입력한 fields에서 중복을 제거하고 반환합니다.",
            type=openapi.TYPE_STRING,
        ),
    ]
    list_get_pagenation = [
        openapi.Parameter(
            "page",
            openapi.IN_QUERY,
            description="page 번호를 입력해주세요.",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "page",
            openapi.IN_QUERY,
            description="page_size를 입력해주세요.",
            type=openapi.TYPE_STRING,
        ),
    ]
    delete_id_list = [
        openapi.Parameter(
            "id_list",
            openapi.IN_QUERY,
            description="삭제할 id_list를 입력해주세요.\n '[]'기호 없이 구분자는 , 로 담아주시면 됩니다.(ex: 130,131)",
            type=openapi.TYPE_STRING,
        ),
    ]


webapp_cmd_start_request_schema_dict = openapi.Schema(
    title=("WebAppCmdStart"),
    type=openapi.TYPE_OBJECT,
    properties={
        "device_ip": openapi.Schema(
            type=openapi.TYPE_STRING,
            description=("device_ip"),
            example="127.0.1.1",
        ),
        "test_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description=("test_id"),
            example="test_1",
        ),
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description=("data"),
            properties={
                "automation_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=("automation_type"),
                    example="AC",
                    enum=["AC", "DC"],
                ),
                "judge_image": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description=("judge_image"),
                    example=True,
                ),
                "judge_cmd": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description=("judge_cmd"),
                    example=True,
                ),
                "judge_image_opt_set": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description=("judge_image_opt_set"),
                    properties={
                        "opt1": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description=("judge_image_opt1"),
                            properties={
                                "opt_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_name"),
                                    example="opt1",
                                ),
                                "opt_value": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_value"),
                                    example="opt1_value",
                                ),
                            },
                        ),
                        "opt2": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description=("judge_image_opt2"),
                            properties={
                                "opt_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_name"),
                                    example="opt2",
                                ),
                                "opt_value": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_value"),
                                    example="opt2_value",
                                ),
                            },
                        ),
                        "opt3": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description=("judge_image_opt3"),
                            properties={
                                "opt_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_name"),
                                    example="opt3",
                                ),
                                "opt_value": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_value"),
                                    example="opt3_value",
                                ),
                            },
                        ),
                    },
                ),
                "judge_cmd_opt_set": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description=("judge_cmd_opt_set"),
                    properties={
                        "opt1": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description=("judge_cmd_opt1"),
                            properties={
                                "opt_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_name"),
                                    example="opt1",
                                ),
                                "opt_value": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_value"),
                                    example="opt1_value",
                                ),
                            },
                        ),
                        "opt2": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description=("judge_cmd_opt2"),
                            properties={
                                "opt_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_name"),
                                    example="opt2",
                                ),
                                "opt_value": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_value"),
                                    example="opt2_value",
                                ),
                            },
                        ),
                        "opt3": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description=("judge_cmd_opt3"),
                            properties={
                                "opt_name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_name"),
                                    example="opt3",
                                ),
                                "opt_value": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description=("opt_value"),
                                    example="opt3_value",
                                ),
                            },
                        ),
                    },
                ),
            },
        ),
    },
)
