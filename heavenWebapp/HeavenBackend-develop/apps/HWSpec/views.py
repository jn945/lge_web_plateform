import json
from datetime import datetime

from apps.accounts.models import User
from apps.HWCheck.models import HWCheck, HWCheckRow
from django.db import transaction
from django.db.models import CharField, Max, Q, QuerySet
from django.db.models.functions import Cast
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from modules.common.params import CommonParams
from modules.common.utils import default_response
from modules.common.viewset import CustomViewset
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .decorators import switch_model_based_on_category
from .models import Power, PowerInfo, Soc, SocInfo
from .params import HWSpecParams
from .serializers import (
    PowerInfoSerializer,
    PowerSerializer,
    SocInfoSerializer,
    SocSerializer,
)


def make_data_list(request):
    data_values = []
    for inv in request["fields"]:
        if "subCat" in inv:
            for inside_dict in inv["subCat"]:
                data_values.append(
                    [inv["name"], inside_dict["name"], inside_dict["value"]]
                )
        else:
            data_values.append([inv["name"], None, inv["value"]])
    return data_values


class SocViewSet(CustomViewset):
    queryset = Soc.objects.all()
    serializer_class = SocSerializer

    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec"],
        manual_parameters=CommonParams.list_get_params + HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    @switch_model_based_on_category()
    def list(self, request, *args, **kwargs):
        print(CommonParams.merge + HWSpecParams.categoty)
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec"],
        manual_parameters=CommonParams.merge + HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    @switch_model_based_on_category()
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if request.data.get("fields", None) is None:
            return super().create(request, *args, **kwargs)
        if isinstance(request.data, list):
            data_values = []
            for inv_data in request.data:
                print(inv_data)
                data_values.extend(make_data_list(inv_data))
        else:
            data_values = make_data_list(request.data)
        # 리스트대로 extend
        for row in data_values:
            print(row)
            instance, is_created = SocInfo.objects.get_or_create(
                row_name_1=row[0], row_name_2=row[1]
            )
            if isinstance(row[2], list):
                print("in list")
                for row_inv in row[2]:
                    if row_inv not in instance.value_list:
                        instance.value_list.append(row_inv)
            else:
                if row[2] not in instance.value_list:
                    instance.value_list.append(row[2])
            instance.save()
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    @switch_model_based_on_category()
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    @switch_model_based_on_category()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        row = serializer.instance

        # for object in serializer.instance:
        # 데이터 리스트 만들기
        if isinstance(request.data, list):
            data_values = []
            for inv_data in request.data:
                data_values.extend(make_data_list(request))
        else:
            data_values = make_data_list(request.data)
        # 리스트대로 extend
        for row in data_values:
            print(row)
            instance, is_created = SocInfo.objects.get_or_create(
                row_name_1=row[0], row_name_2=row[1]
            )
            if isinstance(row[2], list):
                print("in list")
                for row_inv in row[2]:
                    if row_inv not in instance.value_list:
                        instance.value_list.append(row_inv)
            else:
                if row[2] not in instance.value_list:
                    instance.value_list.append(row[2])
            instance.save()
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    @switch_model_based_on_category()
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    @switch_model_based_on_category()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class SocSearchViewSet(CustomViewset):
    queryset = Soc.objects.all()
    serializer_class = SocSerializer
    # -------------------searched-----------------

    # 사용자가 선택한 Soc search에 추가
    # @swagger_auto_schema(
    #     tags=["[HWSpec] HWSpec - Search"],
    #     manual_parameters=HWSpecParams.categoty,
    #     operation_description="설명입니다. id_list를 body에 따로 추가해주세요",
    #     request_body=CommonParams.request_body_list,
    # )
    @switch_model_based_on_category()
    def put_search(self, request, pk=None):
        # 로그인 미 구현으로 인해 잠시 주석 처리, 원복시 User.objects.get(id=1) ->request.user 로 바꿔주세요
        request_Soc_ids = set(request.data.get("id_list", []))
        lastest_Soc_set = set(
            list(User.objects.get(id=1).soc_user_search.values_list("pk", flat=True))
        )
        User.objects.get(id=1).soc_user_search.add(*(request_Soc_ids - lastest_Soc_set))
        User.objects.get(id=1).soc_user_search.remove(
            *(lastest_Soc_set - request_Soc_ids)
        )
        return Response({"message": "put to Search successfully"})

    # 사용자가 선택한 Soc search에 조회
    # @swagger_auto_schema(
    #     tags=["[HWSpec] HWSpec - Search"],
    #     manual_parameters=HWSpecParams.categoty,
    #     operation_description="search설명입니다",
    # )
    # @switch_model_based_on_category()
    def get_search(self, request):
        # searched_Soc = request.user.Soc_user_search.all()
        # 로그인 미 구현으로 인해 잠시 주석 처리, 원복시 User.objects.get(id=1) ->request.user 로 바꿔주세요
        searched_Soc = User.objects.get(id=1).Soc_user_search.all()
        # if len(searched_Soc) == 0:
        #     max_year = (
        #         Soc.objects.all()
        #         .annotate(year_int=Cast("year", CharField()))
        #         .aggregate(max_year=Max("year_int"))["max_year"]
        #     )
        #     highest_year_instances = Soc.objects.all().filter(year=str(max_year))
        #     request.user.Soc_user_search.add(*highest_year_instances)
        #     return self.get_search(request)
        serializer = self.get_serializer(searched_Soc, many=True)
        return Response(serializer.data)

    # 사용자가 선택한 Soc search에 조회
    # @swagger_auto_schema(
    #     tags=["[HWSpec] HWSpec - Search"],
    #     manual_parameters=HWSpecParams.categoty,
    #     operation_description="search설명입니다",
    # )
    @switch_model_based_on_category()
    def get_search_id_list(self, request):
        # searched_Soc = request.user.Soc_user_search.all()
        # 로그인 미 구현으로 인해 잠시 주석 처리, 원복시 User.objects.get(id=1) ->request.user 로 바꿔주세요
        searched_Soc = User.objects.get(id=1).Soc_user_search.all()
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": [inv.id for inv in searched_Soc],
        }
        return Response(response_data, status=status.HTTP_200_OK)


# -------------------compare-----------------
class SocCompareViewSet(CustomViewset):
    queryset = Soc.objects.all()
    serializer_class = SocSerializer

    # 사용자가 선택한 Soc compare에 추가
    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec - Compare"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다. id_list를 body에 따로 추가해주세요",
        request_body=CommonParams.request_body_list,
    )
    @switch_model_based_on_category()
    def put_compare(self, request, pk=None):
        # 로그인 미 구현으로 인해 잠시 주석 처리, 원복시 User.objects.get(id=1) ->request.user 로 바꿔주세요
        category = request.GET.get("category")
        request_Soc_ids = set(request.data.get("id_list", []))
        user = User.objects.get(id=1)
        lastest_Soc_set = set(
            list(getattr(user, category + "_user_compare").values_list("id", flat=True))
        )
        if category == "power":
            print("파워")
            user.power_user_compare.add(*(request_Soc_ids - lastest_Soc_set))
            user.power_user_compare.remove(*(lastest_Soc_set - request_Soc_ids))
            print(user.power_user_compare.all())
        elif category == "soc":
            user.soc_user_compare.add(*(request_Soc_ids - lastest_Soc_set))
            user.soc_user_compare.remove(*(lastest_Soc_set - request_Soc_ids))
        user.save()
        return default_response(None, status=status.HTTP_200_OK)

    # 사용자가 선택한 Soc compare에 조회
    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec - Compare"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="Compare설명입니다",
    )
    @switch_model_based_on_category()
    def get_compare(self, request):
        # 로그인 미 구현으로 인해 잠시 주석 처리
        category = request.GET.get("category")
        compared_Soc = getattr(User.objects.get(id=1), category + "_user_compare").all()
        serializer = self.get_serializer(compared_Soc, many=True)
        return default_response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec - Compare"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="Compare설명입니다",
    )
    @switch_model_based_on_category()
    def delete_compare(self, request, pk):
        spec_instance = self.queryset.get(pk=pk)
        print(spec_instance)
        spec_instance.user_compare.remove(User.objects.get(id=1))  # request.user로 복원
        spec_instance.save()
        return default_response(None, status.HTTP_204_NO_CONTENT)

    # 사용자가 선택한 Soc compare_id_list에 조회
    @swagger_auto_schema(
        tags=["[HWSpec] HWSpec - Compare"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="Compare설명입니다",
    )
    @switch_model_based_on_category()
    def get_compare_id_list(self, request):
        # 로그인 미 구현으로 인해 잠시 주석 처리
        category = request.GET.get("category")
        compared_Soc = getattr(User.objects.get(id=1), category + "_user_compare").all()
        data = [inv.id for inv in compared_Soc]
        return default_response(data, status.HTTP_200_OK)


class SocInfoViewSet(CustomViewset):
    queryset = SocInfo.objects.all()
    serializer_class = SocInfoSerializer

    @swagger_auto_schema(
        tags=["[HWSpec] Info"],
        manual_parameters=CommonParams.list_get_params + HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWSpec] Info"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    def create(self, request, *args, **kwargs):
        rows = request.data
        for row in rows:
            instance, bool = self.queryset.get_or_create(row_name=row["row_name"])
            instance.type_field = row["type_field"]
            instance.unit_field = row["unit_field"]
            for row_inv in row["value"]:
                if row_inv not in instance.category:
                    instance.category.append(row_inv)
            instance.save()
        return default_response(None, status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["[HWSpec] Info"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWSpec] Info"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    def update(self, request, *args, **kwargs):
        rows = request.data
        for row in rows:
            instance, bool = self.queryset.get_or_create(row_name=row["row_name"])
            instance.type_field = row["type_field"]
            instance.unit_field = row["unit_field"]
            for row_inv in row["value"]:
                if row_inv not in instance.category:
                    instance.category.append(row_inv)
            instance.save()
        return default_response(None, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[HWSpec] Info"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWSpec] Info"],
        manual_parameters=HWSpecParams.categoty,
        operation_description="설명입니다",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


"""
class PowerViewSet(viewsets.ModelViewSet):
    queryset = Power.objects.all()
    serializer_class = PowerSerializer

    @swagger_auto_schema(tags=['[HWcheck] Power'],manual_parameters = params.Soc_get_params, operation_description='설명입니다')
    def list(self, request, *args, **kwargs):
        field_name = request.query_params.get('field_name', None)
        search_query = request.query_params.get('keyword', None)
        if field_name and search_query:
            queryset = self.queryset.filter(
                Q(**{field_name + '__icontains': search_query})
            )
        else:
            return super().list(request, *args, **kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(tags=['[HWcheck] Power'],query_serializer=serializer_class, operation_description='설명입니다')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['[HWcheck] Power'], operation_description='설명입니다')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power'], operation_description='설명입니다')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power'], operation_description='설명입니다')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power'], operation_description='설명입니다')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class PowerInfoViewSet(viewsets.ModelViewSet):
    queryset = PowerInfo.objects.all()
    serializer_class = PowerInfoSerializer
    @swagger_auto_schema(tags=['[HWcheck] Power Info'], operation_description='설명입니다')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power Info'], operation_description='설명입니다')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power Info'], operation_description='설명입니다')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power Info'], operation_description='설명입니다')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power Info'], operation_description='설명입니다')
    def partial_update(self, request, *args, **kwargs):
        Socinfo_data = request.data.get('Socinfo')
        for data in Socinfo_data:
            instance_info,bool_info = self.queryset.get_or_create(row_name = data['row_name'])
            instance_info.type = data['type']
            instance_info.unit = data['unit']
            category = json.loads(instance_info.category)
            if data['value'] not in category:
                category.append(data['value'])
            instance_info.category = json.dumps(category)
            instance_info.save()
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(tags=['[HWcheck] Power Info'], operation_description='설명입니다')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)"""
