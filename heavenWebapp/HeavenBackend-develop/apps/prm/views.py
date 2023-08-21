from collections import OrderedDict
from datetime import datetime

from apps.prm.serializers import (
    PlanGroupInfoSerializer,
    PlanGroupSerializer,
    PlanInfoSerializer,
    PlanSerializer,
    PlanSeriesSerializer,
)
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from modules.common.params import CommonParams
from modules.common.utils import bulk_create
from modules.common.viewset import CustomViewset
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList

from .models import Plan, PlanGroup, PlanGroupInfo, PlanInfo, PlanSeries
from .params import PlanGroupParams, PlanInfoParams, PlanSeriesParams
from .utils.utils import combine


# Create your views here.
class PlanInfoViewSet(CustomViewset):
    queryset = PlanInfo.objects.all()
    serializer_class = PlanInfoSerializer

    @swagger_auto_schema(
        tags=["[PRM] Plan Info"],
        manual_parameters=CommonParams.list_get_params,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Info"], operation_description="설명입니다")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Info"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Info"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Info"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Info"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PlanViewSet(CustomViewset):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    @swagger_auto_schema(
        tags=["[PRM] Plan"],
        operation_description="설명입니다",
        manual_parameters=CommonParams.list_get_params,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[PRM] Plan"],
        operation_description="설명입니다",
        manual_parameters=CommonParams.return_params,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[PRM] Plan"],
        operation_description="설명입니다",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PlanGroupInfoViewSet(CustomViewset):
    queryset = PlanGroupInfo.objects.all()
    serializer_class = PlanGroupInfoSerializer

    @swagger_auto_schema(
        tags=["[PRM] Plan Group Info"],
        manual_parameters=CommonParams.list_get_params,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[PRM] Plan Group Info"],
        manual_parameters=CommonParams.return_params,
        operation_description="설명입니다",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Group Info"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Group Info"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Group Info"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Group Info"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PlanSeriesViewSet(CustomViewset):
    queryset = PlanSeries.objects.all()
    serializer_class = PlanSeriesSerializer

    # 해당 plan_id에 해당하는 plan_series만 가져오도록 설정
    def get_queryset(self):
        plan_id = self.kwargs["plan_id"]  # plan_id 값을 가져옴
        queryset = PlanSeries.objects.filter(plan=plan_id)  # plan 필드를 사용하여 필터링
        return queryset

    @swagger_auto_schema(
        tags=["[PRM] Plan Series"],
        manual_parameters=PlanSeriesParams.list,
        peration_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # bulk create 생성 -> list 로 받아서 처리합니다.
    @swagger_auto_schema(
        tags=["[PRM] Plan Series"],
        manual_parameters=CommonParams.merge,
        operation_description="설명입니다",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # return Response("done")

    @swagger_auto_schema(tags=["[PRM] Plan Series"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Series"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Series"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Series"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PlanGroupViewSet(CustomViewset):
    queryset = PlanGroup.objects.all()
    serializer_class = PlanGroupSerializer

    def get_queryset(self):
        plan_id = self.kwargs["plan_id"]
        # plan_id 값을 가져옴
        queryset = PlanGroup.objects.filter(plan=plan_id)  # plan 필드를 사용하여 필터링
        return queryset

    @swagger_auto_schema(
        tags=["[PRM] Plan Group"],
        manual_parameters=CommonParams.list_get_params + PlanGroupParams.get,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        plan_type = request.GET.get("plan_type")
        queryset = self.filter_queryset(self.get_queryset().filter(plan_type=plan_type))
        serializer = self.get_serializer(queryset, many=True)
        # plangroup에 각 group 에 할당된 series 추가
        json_query = "plan_group__" + plan_type
        for query in serializer.data:
            temp_dict = {json_query: int(query["id"])}
            query["details"]["series"] = [
                inv.device + inv.tool + inv.inch_size
                for inv in PlanSeries.objects.filter(**temp_dict)
            ]

        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[PRM] Plan Group"],
        operation_description="'series_id_list'를 body에 추가하여 request 해주세요",
    )
    def create(self, request, *args, **kwargs):
        series_id_list = request.data.pop("series_id_list")
        serializer = bulk_create(self, request)
        # series.plan_group["plan_type"]에 방금 만든 id 추가하기
        for series in PlanSeries.objects.filter(id__in=series_id_list):
            series.plan_group[request.data["plan_type"]] = serializer.instance.id
            series.save()
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["[PRM] Plan Group"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # plangroup에 각 group 에 할당된 series 추가
        json_query = "plan_group__" + instance.plan_type
        temp_dict = {json_query: int(serializer.data["id"])}
        serializer.data["details"]["series"] = [
            inv.device + inv.tool + inv.inch_size
            for inv in PlanSeries.objects.filter(**temp_dict)
        ]

        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["[PRM] Plan Group"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        def clear_type_field(self, request):
            for post_series in PlanSeries.objects.filter(
                plan_group__has_key=request.data["plan_type"]
            ):
                if post_series.plan_group[request.data["plan_type"]] == instance.id:
                    post_series.plan_group.pop(request.data["plan_type"])
                    post_series.save()

        def add_type_field(self, request):
            for series in PlanSeries.objects.filter(id__in=series_id_list):
                series.plan_group[request.data["plan_type"]] = serializer.instance.id
                series.save()

        series_id_list = request.data.get("series_id_list", [])
        request.data.pop("series_id_list")
        instance = self.get_object()
        partial = kwargs.pop("partial", False)

        # series_id_list가 빈리스트라면 삭제
        if series_id_list == []:
            clear_type_field(self, request)
            self.perform_destroy(instance)

        else:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # 기존 그룹 삭제
            clear_type_field(self, request)
            # 그룹 재 삽입
            add_type_field(self, request)
        
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["[PRM] Plan Group"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[PRM] Plan Group"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for series in PlanSeries.objects.filter(plan_group__has_key=instance.plan_type):
            series.plan_group.pop(instance.plan_type)
            series.save()
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=PlanGroupParams.duplication,
        tags=["[PRM] Plan Group"],
        operation_description="설명입니다",
    )
    def duplication(self, request, *args, **kwargs):
        # is_duplicated = PlanGroup.objects.filter(
        #     group_name=request.GET.get("keyword")
        # ).exists()
        is_not_duplicated = PlanGroup.objects.filter(
            group_name=request.GET.get("group_name")
        ).exists()
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": {"is_not_duplicated": not is_not_duplicated},
        }
        return Response(response_data, status=status.HTTP_200_OK)


# class PlanGroupViewSet(CustomViewset):
#     queryset = PlanGroup.objects.all()
#     serializer_class = PlanGroupSerializer

#     def get_queryset(self):
#         plan_id = self.kwargs["plan_id"]  # plan_id 값을 가져옴
#         queryset = PlanGroup.objects.filter(plan=plan_id)  # plan 필드를 사용하여 필터링
#         return queryset

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         transed = list(serializer.data)
#         for inv in transed:
#             inv["plan_series_id_list"] = [
#                 object.id for object in PlanSeries.objects.filter(soc_group=inv["id"])
#             ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - SoC Group"],
#         # properties=SoCGroupparam.post_properties,
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def create(self, request, *args, **kwargs):
#         # 기존 create 부
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         # 추가로 plan_series_id_list를 받아서 역참조로 soc_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         transed_dict = serializer.data
#         transed_dict["plan_series_id_list"] = [
#             object.id
#             for object in PlanSeries.objects.filter(soc_group=transed_dict["id"])
#         ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed_dict,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - SoC Group"],
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def update(self, request, *args, **kwargs):
#         # 기존 update 부
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, "_prefetched_objects_cache", None):
#             instance._prefetched_objects_cache = {}

#         # 추가로 plan_series_id_list를 받아서 역참조로 soc_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)


# class SoCGroupViewSet(CustomViewset):
#     queryset = SoCGroup.objects.all()
#     serializer_class = SoCGroupSerializer

#     def get_queryset(self):
#         plan_id = self.kwargs["plan_id"]  # plan_id 값을 가져옴
#         queryset = SoCGroup.objects.filter(plan=plan_id)  # plan 필드를 사용하여 필터링
#         return queryset

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         transed = list(serializer.data)
#         for inv in transed:
#             inv["plan_series_id_list"] = [
#                 object.id for object in PlanSeries.objects.filter(soc_group=inv["id"])
#             ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - SoC Group"],
#         # properties=SoCGroupparam.post_properties,
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def create(self, request, *args, **kwargs):
#         # 기존 create 부
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         # 추가로 plan_series_id_list를 받아서 역참조로 soc_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         transed_dict = serializer.data
#         transed_dict["plan_series_id_list"] = [
#             object.id
#             for object in PlanSeries.objects.filter(soc_group=transed_dict["id"])
#         ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed_dict,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - SoC Group"],
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def update(self, request, *args, **kwargs):
#         # 기존 update 부
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, "_prefetched_objects_cache", None):
#             instance._prefetched_objects_cache = {}

#         # 추가로 plan_series_id_list를 받아서 역참조로 soc_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)

#     @swagger_auto_schema(tags=["[PRM] Plan - SoC Group"], operation_description="설명입니다")
#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)


# class SpeakerGroupViewSet(CustomViewset):
#     queryset = SpeakerGroup.objects.all()
#     serializer_class = SpeakerGroupSerializer

#     def get_queryset(self):
#         plan_id = self.kwargs["plan_id"]  # plan_id 값을 가져옴
#         queryset = SpeakerGroup.objects.filter(plan=plan_id)  # plan 필드를 사용하여 필터링
#         return queryset

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - Speaker Group"], operation_description="설명입니다"
#     )
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         transed = list(serializer.data)
#         for inv in transed:
#             inv["plan_series_id_list"] = [
#                 object.id
#                 for object in PlanSeries.objects.filter(speaker_group=inv["id"])
#             ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - Speaker Group"],
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         # 추가로 plan_series_id_list를 받아서 역참조로 speaker_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - Speaker Group"], operation_description="설명입니다"
#     )
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         transed_dict = serializer.data
#         transed_dict["plan_series_id_list"] = [
#             object.id
#             for object in PlanSeries.objects.filter(speaker_group=transed_dict["id"])
#         ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed_dict,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - Speaker Group"],
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def update(self, request, *args, **kwargs):
#         # 기존 update 부
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, "_prefetched_objects_cache", None):
#             instance._prefetched_objects_cache = {}

#         # 추가로 plan_series_id_list를 받아서 역참조로 speaker_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - Speaker Group"], operation_description="설명입니다"
#     )
#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - Speaker Group"], operation_description="설명입니다"
#     )
#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)


# class PCBGroupViewSet(CustomViewset):
#     queryset = PCBGroup.objects.all()
#     serializer_class = PCBGroupSerializer

#     def get_queryset(self):
#         plan_id = self.kwargs["plan_id"]  # plan_id 값을 가져옴
#         queryset = PCBGroup.objects.filter(plan=plan_id)  # plan 필드를 사용하여 필터링
#         return queryset

#     @swagger_auto_schema(tags=["[PRM] Plan - PCB Group"], operation_description="설명입니다")
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         transed = list(serializer.data)
#         for inv in transed:
#             inv["plan_series_id_list"] = [
#                 object.id for object in PlanSeries.objects.filter(pcb_group=inv["id"])
#             ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - PCB Group"],
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         # 추가로 plan_series_id_list를 받아서 역참조로 pcb_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(tags=["[PRM] Plan - PCB Group"], operation_description="설명입니다")
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         transed_dict = serializer.data
#         transed_dict["plan_series_id_list"] = [
#             object.id
#             for object in PlanSeries.objects.filter(pcb_group=transed_dict["id"])
#         ]
#         response_data = {
#             "datetime": datetime.now(),
#             "message": "OK",
#             "data": transed_dict,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         tags=["[PRM] Plan - PCB Group"],
#         operation_description="**plan_series_id_list 를 추가로 입력해야 합니다**",
#     )
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, "_prefetched_objects_cache", None):
#             instance._prefetched_objects_cache = {}

#         # 추가로 plan_series_id_list를 받아서 역참조로 pcb_group_id 작성
#         plan_series_id_list = request.data.pop("plan_series_id_list")
#         plan_series_list = PlanSeries.objects.filter(id__in=plan_series_id_list)
#         serializer.instance.planseries_set.set(plan_series_list)

#         response_data = {"datetime": datetime.now(), "message": "OK"}
#         return Response(response_data, status=status.HTTP_201_CREATED)

#     @swagger_auto_schema(tags=["[PRM] Plan - PCB Group"], operation_description="설명입니다")
#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)

#     @swagger_auto_schema(tags=["[PRM] Plan - PCB Group"], operation_description="설명입니다")
#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)
