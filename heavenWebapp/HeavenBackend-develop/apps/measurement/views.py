import json
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any

import reversion
from apps.measurement.tasks import tasks
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from django.db import models, transaction
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from manage import scheduler
from modules.common.params import CommonParams
from modules.common.utils import default_response
from modules.common.viewset import CustomViewset
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from reversion.models import Version
from scheduler import initialize_scheduler

from .decorators import check_user_group
from .models import MeasurementRequest, Result, TestItemInfo
from .serializers import (
    MeasurementRequestSerializer,
    ResultSerializer,
    TestItemInfoSerializer,
)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return default_response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            ),
            status=status.HTTP_200_OK,
        )

    page_query_param = "page"
    page_query_description = "page num을 입력해주세요"
    page_size_query_param = "page_size"
    page_size_query_description = "page size 을 입력해주세요"

    page_size = 9e9  # 한 페이지에 표시할 아이템 수 설정


class TestItemInfoViewSet(CustomViewset):
    queryset = TestItemInfo.objects.all()
    serializer_class = TestItemInfoSerializer

    @swagger_auto_schema(
        tags=["[Measurement] TestItemInfo"],
        manual_parameters=CommonParams.list_get_params,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Measurement] TestItemInfo"], operation_description="설명입니다"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Measurement] TestItemInfo"], operation_description="설명입니다"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Measurement] TestItemInfo"], operation_description="설명입니다"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Measurement] TestItemInfo"], operation_description="설명입니다"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Measurement] TestItemInfo"], operation_description="설명입니다"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MeasurementRequestViewSet(CustomViewset):
    queryset = MeasurementRequest.objects.all().order_by("-id")
    serializer_class = MeasurementRequestSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=["[Measurement] Request"],
        manual_parameters=CommonParams.list_get_params,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    @swagger_auto_schema(tags=["[Measurement] Request"], operation_description="설명입니다")
    def create(self, request, *args, **kwargs):
        # 기존 create 함수 code
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # scheduler 등록을 위한 정보 collect
        # request_id = serializer.data["id"]
        # instance = MeasurementRequest.objects.get(id=request_id)
        # scheduled_date_start = instance.scheduled_date["start"]
        # scheduled_date_end = instance.scheduled_date["end"]

        # # scheduled_date_start
        # initialize_scheduler()
        # trigger = DateTrigger(run_date=scheduled_date_start)
        # job = scheduler.add_job(
        #     tasks.update_request_status,
        #     trigger,
        #     args=[request_id],
        # )
        # instance.job_id["start_event"] = job.id

        # # scheduled_date_end
        # trigger = DateTrigger(run_date=scheduled_date_end)
        # job = scheduler.add_job(
        #     tasks.update_request_status,
        #     trigger,
        #     args=[request_id],
        # )
        # instance.job_id["end_event"] = job.id
        # instance 저장
        # instance.save()
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["[Measurement] Request"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    @swagger_auto_schema(tags=["[Measurement] Request"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        post_instance = self.get_object()
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        print(post_instance.status.lower(), request.data["status"].lower())
        if (
            post_instance.status.lower() == "saved"
            and request.data["status"].lower() == "requested"
        ):
            instance.scheduled_date = {
                "start": request.data["request_date"],
                "end": request.data["target_date"],
            }
            instance.save()

        if (
            # post_instance.status.lower() == "requested"
            request.data["status"].lower()
            == "confirmed"
        ):
            job_id = instance.job_id
            print(job_id)
            # start date 수정
            # scheduler 등록을 위한 정보 collect
            scheduled_date_start = instance.scheduled_date["start"]
            scheduled_date_end = instance.scheduled_date["end"]

            # scheduled_date_start
            trigger = DateTrigger(run_date=scheduled_date_start)
            print(trigger)
            job = scheduler.add_job(
                tasks.update_request_status,
                trigger,
                args=[instance.id],
            )
            instance.job_id["start_event"] = job.id

            # scheduled_date_end
            trigger = DateTrigger(run_date=scheduled_date_end)
            job = scheduler.add_job(
                tasks.update_request_status,
                trigger,
                args=[instance.id],
            )
            instance.job_id["end_event"] = job.id
            instance.save()

            # if scheduler.get_job(job_id["start"]) is not None:
            #     print(f"Job with id '{job_id}' exists.")
            #     # job 현재 + 변경
            #     job = scheduler.get_job(job_id["start_event"])
            #     current_run_date = job.trigger.run_date
            #     # job 변경
            #     new_run_date = request.data["scheduled_date_start"]
            #     job.reschedule(trigger="date", run_date=new_run_date)
            #     print(
            #         f"Current run date: {current_run_date}  -> ",
            #         f"Updated run date: {job.trigger.run_date}",
            #     )
            # else:
            #     print(f"Job with id '{job_id}' doesn't exists.")
            # # end date 수정
            # if scheduler.get_job(job_id["end_event"]) is not None:
            #     print(f"Job with id '{job_id}' exists.")
            #     # job 현재 + 변경
            #     job = scheduler.get_job(job_id["end_event"])
            #     current_run_date = job.trigger.run_date
            #     # job 변경
            #     new_run_date = request.data["scheduled_end_start"]
            #     job.reschedule(trigger="date", run_date=new_run_date)
            #     print(
            #         f"Current run date: {current_run_date}  -> ",
            #         f"Updated run date: {job.trigger.run_date}",
            #     )
            # else:
            #     print(f"Job with id '{job_id}' doesn't exists.")

        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_200_OK)

    @transaction.atomic
    @swagger_auto_schema(tags=["[Measurement] Request"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @transaction.atomic
    @swagger_auto_schema(tags=["[Measurement] Request"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        job_ids = instance.job_id
        for id in job_ids:
            try:
                job_id = job_ids[id]
                if job_id:
                    scheduler.remove_job(job_id)
            except JobLookupError:
                pass

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ResultViewset(CustomViewset):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    @swagger_auto_schema(
        tags=["[Measurement] Result"],
        manual_parameters=CommonParams.list_get_params,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Measurement] Result"],
        operation_description="*** history_comment 를 추가로 json 에 포함해서 입력해주세요 ***",
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        with reversion.create_revision():
            # history create 부
            history_comment = request.data["history_comment"]
            reversion.set_comment(history_comment)
            request.data.pop("history_comment", None)
        # 기존 create 함수 code
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["[Measurement] Result"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Measurement] Result"],
        operation_description="*** history_comment 를 추가로 json 에 포함해서 입력해주세요 ***",
    )
    def update(self, request, *args, **kwargs):
        with reversion.create_revision():
            # history comment는 별개로 작성
            # reversion 부
            history_comment = request.data["history_comment"]
            reversion.set_comment(history_comment)
            request.data.pop("history_comment", None)
            partial = kwargs.pop("partial", False)
            # super() update 부
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}
            response_data = {"datetime": datetime.now(), "message": "OK"}
            return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["[Measurement] Result"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[Measurement] Result"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ResultHistoryApiviewList(APIView):
    queryset = Version.objects.all()
    serializer_class = ResultSerializer

    @swagger_auto_schema(
        tags=["[Measurement] Result History"], operation_description="설명입니다"
    )
    def get(self, request, *args, **kwargs):
        # result_id 에 해당하는 document history만 filtering
        result_id = self.kwargs["result_id"]
        versions = self.queryset.filter(object_id=result_id, content_type_id=25)
        serialized_data_list, comment_list, final_data = [], [], []
        for version in versions:
            # string으로 쓰여진 reversion data를 Document에 맞춰서 instance화
            data = json.loads(version.serialized_data)[0]["fields"]
            # reversion id 로 id 변환
            data["id"] = version.id
            serialized_data_list.append(data)

            # history comment 가져오기
            comment = version.revision.comment
            comment_list.append(comment)
        # serialize 후 comment 삽입
        for result, comment in zip(serialized_data_list, comment_list):
            result["history_comment"] = comment
            final_data.append(result)
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": final_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ResultHistoryApiview(APIView):
    queryset = Version.objects.all()
    serializer_class = ResultSerializer

    @swagger_auto_schema(
        tags=["[Measurement] Result History"], operation_description="설명입니다"
    )
    def get(self, request, *args, **kwargs):
        history_id = self.kwargs["id"]
        version = self.queryset.get(id=history_id)
        data = json.loads(version.serialized_data)[0]["fields"]
        data["id"] = history_id
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[Measurement] Result History"], operation_description="설명입니다"
    )
    def delete(self, request, *args, **kwargs):
        history_id = self.kwargs["id"]
        version = self.queryset.filter(id=history_id)
        version.delete()
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data)
